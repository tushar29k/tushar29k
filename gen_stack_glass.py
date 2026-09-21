#!/usr/bin/env python3
"""Generate assets/stack-glass.svg — anime-themed tech-stack showcase.

Manga-panel card on the night-sea navy base: ink-bordered pills with a slow
subtle glow, red hanko-style kanji chips per group (忍法 / 探索 / 武器 / 心構え),
a small rising sun, halftone dots and thin speedlines. Pure SVG + CSS
keyframes, which GitHub renders (including the animation) inside README
<img> tags. Respects prefers-reduced-motion.
"""
from PIL import ImageFont

GROUPS = [
    ("LLM & Agents", "忍法", ["LangChain", "LangGraph", "Google ADK", "LlamaIndex", "AutoGen",
                              "CrewAI", "MCP", "OpenAI API", "Anthropic API", "Gemini API",
                              "Azure OpenAI", "Hugging Face", "Transformers", "vLLM", "Ollama"]),
    ("Retrieval & Data", "探索", ["Azure AI Search", "Pinecone", "Qdrant", "Weaviate", "Milvus",
                                 "pgvector", "FAISS", "Elasticsearch", "Embeddings",
                                 "Hybrid retrieval", "Reranking", "SQL", "Pandas", "NumPy"]),
    ("Serving & MLOps", "武器", ["Python", "FastAPI", "Uvicorn", "Docker", "Kubernetes",
                                 "GitHub Actions", "Pytest", "Pydantic", "REST APIs", "Linux",
                                 "Git", "MLflow", "Weights & Biases"]),
    ("Practices", "心構え", ["Eval-driven development", "RAG evals", "Prompt engineering",
                             "Structured extraction", "LLM-as-judge", "ReAct workflows",
                             "Guardrails"]),
]

GROUP_ACCENTS = ["#22D3EE", "#2DD4BF", "#A78BFA", "#F472B6"]  # cyan/teal/violet/pink

W = 820
PAD = 28
PILL_H = 32
PILL_GAP = 9
ROW_GAP = 10
LABEL_H = 30
GROUP_GAP = 26
HEADER_H = 54
FONT_SIZE = 13.5
RED = "#E63946"
PAPER = "#F5F2E9"
INK = "#04080F"

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(FONT_SIZE))
    label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
except OSError:
    font = ImageFont.load_default()
    label_font = font

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def text_w(t, f=font):
    bb = f.getbbox(t)
    return bb[2] - bb[0]

# flow layout (same mechanics as before; header block sits above group 1)
groups_layout = []  # (label, jp, accent, rows:[[(text, x, w)...]], y, height)
y = PAD + HEADER_H
for gi, (label, jp, items) in enumerate(GROUPS):
    rows, cur, cx = [], [], PAD
    max_w = W - 2 * PAD
    for it in items:
        w = text_w(it) + 30  # horizontal padding
        if cx + w > PAD + max_w and cur:
            rows.append(cur); cur = []; cx = PAD
        cur.append((it, cx, w)); cx += w + PILL_GAP
    if cur:
        rows.append(cur)
    gh = LABEL_H + len(rows) * PILL_H + (len(rows) - 1) * ROW_GAP
    groups_layout.append((label, jp, GROUP_ACCENTS[gi % len(GROUP_ACCENTS)], rows, y, gh))
    y += gh + GROUP_GAP
H = int(y - GROUP_GAP + PAD)

CSS = """
.pill{animation:pillGlow 12s ease-in-out infinite}
@keyframes pillGlow{
0%,100%{filter:drop-shadow(0 0 2px rgba(139,152,169,.10))}
50%{filter:drop-shadow(0 0 5px rgba(139,152,169,.22))}
}
.beam{animation:beamFlow 12s ease-in-out infinite}
@keyframes beamFlow{0%,100%{stop-color:#38bdf8}50%{stop-color:#2dd4bf}}
.sun{animation:sunPulse 9s ease-in-out infinite}
@keyframes sunPulse{0%,100%{opacity:.75}50%{opacity:.45}}
text{font-family:'Segoe UI',system-ui,-apple-system,'Noto Sans CJK JP','Hiragino Sans','Yu Gothic',sans-serif}
@media (prefers-reduced-motion: reduce){.pill,.beam,.sun{animation:none}}
"""

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">']
parts.append(f"<style>{CSS}</style>")
parts.append("""<defs>
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#101d33"/><stop offset="1" stop-color="#0a1424"/>
</linearGradient>
<pattern id="halftone" width="9" height="9" patternUnits="userSpaceOnUse">
<circle cx="4.5" cy="4.5" r="1.25" fill="#8b98a9" opacity="0.16"/>
</pattern>
<radialGradient id="sunGlow" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#E63946" stop-opacity="0.5"/>
<stop offset="1" stop-color="#E63946" stop-opacity="0"/>
</radialGradient>
</defs>""")
# manga panel frame: navy fill, ink border, inner hairline
parts.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20" fill="url(#panel)" stroke="{INK}" stroke-width="2"/>')
parts.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="none" stroke="#182742" stroke-width="1"/>')
# manga texture: halftone corners + faint speedlines + rising sun by the header
parts.append(f'<rect x="{W-180}" y="8" width="172" height="86" fill="url(#halftone)"/>')
parts.append(f'<rect x="8" y="{H-94}" width="150" height="86" fill="url(#halftone)" opacity="0.5"/>')
for i in range(5):
    x = W - 60 - i * 16
    parts.append(f'<line x1="{x}" y1="{H-18}" x2="{x-46}" y2="{H-64}" stroke="#8b98a9" stroke-width="2" stroke-linecap="round" opacity="0.07"/>')

# header: title + hanko chip + rising sun
parts.append(f'<text x="{PAD}" y="{PAD+22}" font-size="14" font-weight="700" fill="#22d3ee" letter-spacing="4">TECH STACK</text>')
chip_w = 2 * 17 + 16
parts.append(f'<rect x="{PAD+150}" y="{PAD+2}" width="{chip_w}" height="26" rx="13" fill="{RED}" opacity="0.92"/>')
parts.append(f'<text x="{PAD+150+chip_w/2:.0f}" y="{PAD+20}" font-size="14" font-weight="700" fill="{PAPER}" text-anchor="middle">技術</text>')
parts.append(f'<g class="sun"><circle cx="{W-PAD-24}" cy="{PAD+14}" r="30" fill="url(#sunGlow)"/><circle cx="{W-PAD-24}" cy="{PAD+14}" r="14" fill="{RED}" opacity="0.8"/></g>')

idx = 0
for label, jp, accent, rows, gy, gh in groups_layout:
    # hanko kanji chip + english label + animated beam
    chip_w = len(jp) * 16 + 14
    cy = gy + 9
    parts.append(f'<rect x="{PAD}" y="{cy-9}" width="{chip_w}" height="20" rx="10" fill="{RED}" opacity="0.92"/>')
    parts.append(f'<text x="{PAD+chip_w/2:.0f}" y="{cy+5}" font-size="12" font-weight="700" fill="{PAPER}" text-anchor="middle">{esc(jp)}</text>')
    parts.append(f'<text x="{PAD+chip_w+12}" y="{cy+5}" font-size="12" font-weight="700" fill="#8b98b8" letter-spacing="3">{esc(label.upper())}</text>')
    parts.append(f'<rect class="beam" x="{PAD}" y="{cy+14}" width="44" height="3" rx="1.5" fill="#22d3ee"/>')
    for ri, row in enumerate(rows):
        ry = gy + LABEL_H + ri * (PILL_H + ROW_GAP)
        for text, x, w in row:
            delay = -(idx % 12) * (8 / 12)
            parts.append(
                f'<g class="pill" style="animation-delay:{delay:.2f}s">'
                f'<rect x="{x:.0f}" y="{ry}" width="{w:.0f}" height="{PILL_H}" rx="{PILL_H/2}" '
                f'fill="#0c1626" stroke="{INK}" stroke-width="1.5"/>'
                f'<rect x="{x+3:.0f}" y="{ry+3}" width="{w-6:.0f}" height="{PILL_H-6}" rx="{(PILL_H-6)/2}" '
                f'fill="none" stroke="{accent}" stroke-width="1" opacity="0.45"/>'
                f'<text x="{x+w/2:.0f}" y="{ry+PILL_H/2+5}" font-size="{FONT_SIZE}" fill="#eaf2ff" '
                f'text-anchor="middle">{esc(text)}</text></g>'
            )
            idx += 1

parts.append("</svg>")
svg = "\n".join(parts)
open("assets/stack-glass.svg", "w").write(svg)
print(f"wrote assets/stack-glass.svg ({len(svg)//1024}KB, {W}x{H})")
