from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    code: str
    message: str


PLACEHOLDER_RE = re.compile(r"(\{\{[^}]+\}\}|<[^>]*(?:TODO|KEY|TOKEN|SECRET)[^>]*>)", re.I)
SECRET_RE = re.compile(r"(sk-[A-Za-z0-9._-]{8,}|(?:api[_-]?key|token|password)\s*[:=]\s*[^\s]{8,})", re.I)
TODO_RE = re.compile(r"\b(TODO|TBD|FIXME|fill later)\b", re.I)


def lint_text(path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    lower = text.lower()
    for number, line in enumerate(text.splitlines(), start=1):
        if PLACEHOLDER_RE.search(line):
            findings.append(Finding(path, number, "placeholder", "unresolved placeholder"))
        if SECRET_RE.search(line):
            findings.append(Finding(path, number, "secret-like-value", "possible secret or credential"))
        if TODO_RE.search(line):
            findings.append(Finding(path, number, "todo-marker", "unfinished TODO/TBD marker"))

    is_agent_prompt = "agent" in lower and ("execute" in lower or "tool" in lower or "autonomous" in lower)
    has_safety = "safety" in lower or "guardrail" in lower or "do not" in lower
    if is_agent_prompt and not has_safety:
        findings.append(Finding(path, 1, "missing-safety-section", "agent prompt appears to lack safety/guardrail instructions"))
    return findings


def lint_files(paths: Iterable[str | Path]) -> list[Finding]:
    all_findings: list[Finding] = []
    for path in paths:
        p = Path(path)
        if p.is_dir():
            files = sorted(x for x in p.rglob("*") if x.suffix.lower() in {".md", ".txt", ".prompt"})
        else:
            files = [p]
        for file in files:
            text = file.read_text(encoding="utf-8")
            all_findings.extend(lint_text(str(file), text))
    return sorted(all_findings, key=lambda f: (f.path, f.line, f.code))
