#!/usr/bin/env python3
"""Validate the two independently installable skill packages and their local links."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
NAMES = ("geo-optimization", "geo-optimization-zh")


def check(condition, message):
    if not condition:
        raise ValueError(message)


def validate():
    for name in NAMES:
        directory = ROOT / "skills" / name
        entry = directory / "SKILL.md"
        content = entry.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
        check(match is not None, f"missing frontmatter: {entry}")
        metadata = yaml.safe_load(match.group(1))
        check(metadata["name"] == name, f"folder/name mismatch: {entry}")
        check(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) and len(name) <= 64,
              f"invalid skill name: {name}")
        description = metadata.get("description")
        check(isinstance(description, str) and 0 < len(description) <= 1024,
              f"invalid description: {entry}")
        check(metadata.get("license") == "MIT", f"license mismatch: {entry}")
        check(len(content.splitlines()) < 500, f"entrypoint too long: {entry}")
        ui = yaml.safe_load((directory / "agents/openai.yaml").read_text(encoding="utf-8"))
        interface = ui["interface"]
        check(25 <= len(interface["short_description"]) <= 64, f"UI blurb length: {name}")
        check("$" + name in interface["default_prompt"], f"UI invocation mismatch: {name}")
        check(ui.get("policy", {}).get("allow_implicit_invocation", True),
              f"implicit invocation unexpectedly disabled: {name}")
        for path in re.findall(r"`(references/[^`]+\.md)`", content):
            check((directory / path).is_file(), f"missing routed reference: {name}/{path}")
        for path in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
            check((directory / path).read_bytes() == (ROOT / path).read_bytes(),
                  f"standalone attribution missing or inconsistent: {name}/{path}")

    for file in ROOT.rglob("*"):
        if not file.is_file() or any(part in {".git", "__pycache__", ".venv"} for part in file.parts):
            continue
        text = file.read_text(encoding="utf-8")
        check("[TO" + "DO:" not in text, f"unfinished scaffold: {file.relative_to(ROOT)}")
        for pattern in (
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
            r"\bgh[pousr]_[A-Za-z0-9]{20,}",
            r"\bgithub_pat_[A-Za-z0-9_]{20,}",
            r"\bAKIA[A-Z0-9]{16}\b",
            r"\bsk-[A-Za-z0-9_-]{20,}",
            r"/Users/[A-Za-z0-9_.-]+/",
        ):
            check(re.search(pattern, text) is None, f"possible private data: {file.relative_to(ROOT)}")
        if file.suffix == ".md":
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in link or link.startswith("#"):
                    continue
                path = unquote(link.split("#", 1)[0]).strip("<>")
                check((file.parent / path).is_file(), f"broken local link: {file.relative_to(ROOT)} -> {link}")

    first, second = (ROOT / "skills" / name for name in NAMES)
    check(
        (first / "scripts/score_visibility.py").read_bytes()
        == (second / "scripts/score_visibility.py").read_bytes(),
        "language packages have divergent measurement tools",
    )
    check(
        (first / "assets/sample-observations.jsonl").read_bytes()
        == (second / "assets/sample-observations.jsonl").read_bytes(),
        "language packages have divergent synthetic samples",
    )
    check(
        {path.name for path in (first / "references").glob("*.md")}
        == {path.name for path in (second / "references").glob("*.md")},
        "language packages have different reference coverage",
    )
    print("PASS: two self-contained skills, UI metadata, local links, package parity, and private-data patterns")


if __name__ == "__main__":
    try:
        validate()
    except (ValueError, KeyError, OSError, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
