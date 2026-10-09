#!/usr/bin/env python3
"""Aggregate annotated GEO observations offline; no inference or provider scoring."""

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


COHORT_FIELDS = ("engine", "model", "language", "market", "retrieval")
LABEL_FIELDS = (
    "target_mentioned", "target_recommended", "cited_urls", "sentiment", "factual_error"
)


def normalize_domain(value):
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("domain must be a nonempty hostname")
    try:
        value = value.rstrip(".").encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ValueError("invalid domain") from exc
    if len(value) > 253 or any(
        not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", part)
        for part in value.split(".")
    ):
        raise ValueError("domain must be a hostname without scheme, port, or path")
    return value


def citation_host(value):
    if not isinstance(value, str) or any(char.isspace() for char in value):
        raise ValueError("citation must be an HTTP(S) URL without whitespace")
    parsed = urlsplit(value)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise ValueError("citation must be an absolute HTTP(S) URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("citation URLs must not contain credentials")
    _ = parsed.port  # Validate malformed ports, even though ports do not affect ownership.
    return normalize_domain(parsed.hostname)


def is_owned(url, domains):
    host = citation_host(url)
    return any(host == domain or host.endswith("." + domain) for domain in domains)


def parse_timestamp(value):
    if not isinstance(value, str):
        raise ValueError("observed_at must be a timestamp string")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("observed_at must include a timezone")
    return parsed.astimezone(timezone.utc)


def validate_record(record):
    if not isinstance(record, dict):
        raise ValueError("each record must be an object")
    for key in ("run_id", "prompt_id", *COHORT_FIELDS):
        value = record.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a nonempty string")
        if value != value.strip():
            raise ValueError(f"{key} must not have surrounding whitespace")
    parse_timestamp(record.get("observed_at"))
    if record["retrieval"] not in {"web", "off", "supplied", "unknown"}:
        raise ValueError("invalid retrieval mode")
    if record.get("status") not in {"ok", "error"}:
        raise ValueError("status must be ok or error")
    if record["status"] == "error":
        if any(record.get(key) is not None for key in LABEL_FIELDS):
            raise ValueError("error records must not contain outcome labels")
        return
    for key in LABEL_FIELDS:
        if key not in record:
            raise ValueError(f"missing {key}; use null for unknown")
    for key in ("target_mentioned", "target_recommended", "factual_error"):
        if record[key] is not None and type(record[key]) is not bool:
            raise ValueError(f"{key} must be boolean or null")
    if record["target_recommended"] is True and record["target_mentioned"] is not True:
        raise ValueError("a recommendation requires a confirmed mention")
    sentiment = record["sentiment"]
    if sentiment is not None and sentiment not in (
        "positive", "neutral", "negative", "mixed"
    ):
        raise ValueError("invalid sentiment")
    if record["target_mentioned"] is not True and (
        sentiment is not None or record["factual_error"] is not None
    ):
        raise ValueError("sentiment and factual_error require a confirmed mention")
    urls = record["cited_urls"]
    if urls is not None:
        if not isinstance(urls, list):
            raise ValueError("cited_urls must be a list or null")
        for url in urls:
            citation_host(url)


def read_records(path):
    records, seen = [], set()
    with Path(path).open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                validate_record(record)
                if record["run_id"] in seen:
                    raise ValueError("duplicate run_id")
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"line {line_number}: {exc}") from exc
            seen.add(record["run_id"])
            records.append(record)
    return records


def metric(values):
    known = [value for value in values if value is not None]
    numerator = sum(value is True for value in known)
    return {
        "numerator": numerator,
        "denominator": len(known),
        "rate": numerator / len(known) if known else None,
        "unknown": len(values) - len(known),
    }


def summarize(records, domains):
    ok = [record for record in records if record["status"] == "ok"]
    mentioned = [record for record in ok if record["target_mentioned"] is True]
    dates = [parse_timestamp(record["observed_at"]) for record in records]
    counts = Counter(record["prompt_id"] for record in ok)
    return {
        "observations": len(records),
        "successful": len(ok),
        "failed": len(records) - len(ok),
        "observed_from_utc": min(dates).isoformat() if dates else None,
        "observed_to_utc": max(dates).isoformat() if dates else None,
        "successful_per_prompt": dict(sorted(counts.items())),
        "attempted_per_prompt": dict(sorted(Counter(
            record["prompt_id"] for record in records
        ).items())),
        "metrics": {
            "mention_rate": metric([record["target_mentioned"] for record in ok]),
            "recommendation_rate": metric([
                record["target_recommended"] for record in ok
            ]),
            "owned_citation_rate": metric([
                None if record["cited_urls"] is None else
                any(is_owned(url, domains) for url in record["cited_urls"])
                for record in ok
            ]),
            "negative_sentiment_rate": metric([
                None if record["sentiment"] is None else record["sentiment"] == "negative"
                for record in mentioned
            ]),
            "factual_error_rate": metric([record["factual_error"] for record in mentioned]),
        },
    }


def build_report(records, domains):
    groups = defaultdict(list)
    for record in records:
        groups[tuple(record[key] for key in COHORT_FIELDS)].append(record)
    cohorts = [
        {"cohort": dict(zip(COHORT_FIELDS, key)), **summarize(group, domains)}
        for key, group in sorted(groups.items())
    ]
    overall = summarize(records, domains)
    warnings = [
        "Pooled rates weight responses; compare matched cohorts and prompt panels.",
        "Labels are user-supplied; this tool does not verify facts or citation support.",
    ]
    if not overall["successful"]:
        warnings.append("No successful observations; outcome rates are unknown.")
    if overall["failed"]:
        warnings.append("Failed observations are excluded from outcome denominators.")
    if any(value["unknown"] for value in overall["metrics"].values()):
        warnings.append("Some labels are unknown; inspect each metric's denominator.")
    if any(len(set(cohort["successful_per_prompt"].values())) > 1 for cohort in cohorts):
        warnings.append("Successful repetitions are unbalanced within at least one cohort.")
    return {
        "schema_version": "1.0",
        "owned_domains": sorted(domains),
        "overall": overall,
        "cohorts": cohorts,
        "warnings": warnings,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Annotated JSONL file")
    parser.add_argument("--domain", action="append", required=True, help="Owned hostname; repeatable")
    parser.add_argument("--output", help="Write JSON instead of printing to stdout")
    args = parser.parse_args()
    try:
        if args.output and Path(args.input).resolve() == Path(args.output).resolve():
            raise ValueError("output must not overwrite the input")
        domains = {normalize_domain(domain) for domain in args.domain}
        report = build_report(read_records(args.input), domains)
        rendered = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            Path(args.output).write_text(rendered, encoding="utf-8")
        else:
            sys.stdout.write(rendered)
    except (OSError, ValueError, TypeError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    main()
