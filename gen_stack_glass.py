#!/usr/bin/env python3
"""Generate assets/stack-glass.svg — night-sea tech-stack showcase.

Matches the top banner's theme: watercolor grain and drifting mist over deep
desaturated navy, antique-gold serif headings with wide tracking (like the
TUSHAR wordmark), moonlight pale text and a small crescent moon. The pirate
motifs stay (log-pose compass, kanji chips) but restyled in gold. Pure SVG +
CSS keyframes/SMIL, which GitHub renders (including the animation) inside
README <img> tags. Respects prefers-reduced-motion.
"""
import math
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

GROUP_ACCENTS = ["#C9A86A", "#D9BE85", "#A8823F", "#EAD9AC"]  # antique golds

W = 820
PAD = 28
PILL_H = 32
PILL_GAP = 9
ROW_GAP = 10
LABEL_H = 30
GROUP_GAP = 26
HEADER_H = 54
FONT_SIZE = 13.5
GOLD = "#C9A86A"       # antique gold, like the banner's TUSHAR wordmark
GOLD_HI = "#EAD9AC"    # champagne highlight
GOLD_DEEP = "#8C6F3E"  # deep gold
MOON = "#E8E4D8"       # moonlight pale
INK = "#05080F"        # deep water ink
SERIF = ("'Cinzel, Trajan Pro, Didot, Bodoni MT, Playfair Display, "
         "Georgia, Times New Roman, serif'")

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
0%,100%{filter:drop-shadow(0 0 2px rgba(201,168,106,.08))}
50%{filter:drop-shadow(0 0 5px rgba(201,168,106,.18))}
}
text{font-family:'Segoe UI',system-ui,-apple-system,'Noto Sans CJK JP','Hiragino Sans','Yu Gothic',sans-serif}
text.serif{font-family:'SERIFSTACK'}
@media (prefers-reduced-motion: reduce){.pill{animation:none}}
""".replace("'SERIFSTACK'", SERIF)

def compass_points(cx, cy, r):
    # 8-point compass star; the north spike runs a little longer
    pts = []
    for i in range(16):
        ang = math.pi * i / 8 - math.pi / 2
        rad = r * (1.18 if i == 0 else 1.0 if i % 2 == 0 else 0.34)
        pts.append(f"{cx + rad * math.cos(ang):.1f},{cy + rad * math.sin(ang):.1f}")
    return " ".join(pts)

def crescent(cx, cy, r, opacity=0.9):
    # small crescent moon like the banner's: two circles, evenodd cuts the bite
    bx, by, br = cx + r * 0.42, cy - r * 0.28, r * 0.88
    return (f"<path fill-rule='evenodd' fill='{MOON}' opacity='{opacity}' d='"
            f"M {cx-r:.1f},{cy:.1f} a {r:.1f},{r:.1f} 0 1,0 {2*r:.1f},0 "
            f"a {r:.1f},{r:.1f} 0 1,0 {-2*r:.1f},0 "
            f"M {bx-br:.1f},{by:.1f} a {br:.1f},{br:.1f} 0 1,0 {2*br:.1f},0 "
            f"a {br:.1f},{br:.1f} 0 1,0 {-2*br:.1f},0'/>)")

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">']
parts.append(f"<style>{CSS}</style>")
parts.append("""<defs>
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#151e34"/><stop offset="1" stop-color="#0e1526"/>
</linearGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" stitchTiles="stitch" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0.82  0 0 0 0 0.78  0 0 0 0 0.66  0 0 0 0.06 0"/>
</filter>
<linearGradient id="mist" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#E8E4D8" stop-opacity="0"/>
<stop offset="0.5" stop-color="#9AA3B8" stop-opacity="0.10"/>
<stop offset="1" stop-color="#E8E4D8" stop-opacity="0"/>
</linearGradient>
<radialGradient id="moonglow" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#E8E4D8" stop-opacity="0.15"/>
<stop offset="1" stop-color="#E8E4D8" stop-opacity="0"/>
</radialGradient>
</defs>""")
# frame: watercolor navy, ink border, faint gold inner hairline, grain overlay
parts.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20" fill="url(#panel)" stroke="{INK}" stroke-width="2"/>')
parts.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="20" fill="none" filter="url(#grain)"/>')
parts.append(f'<rect x="6" y="6" width="{W-12}" height="{H-12}" rx="16" fill="none" stroke="{GOLD}" stroke-width="1" opacity="0.28"/>')
# texture: drifting mist bands
parts.append(f'<rect x="40" y="70" width="300" height="60" fill="url(#mist)" opacity="0.5"/>')
parts.append(f'<rect x="{W-360}" y="{H-120}" width="320" height="70" fill="url(#mist)" opacity="0.4"/>')

# header: serif gold title + navy/gold chip + slow-turning log-pose compass + moon
parts.append(f'<text x="{PAD}" y="{PAD+22}" class="serif" font-size="15" fill="{GOLD}" letter-spacing="5">TECH STACK</text>')
chip_w = 2 * 17 + 16
parts.append(f'<rect x="{PAD+158}" y="{PAD+2}" width="{chip_w}" height="26" rx="13" fill="{INK}" stroke="{GOLD}" stroke-width="1" opacity="0.95"/>')
parts.append(f'<text x="{PAD+158+chip_w/2:.0f}" y="{PAD+20}" font-size="14" font-weight="700" fill="{GOLD}" text-anchor="middle">技術</text>')
rcx, rcy, rr = W - PAD - 30, PAD + 16, 21
parts.append(f'<ellipse cx="{rcx-54}" cy="{rcy}" rx="44" ry="34" fill="url(#moonglow)"/>')
parts.append(crescent(rcx - 54, rcy, 10))
parts.append(
    f'<g opacity="0.5"><g>'
    f'<animateTransform attributeName="transform" type="rotate" from="0 {rcx} {rcy}" to="360 {rcx} {rcy}" dur="60s" repeatCount="indefinite"/>'
    f'<circle cx="{rcx}" cy="{rcy}" r="{rr}" fill="none" stroke="{GOLD}" stroke-width="1"/>'
    f'<circle cx="{rcx}" cy="{rcy}" r="{rr*0.66:.1f}" fill="none" stroke="{GOLD}" stroke-width="0.6"/>'
    f'<polygon points="{compass_points(rcx, rcy, rr)}" fill="{GOLD}" opacity="0.85"/>'
    f'<circle cx="{rcx}" cy="{rcy}" r="{rr*0.13:.1f}" fill="#10182B" stroke="{GOLD}" stroke-width="0.8"/>'
    f'</g></g>')

idx = 0
for label, jp, accent, rows, gy, gh in groups_layout:
    # navy/gold kanji chip + serif gold english label + gold beam
    chip_w = len(jp) * 16 + 14
    cy = gy + 9
    parts.append(f'<rect x="{PAD}" y="{cy-9}" width="{chip_w}" height="20" rx="10" fill="{INK}" stroke="{GOLD}" stroke-width="1" opacity="0.95"/>')
    parts.append(f'<text x="{PAD+chip_w/2:.0f}" y="{cy+5}" font-size="12" font-weight="700" fill="{GOLD}" text-anchor="middle">{esc(jp)}</text>')
    parts.append(f'<text x="{PAD+chip_w+12}" y="{cy+5}" class="serif" font-size="12" fill="{GOLD}" letter-spacing="3">{esc(label.upper())}</text>')
    parts.append(f'<rect x="{PAD}" y="{cy+14}" width="44" height="3" rx="1.5" fill="{GOLD}" opacity="0.7"/>')
    for ri, row in enumerate(rows):
        ry = gy + LABEL_H + ri * (PILL_H + ROW_GAP)
        for text, x, w in row:
            delay = -(idx % 12) * (8 / 12)
            parts.append(
                f'<g class="pill" style="animation-delay:{delay:.2f}s">'
                f'<rect x="{x:.0f}" y="{ry}" width="{w:.0f}" height="{PILL_H}" rx="{PILL_H/2}" '
                f'fill="#131B30" stroke="{INK}" stroke-width="1.5"/>'
                f'<rect x="{x+3:.0f}" y="{ry+3}" width="{w-6:.0f}" height="{PILL_H-6}" rx="{(PILL_H-6)/2}" '
                f'fill="none" stroke="{accent}" stroke-width="1" opacity="0.4"/>'
                f'<text x="{x+w/2:.0f}" y="{ry+PILL_H/2+5}" font-size="{FONT_SIZE}" fill="{MOON}" '
                f'text-anchor="middle">{esc(text)}</text></g>'
            )
            idx += 1

parts.append("</svg>")
svg = "\n".join(parts)
open("assets/stack-glass.svg", "w").write(svg)
print(f"wrote assets/stack-glass.svg ({len(svg)//1024}KB, {W}x{H})")
