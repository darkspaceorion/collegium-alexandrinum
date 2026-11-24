"""Free fact check for Collegium lessons. No AI, no tokens.

Usage: python -I factcheck.py <block_dir> <scout_file>
Pulls every hard fact out of each lesson (years, prices, percentages, big numbers,
version names like GPT-4o or Claude 3.5) and flags the ones that do not appear in the
block's scout notes. Writes <block_dir>/facts.txt and prints a one-line summary.
A flag is not an error: it is a line for the checker agent to verify at the source.
Skipped on purpose: markdown table rows, quiz questions, and sentences marked as made-up
examples ("for example", "say", "imagine", "invented"...). Writers label invented numbers.
"""
import json, re, sys
from pathlib import Path

YEAR = re.compile(r"\b(1[89]\d\d|20\d\d)\b")
MONEY = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?\s?(?:k|m|bn|million|billion)?", re.I)
PCT = re.compile(r"\b\d+(?:\.\d+)?\s?(?:%|percent)")
BIG = re.compile(r"(?<![.\d])\b\d{1,3}(?:,\d{3})+\b|(?<![.\d])\b(?!1[89]\d\d\b|20\d\d\b)\d{3,}\b|\b\d+(?:\.\d+)?\s?(?:million|billion|trillion)\b")
VERSION = re.compile(r"\b[A-Z][A-Za-z]*-\d+(?:\.\d+)?[a-z]*\b|\b[A-Z][A-Za-z]+ \d+\.\d+\b|\b[A-Z][A-Za-z]+-?\d+[a-z]+\b")  # GPT-4o, Claude 3.5, Llama-3
SKIP_VERSION = re.compile(r"^(Block|Lesson|Step|Section|Level|Rung|Week|Day|Option|Phase|Part|Table|Figure|Q)\b", re.I)
ILLUSTRATIVE = re.compile(r"\b(for example|e\.g\.|say|suppose|imagine|picture|invented|illustrat\w*|made-up|hypothetical|pretend|toy|worked example|if a|a client|your client)\b", re.I)


def sentences(text):
    """Split into sentences, dropping markdown table rows (worked examples)."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)  # code blocks
    text = re.sub(r"`[^`]*`", " ", text)                 # inline code
    keep = "\n".join(l for l in text.split("\n") if not l.lstrip().startswith(("|", "{", "}", '"')))
    return re.split(r"(?<=[.!?])\s+|\n+", keep)


def norm(s):
    return re.sub(r"[\s,$]", "", s.lower()).replace("percent", "%")


def texts(lesson):
    for s in lesson.get("sections") or []:
        yield s.get("h", ""), s.get("md", "")
        if s.get("check"):
            yield s.get("h", ""), s["check"].get("q", "") + " " + s["check"].get("a", "")
    f = lesson.get("field") or {}
    yield "field", (f.get("client") or "") + "\n" + (f.get("talk") or "")
    yield "key points", "\n".join(lesson.get("key_points") or [])


def facts_in(text):
    found = []
    for rx in (MONEY, PCT, BIG, YEAR):
        found += [m.group(1) if rx is YEAR else m.group(0) for m in rx.finditer(text)]
    found += [m.group(0) for m in VERSION.finditer(text) if not SKIP_VERSION.match(m.group(0))]
    return found


def main(block_dir, scout_file):
    d = Path(block_dir)
    known = norm(Path(scout_file).read_text(encoding="utf-8"))
    out, total, flagged = [], 0, 0
    for p in sorted(d.glob("l*.json")):
        lesson = json.loads(p.read_text(encoding="utf-8"))
        seen, lines = set(), []
        for where, text in texts(lesson):
            for sent in sentences(text):
                if ILLUSTRATIVE.search(sent):
                    continue
                for fact in facts_in(sent):
                    key = norm(fact)
                    if key in seen:
                        continue
                    seen.add(key)
                    total += 1
                    if key not in known:
                        flagged += 1
                        lines.append(f"  [{where}] {fact}  ::  {sent.strip()[:240]}")
        if lines:
            out.append(f"{p.name}: {len(lines)} unsupported")
            out += lines
    (d / "facts.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{d.name}: {total} facts checked, {flagged} not in scout notes -> {d / 'facts.txt'}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
