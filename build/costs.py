"""Record what a Collegium build cost, from the Claude Code session logs. No AI, no tokens.

Usage: python -I costs.py <out.json> [session_id] [--since ISO-time]
Reads ~/.claude/projects/<NEXUS project>/<session>.jsonl and its subagents/ folder.
With no session_id it takes the newest session. --since counts only calls after that
time (use the build's start time so earlier chat in the session is left out).
Writes per-role totals (main thread, scouts, writers, checkers, failed agents) and prints a summary.
"Read" is all context fed to the model across calls (mostly cached, still counts toward plan limits).
"""
import json, os, sys
from pathlib import Path

PROJ = Path(os.environ.get("CLAUDE_PROJECT_LOGS", Path.home() / ".claude" / "projects" / "<your-project>"))


def calls(f, since):
    seen = {}
    for line in open(f, encoding="utf-8"):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if o.get("type") != "assistant" or (since and o.get("timestamp", "") < since):
            continue
        m = o.get("message") or {}
        u = m.get("usage") or {}
        seen[m.get("id")] = {
            "model": m.get("model", "?"),
            "read": u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0),
            "out": u.get("output_tokens", 0),
        }
    return list(seen.values())


def first_prompt(f):
    for line in open(f, encoding="utf-8"):
        o = json.loads(line)
        if o.get("type") == "user":
            c = o["message"].get("content")
            return c if isinstance(c, str) else json.dumps(c)
    return ""


def role(prompt, models):
    p = prompt.lower()
    if "<synthetic>" in models and len(models) <= 2:
        return "failed"
    if "fact check" in p or "facts.txt" in p:
        return "checkers"
    if any("haiku" in m for m in models):
        return "scouts"  # scouts are the only other Haiku agents
    if any("sonnet" in m for m in models):
        return "writers"
    return "other agents"


def main():
    args = sys.argv[1:]
    since = None
    if "--since" in args:
        i = args.index("--since"); since = args[i + 1]; del args[i:i + 2]
    out = Path(args[0])
    if len(args) > 1:
        main_f = PROJ / f"{args[1]}.jsonl"
    else:
        main_f = max(PROJ.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    roles = {}

    def add(name, cs, agent=False):
        r = roles.setdefault(name, {"agents": 0, "calls": 0, "read": 0, "out": 0, "models": set(), "peak_context": 0})
        r["agents"] += 1 if agent else 0
        r["calls"] += len(cs)
        r["read"] += sum(c["read"] for c in cs)
        r["out"] += sum(c["out"] for c in cs)
        r["models"] |= {c["model"] for c in cs}
        r["peak_context"] = max([r["peak_context"]] + [c["read"] for c in cs])

    add("main thread", calls(main_f, since))
    sub = main_f.with_suffix("") / "subagents"
    for f in sorted(sub.glob("*.jsonl")) if sub.exists() else []:
        cs = calls(f, since)
        if not cs:
            continue
        meta = f.with_suffix(".meta.json")
        kind = json.loads(meta.read_text(encoding="utf-8")).get("agentType", "") if meta.exists() else ""
        if kind.startswith("collegium-") and "<synthetic>" not in {c["model"] for c in cs}:
            add(kind.replace("collegium-", "") + "s", cs, agent=True)  # scouts / writers / checkers
        else:
            add(role(first_prompt(f), {c["model"] for c in cs}), cs, agent=True)
    for r in roles.values():
        r["models"] = sorted(r["models"])
    rec = {"session": main_f.stem, "since": since, "roles": roles,
           "total_read": sum(r["read"] for r in roles.values())}
    out.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    for k, r in roles.items():
        print(f"{k:13} agents {r['agents']:3}  calls {r['calls']:4}  read {r['read']/1e6:6.1f}M  peak ctx {r['peak_context']//1000}k  {','.join(r['models'])}")
    print(f"TOTAL read {rec['total_read']/1e6:.1f}M -> {out}")


if __name__ == "__main__":
    main()
