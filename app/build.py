"""Build app/index.html from app/index.src.html.

The agents/*.md specs are the source of truth for what each agent does. This script
copies them into the page as JSON, inlines the crest image, and fills in the live
artifact URL (from app/url.txt, if present). Re-run after editing any agent spec:
    python build.py
Then republish app/index.html to the same artifact.
"""
import base64
import json
from pathlib import Path

HERE = Path(__file__).parent
AGENTS_DIR = HERE.parent / "agents"
SRC = HERE / "index.src.html"
OUT = HERE / "index.html"
START, END = "<!--AGENTS-->", "<!--/AGENTS-->"

agents = {p.stem: p.read_text(encoding="utf-8") for p in sorted(AGENTS_DIR.glob("*.md"))}
blob = json.dumps(agents, ensure_ascii=False).replace("</", "<\\/")  # never close the script tag early

html = SRC.read_text(encoding="utf-8")
a, b = html.index(START) + len(START), html.index(END)
html = html[:a] + f'\n<script type="application/json" id="agents">{blob}</script>\n' + html[b:]

crest = base64.b64encode((HERE / "crest.jpg").read_bytes()).decode()
html = html.replace("__CREST__", f"data:image/jpeg;base64,{crest}")

url_file = HERE / "url.txt"
url = url_file.read_text(encoding="utf-8").strip() if url_file.exists() else ""
if url:
    html = html.replace("__APP_URL__", url)

OUT.write_text(html, encoding="utf-8", newline="")
print(f"Built {OUT.name}: {len(agents)} agents, {OUT.stat().st_size // 1024} KB, url={'set' if url else 'not set'}")
