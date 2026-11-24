"""Validate deep-dive lesson files for the Collegium Alexandrinum.

Usage: python -I validate.py <block_dir> [crash|standard|deep]   (default deep)
Checks block.json and every lesson file in the folder against the Cartographer contract.
Prints problems per file and a summary. Exit code 1 if any file fails.
"""
import json, re, sys
from pathlib import Path

DASHES = ["—", "–"]
BAD_LABEL = re.compile(r'[\[\(\{]([^\]\)\}]*)[\]\)\}]')


def words(s):
    return len(re.findall(r"\b\w+\b", s or ""))


def check_mermaid(src, where, probs):
    if not src:
        return
    first = src.strip().split("\n", 1)[0].strip()
    if not re.match(r"^(flowchart|graph|sequenceDiagram|timeline|stateDiagram|classDiagram)", first):
        probs.append(f"{where}: diagram must start with flowchart/graph/sequenceDiagram/timeline")
    if "```" in src:
        probs.append(f"{where}: diagram must not include code fences")
    if len(re.findall(r"-->|->>|-->>|---", src)) > 16:
        probs.append(f"{where}: diagram too busy (over 16 links)")
    for m in BAD_LABEL.finditer(src):
        inner = m.group(1)
        if any(ch in inner for ch in ['"', ":", ";", "(", ")", "[", "]", "{", "}"]):
            probs.append(f"{where}: diagram label has a risky character: {inner[:40]!r}")
            break


RULES = {"crash": (3, 0, 1), "standard": (4, 1, 2), "deep": (5, 2, 3)}  # min sections, min diagrams, min checks
DEPTH = "deep"


def check_lesson(p, data, probs):
    min_secs, min_diag, min_checks = RULES[DEPTH]
    for k in ["order", "title", "minutes", "objective", "sections", "field", "key_points", "terms", "sources", "practice", "quiz"]:
        if k not in data:
            probs.append(f"missing field {k}")
    secs = data.get("sections") or []
    if not (min_secs <= len(secs) <= 14):
        probs.append(f"{len(secs)} sections (minimum {min_secs} for {DEPTH})")
    total = 0
    diagrams = 0
    checks = 0
    for i, s in enumerate(secs):
        if not s.get("h") or not s.get("md"):
            probs.append(f"section {i+1}: needs h and md")
        total += words(s.get("md"))
        if s.get("check"):
            checks += 1
            if not s["check"].get("q") or not s["check"].get("a"):
                probs.append(f"section {i+1}: check needs q and a")
        if s.get("diagram"):
            diagrams += 1
            check_mermaid(s["diagram"], f"section {i+1}", probs)
    f = data.get("field") or {}
    total += words(f.get("client")) + words(f.get("talk"))
    mins = data.get("minutes") or 20
    want = int(mins * 110)
    if total < want:
        probs.append(f"only {total} words for a {mins}-minute lesson (want at least {want})")
    if diagrams < min_diag:
        probs.append(f"{diagrams} diagrams (want at least {min_diag} for {DEPTH})")
    if checks < max(min_checks, len(secs) // 2):
        probs.append(f"{checks} check-yourself questions (want most sections)")
    if not f.get("client") or not f.get("talk"):
        probs.append("field needs client and talk")
    if len(data.get("key_points") or []) < 5:
        probs.append("fewer than 5 key_points")
    if len(data.get("sources") or []) < 3:
        probs.append("fewer than 3 sources")
    for s in data.get("sources") or []:
        if not s.get("title") or not s.get("date"):
            probs.append("a source is missing title or date")
            break
    pr = data.get("practice") or {}
    if not pr.get("prompt") or not pr.get("answer_guide"):
        probs.append("practice needs prompt and answer_guide")
    q = data.get("quiz") or []
    if len(q) != 4:
        probs.append(f"quiz has {len(q)} questions (want 4)")
    if sum(1 for x in q if x.get("type") == "mc") != 2:
        probs.append("quiz wants exactly 2 mc and 2 short")
    for x in q:
        for k in ["id", "rung", "type", "q", "answer", "why", "concept"]:
            if not x.get(k):
                probs.append(f"quiz {x.get('id')}: missing {k}")
        if x.get("type") == "mc":
            ch = x.get("choices") or []
            if len(ch) != 4:
                probs.append(f"quiz {x.get('id')}: mc needs 4 choices")
            if x.get("answer") not in ch:
                probs.append(f"quiz {x.get('id')}: answer must exactly equal one choice")
    return total


def main(d):
    d = Path(d)
    bad = 0
    files = sorted(d.glob("*.json"))
    if not (d / "block.json").exists():
        print("MISSING block.json")
        bad += 1
    for p in files:
        probs = []
        raw = p.read_text(encoding="utf-8")
        for ch in DASHES:
            if ch in raw:
                probs.append(f"contains {'em' if ch == DASHES[0] else 'en'} dash characters ({raw.count(ch)})")
        try:
            data = json.loads(raw)
        except Exception as e:
            print(f"FAIL {p.name}: invalid JSON: {e}")
            bad += 1
            continue
        info = ""
        if p.name == "block.json":
            for k in ["order", "title", "why", "objective", "builds_on", "lessons", "pack"]:
                if k not in data:
                    probs.append(f"missing field {k}")
            pk = data.get("pack") or {}
            if len(pk.get("key_points") or []) < 8:
                probs.append("pack wants 8-14 key_points")
            ids = {l.get("id") for l in data.get("lessons") or []}
            for lid in ids:
                if not (d / f"{lid}.json").exists():
                    probs.append(f"lesson file {lid}.json not found")
        else:
            info = f"{check_lesson(p, data, probs)} words"
        if probs:
            bad += 1
            print(f"FAIL {p.name} {info}")
            for x in probs:
                print("   -", x)
        else:
            print(f"ok   {p.name} {info}")
    print("RESULT:", "PASS" if not bad else f"{bad} file(s) need fixing")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        DEPTH = sys.argv[2]
    main(sys.argv[1])
