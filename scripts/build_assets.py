#!/usr/bin/env python3
"""Build the animated SVG panels used by the profile README.

Numbers come from the Mango matched comparison (202 questions + 12 agent cases per
configuration, weighted to social/EQ 30, cyber 20, coding 10, agentic 30, instructions 5,
general 5). Re-run after a new graded cohort:

    python3 scripts/build_assets.py [path/to/comparison.json]

Without an argument it uses the snapshot embedded below.
"""
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

BG = "#0d1117"
PANEL = "#111823"
LINE = "#223044"
TEXT = "#e6edf3"
MUTED = "#8b98a9"
CYAN = "#7EE0FF"
MANGO = "#FFB547"
CORAL = "#FF7A59"
VIOLET = "#B69CFF"
MONO = "JetBrains Mono, SFMono-Regular, ui-monospace, Menlo, Consolas, monospace"
SANS = "Inter, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"

# label -> (display name, quant/runtime, family colour)
NAMES = {
    "qwen38-flashnext-iq4xs": ("Qwen3.8 Flash Next", "IQ4_XS", CYAN),
    "qwen38-flashnext-orca-iq4xs-32k": ("Flash Next (Orca)", "IQ4_XS · 32K", CYAN),
    "deepseek41-gsq-iq2xs": ("DeepSeek V4.1 Flash", "GSQ IQ2_XS · Strata", VIOLET),
    "glm53flash-mixed-32k": ("GLM 5.3 Flash", "mixed IQ2/IQ3", MANGO),
    "qwen35-122b-q4": ("Qwen3.5 122B A10B", "Q4", CYAN),
    "qwen27-mlx4-tf-medium": ("Qwen3.8 27B", "MLX 4-bit + DFlash2", CYAN),
    "mimo26-flash-q3km": ("MiMo V2.6 Flash", "Q3_K_M", CORAL),
    "glm53flash-bolding-iq2xxs-32k-high": ("GLM 5.3 Flash (Bolding)", "IQ2_XXS", MANGO),
    "glm53flash-orca-q2k-32k-high": ("GLM 5.3 Flash (Orca)", "Q2_K", MANGO),
    "qwen27-cyber-iq4xs-mtp": ("Qwen3.8 27B Cyber", "IQ4_XS + MTP", CYAN),
    "nanbeige43-33b-q6k": ("Nanbeige 4.3 33B", "Q6_K", CORAL),
    "qwen27-cyber-q6k": ("Qwen3.8 27B Cyber v2", "Q6_K + Q8 MTP", CYAN),
}

DOMAINS = [
    ("social_eq", "Social / EQ"),
    ("cyber", "Cyber"),
    ("agentic", "Agentic"),
    ("coding", "Coding"),
    ("instructions", "Instr."),
    ("general", "General"),
]

# Snapshot of comparison.json rows (quality, workload minutes, domain scores), 2026-10-30.
SNAPSHOT = [
    ("qwen38-flashnext-iq4xs", 84.187, 35.33, [74.41, 83.33, 88.75, 95.0, 85.0, 96.43]),
    ("qwen38-flashnext-orca-iq4xs-32k", 83.417, 37.36, [71.15, 85.0, 87.5, 95.0, 90.0, 96.43]),
    ("deepseek41-gsq-iq2xs", 83.188, 71.43, [74.98, 87.22, 85.0, 85.0, 95.0, 90.0]),
    ("glm53flash-mixed-32k", 82.547, 27.49, [77.10, 81.11, 86.25, 90.0, 70.0, 96.43]),
    ("qwen35-122b-q4", 80.720, 120.76, [71.19, 83.33, 79.58, 90.0, 100.0, 96.43]),
    ("qwen27-mlx4-tf-medium", 80.645, 23.98, [69.68, 86.11, 83.75, 85.0, 95.0, 82.86]),
    ("mimo26-flash-q3km", 79.392, 220.28, [65.47, 85.0, 82.5, 90.0, 90.0, 90.0]),
    ("glm53flash-bolding-iq2xxs-32k-high", 79.107, 40.98, [70.34, 85.56, 85.0, 85.0, 65.0, 72.86]),
    ("glm53flash-orca-q2k-32k-high", 75.642, 54.76, [68.60, 81.11, 78.75, 80.0, 65.0, 79.29]),
    ("qwen27-cyber-iq4xs-mtp", 70.271, 29.74, [43.83, 82.22, 85.0, 85.0, 55.0, 78.57]),
    ("nanbeige43-33b-q6k", 67.456, 175.31, [54.52, 78.89, 61.67, 85.0, 80.0, 86.43]),
    ("qwen27-cyber-q6k", 66.982, 45.60, [38.68, 75.56, 83.75, 85.0, 70.0, 62.86]),
]
PICK = "qwen38-flashnext-iq4xs"
PARETO = {"qwen38-flashnext-iq4xs", "glm53flash-mixed-32k", "qwen27-mlx4-tf-medium"}


def load_rows(path):
    if not path:
        return SNAPSHOT
    data = json.loads(Path(path).read_text())
    global PICK, PARETO
    PICK = data.get("default_under_rule", PICK)
    PARETO = set(data.get("pareto", PARETO))
    rows = []
    for r in data["rows"]:
        rows.append((r["label"], r["quality"], r["workload_minutes"],
                     [r["domains"][k] for k, _ in DOMAINS]))
    return sorted(rows, key=lambda r: -r[1])


def svg(w, h, body, defs="", style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img">\n<defs>{defs}</defs>\n'
            f'<style>{style}</style>\n{body}\n</svg>\n')


def t(x, y, s, size=13, fill=TEXT, weight=400, anchor="start", family=SANS, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def frame(w, h, r=18, fill=BG):
    return (f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="{fill}" '
            f'stroke="url(#edge)" stroke-width="1"/>')


EDGE = (f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".55"/>'
        f'<stop offset=".5" stop-color="{LINE}"/>'
        f'<stop offset="1" stop-color="{MANGO}" stop-opacity=".55"/></linearGradient>')


# ---------------------------------------------------------------- hero banner
def hero():
    w, h = 1200, 300
    defs = EDGE + f"""
<radialGradient id="orbA" cx="50%" cy="50%" r="50%">
  <stop offset="0" stop-color="{CYAN}" stop-opacity=".38"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="orbB" cx="50%" cy="50%" r="50%">
  <stop offset="0" stop-color="{MANGO}" stop-opacity=".30"/><stop offset="1" stop-color="{MANGO}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="title" x1="0" x2="1">
  <stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="#E9F7FF"/><stop offset="1" stop-color="{MANGO}"/>
</linearGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
  <path d="M28 0H0V28" fill="none" stroke="{LINE}" stroke-width=".6"/>
</pattern>
<linearGradient id="sweep" x1="0" x2="1">
  <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".07"/>
  <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
</linearGradient>
<clipPath id="clip"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18"/></clipPath>
<linearGradient id="fade" x1="0" x2="1">
  <stop offset="0" stop-color="{BG}" stop-opacity=".2"/><stop offset=".5" stop-color="{BG}" stop-opacity=".85"/>
  <stop offset="1" stop-color="{BG}" stop-opacity=".2"/>
</linearGradient>"""
    style = """
.orbA{animation:driftA 14s ease-in-out infinite alternate}
.orbB{animation:driftB 17s ease-in-out infinite alternate}
@keyframes driftA{from{transform:translate(0,0)}to{transform:translate(160px,40px)}}
@keyframes driftB{from{transform:translate(0,0)}to{transform:translate(-180px,-30px)}}
.pulse{animation:pulse 3.2s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.25}50%{opacity:1}}
.scan{animation:scan 6s linear infinite}
@keyframes scan{from{transform:translateX(-300px)}to{transform:translateX(1300px)}}
.cursor{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.flow{stroke-dasharray:4 10;animation:flow 1.6s linear infinite}
@keyframes flow{to{stroke-dashoffset:-28}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""
    # constellation of nodes on the right (agents -> router -> GPU)
    nodes = [(820, 70), (900, 120), (980, 80), (1060, 140), (940, 200), (1100, 220), (860, 230), (1030, 250)]
    links = [(0, 1), (1, 2), (2, 3), (1, 4), (4, 6), (4, 3), (3, 5), (4, 7), (7, 5)]
    g = []
    for a, b in links:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-opacity=".35" class="flow"/>')
    for i, (x, y) in enumerate(nodes):
        c = MANGO if i in (3, 4) else CYAN
        g.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}" fill-opacity=".12"/>'
                 f'<circle cx="{x}" cy="{y}" r="3.2" fill="{c}" class="pulse" style="animation-delay:{i*0.37:.2f}s"/>')
    body = f"""
<g clip-path="url(#clip)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#grid)" opacity=".55"/>
  <circle class="orbA" cx="250" cy="90" r="260" fill="url(#orbA)"/>
  <circle class="orbB" cx="980" cy="230" r="280" fill="url(#orbB)"/>
  <rect width="{w}" height="{h}" fill="url(#fade)"/>
  {''.join(g)}
  <rect class="scan" x="0" y="0" width="220" height="{h}" fill="url(#sweep)"/>
</g>
{frame(w, h, fill="none")}
{t(64, 92, "~/isilicon $ whoami", 15, MUTED, 500, family=MONO)}
<rect class="cursor" x="262" y="80" width="9" height="16" fill="{CYAN}"/>
{t(60, 168, "isilicon", 76, "url(#title)", 700, family=MONO, extra='letter-spacing="-2"')}
{t(64, 212, "Security engineer building things that fail closed.", 20, TEXT, 500)}
{t(64, 244, "embedded + FIDO2  ·  AI red teaming  ·  computer-use agents  ·  self-hosted LLM fleet", 15, MUTED, 400, family=MONO)}
"""
    return svg(w, h, body, defs, style)


# ---------------------------------------------------------------- stat tiles
def stats():
    w, h = 1200, 168
    tiles = [
        ("12", "model configs", "graded on one matched screen", CYAN),
        ("3,232", "per-question grades", "Wilson CIs · paired bootstrap", MANGO),
        ("24", "public HF repos", "exact quants + cards", CYAN),
        ("~1.19 TB", "weights preserved", "HF mirrors + torrents", MANGO),
        ("96 GB", "one RTX PRO 6000", "Blackwell · single GPU", CYAN),
    ]
    tw, gap, x0 = 216, 18, 24
    style = """
.tile{opacity:0;animation:rise .9s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.glow{animation:glow 4s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:.9}}
@media (prefers-reduced-motion: reduce){*{animation:none!important;opacity:1!important}}
"""
    parts = [frame(w, h)]
    for i, (big, label, sub, c) in enumerate(tiles):
        x = x0 + i * (tw + gap)
        parts.append(
            f'<g class="tile" style="animation-delay:{0.12*i:.2f}s">'
            f'<rect x="{x}" y="24" width="{tw}" height="120" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
            f'<rect class="glow" x="{x+18}" y="24" width="56" height="2.5" rx="1" fill="{c}" style="animation-delay:{0.5*i:.1f}s"/>'
            + t(x + 18, 80, big, 34, c, 700, family=MONO)
            + t(x + 18, 108, label, 14, TEXT, 600)
            + t(x + 18, 128, sub, 11.5, MUTED, 400)
            + '</g>')
    return svg(w, h, "\n".join(parts), EDGE, style)


# ---------------------------------------------------------------- architecture
def architecture():
    w, h = 1200, 470
    style = """
.flow{stroke-dasharray:6 9;animation:flow 1.2s linear infinite}
.flow.slow{animation-duration:2.4s}
@keyframes flow{to{stroke-dashoffset:-30}}
.blip{animation:blip 2.4s ease-in-out infinite}
@keyframes blip{0%,100%{opacity:.35}50%{opacity:1}}
.lease{animation:lease 6s ease-in-out infinite}
@keyframes lease{0%,30%{opacity:1}36%,94%{opacity:.25}100%{opacity:1}}
.lease2{animation:lease2 6s ease-in-out infinite}
@keyframes lease2{0%,30%{opacity:.25}36%,62%{opacity:1}68%,100%{opacity:.25}}
.lease3{animation:lease3 6s ease-in-out infinite}
@keyframes lease3{0%,62%{opacity:.25}68%,94%{opacity:1}100%{opacity:.25}}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
"""
    defs = EDGE + f"""
<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M0 0L10 5L0 10z" fill="{CYAN}"/></marker>
<marker id="arrM" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
  <path d="M0 0L10 5L0 10z" fill="{MANGO}"/></marker>"""

    def box(x, y, bw, bh, title, lines, c=CYAN, cls=""):
        out = [f'<g class="{cls}"><rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="12" fill="{PANEL}" stroke="{c}" stroke-opacity=".55"/>',
               f'<circle cx="{x+16}" cy="{y+20}" r="3.5" fill="{c}" class="blip"/>',
               t(x + 28, y + 25, title, 14, TEXT, 700)]
        for i, ln in enumerate(lines):
            out.append(t(x + 16, y + 48 + i * 18, ln, 11.5, MUTED, 400, family=MONO))
        out.append("</g>")
        return "".join(out)

    def wire(x1, y1, x2, y2, c=CYAN, slow=False, marker="arr"):
        return (f'<path d="M{x1} {y1} C{(x1+x2)/2} {y1} {(x1+x2)/2} {y2} {x2} {y2}" fill="none" '
                f'stroke="{c}" stroke-width="1.6" stroke-opacity=".8" class="flow{" slow" if slow else ""}" marker-end="url(#{marker})"/>')

    p = [frame(w, h)]
    p.append(t(28, 40, "MANGO · SERVING PATH", 12, CYAN, 700, family=MONO, extra='letter-spacing="2"'))
    p.append(t(1172, 40, "one asyncio process · OpenAI-compatible · streaming SSE", 12, MUTED, 400, "end", MONO))

    p.append(box(28, 70, 190, 104, "Agents", ["Hermes agent", "scripts / tools", "any OpenAI client"]))
    p.append(box(258, 88, 150, 68, "HTTPS tunnel", ["ngrok · API keys"]))
    p.append(box(448, 62, 330, 228, "mango-server", [
        "auth · aliases (auto/fast/vision)",
        "profile lease: drain → switch",
        "elastic context tiers ↑ grow ↓ shrink",
        "reasoning-effort mapping",
        "vendor sampling defaults",
        "thinking always on · no token caps",
        "maintenance pin for benchmarks",
        "content-free telemetry v2",
    ], MANGO))
    p.append(box(818, 62, 170, 64, "TensorFold", ["MLX 4-bit + DFlash2"], CYAN, "lease"))
    p.append(box(818, 144, 170, 64, "Strata", ["GSQ + hot experts"], VIOLET, "lease2"))
    p.append(box(818, 226, 170, 64, "llama.cpp", ["GGUF · MTP · --fit"], CORAL, "lease3"))
    p.append(box(1024, 118, 148, 116, "RTX PRO 6000", ["96 GB Blackwell", "one profile", "at a time"], MANGO))

    p.append(wire(218, 122, 258, 122))
    p.append(wire(408, 122, 448, 122))
    for y in (94, 176, 258):
        p.append(wire(778, 176 if y == 176 else 176 + (y - 176) * 0.15, 818, y))
        p.append(wire(988, y, 1024, 176, MANGO, True, "arrM"))

    # evaluation loop
    p.append(f'<line x1="28" y1="318" x2="1172" y2="318" stroke="{LINE}"/>')
    p.append(t(28, 348, "EVALUATION + PUBLICATION LOOP", 12, MANGO, 700, family=MONO, extra='letter-spacing="2"'))
    steps = [
        ("fair-bench", ["404 frozen items", "12 agent cases"]),
        ("graders", ["Wilson CIs", "paired bootstrap"]),
        ("blind panel", ["Claude + Codex", "22 open prompts"]),
        ("economics rule", ["quality first;", "≥1.5× faster to swap"]),
        ("HF cards + data", ["24 repos · charts", "per-item archive"]),
        ("PirateFace", ["torrent seeding", "for preservation"]),
    ]
    sw, sg = 170, 25
    for i, (title, lines) in enumerate(steps):
        x = 28 + i * (sw + sg)
        p.append(box(x, 366, sw, 80, title, lines, MANGO if i % 2 else CYAN))
        if i < len(steps) - 1:
            p.append(f'<line x1="{x+sw+2}" y1="406" x2="{x+sw+sg-4}" y2="406" stroke="{MANGO}" '
                     f'stroke-width="1.6" class="flow" marker-end="url(#arrM)"/>')
    return svg(w, h, "\n".join(p), defs, style)


# ---------------------------------------------------------------- leaderboard
def leaderboard(rows):
    w = 1200
    top, rh = 96, 34
    h = top + rh * len(rows) + 64
    x_name, x_bar, bar_w = 28, 384, 500
    lo, hi = 60.0, 90.0
    x_min = 990
    max_min = max(r[2] for r in rows)
    style = """
.bar{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);animation:grow 1.4s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes grow{to{transform:scaleX(1)}}
.val{opacity:0;animation:fade .6s ease forwards}
@keyframes fade{to{opacity:1}}
.star{animation:tw 2.2s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.55}50%{opacity:1}}
@media (prefers-reduced-motion: reduce){.bar{animation:none;transform:none}.val{animation:none;opacity:1}.star{animation:none}}
"""
    defs = EDGE
    for name, c in (("c", CYAN), ("m", MANGO), ("v", VIOLET), ("r", CORAL)):
        defs += (f'<linearGradient id="g{name}" x1="0" x2="1"><stop offset="0" stop-color="{c}" stop-opacity=".25"/>'
                 f'<stop offset="1" stop-color="{c}"/></linearGradient>')
    gid = {CYAN: "gc", MANGO: "gm", VIOLET: "gv", CORAL: "gr"}

    p = [frame(w, h)]
    p.append(t(28, 40, "MATCHED SCREEN · WEIGHTED QUALITY /100", 12, CYAN, 700, family=MONO, extra='letter-spacing="2"'))
    p.append(t(28, 62, "202 questions + 12 agent cases per configuration · social/EQ 30 · cyber 20 · coding 10 · agentic 30 · instr 5 · general 5",
               12, MUTED, 400))
    p.append(t(x_min, 86, "workload minutes ↓", 10.5, MUTED, 400, family=MONO))
    for gx in range(int(lo), int(hi) + 1, 5):
        x = x_bar + (gx - lo) / (hi - lo) * bar_w
        p.append(t(x, 86, f"{gx}", 10.5, MUTED, 400, "middle", MONO))
        p.append(f'<line x1="{x:.1f}" y1="{top-6}" x2="{x:.1f}" y2="{top + rh*len(rows)}" stroke="{LINE}" stroke-dasharray="2 4"/>')

    for i, (label, q, mins, _) in enumerate(rows):
        y = top + i * rh
        name, quant, c = NAMES.get(label, (label, "", CYAN))
        if i % 2 == 0:
            p.append(f'<rect x="16" y="{y}" width="{w-32}" height="{rh}" rx="8" fill="{PANEL}" opacity=".7"/>')
        p.append(t(x_name, y + 22, f"{i+1:>2}", 12, MUTED, 600, family=MONO))
        p.append(t(x_name + 30, y + 22, name, 13.5, TEXT, 600))
        p.append(t(x_name + 30 + 8.0 * len(name) + 10, y + 22, quant, 11, MUTED, 400, family=MONO))
        bw = max(2, (q - lo) / (hi - lo) * bar_w)
        delay = 0.08 * i
        p.append(f'<rect class="bar" style="animation-delay:{delay:.2f}s" x="{x_bar}" y="{y+9}" width="{bw:.1f}" '
                 f'height="16" rx="5" fill="url(#{gid[c]})"/>')
        p.append(t(x_bar + bw + 10, y + 22, f"{q:.2f}", 13, c, 700, family=MONO,
                   extra=f'class="val" style="animation-delay:{delay+0.9:.2f}s"'))
        mw = max(2, mins / max_min * 120)
        p.append(f'<rect x="{x_min}" y="{y+13}" width="120" height="8" rx="4" fill="{LINE}"/>')
        p.append(f'<rect class="bar" style="animation-delay:{delay+0.3:.2f}s" x="{x_min}" y="{y+13}" width="{mw:.1f}" height="8" rx="4" fill="{MUTED}"/>')
        p.append(t(x_min + 130, y + 22, f"{mins:.0f}m", 12, MUTED, 500, family=MONO))
        if label == PICK:
            p.append(t(x_bar - 16, y + 22, "★", 14, MANGO, 700, "middle", extra='class="star"'))
        elif label in PARETO:
            p.append(t(x_bar - 16, y + 22, "◆", 11, CYAN, 700, "middle"))
    fy = top + rh * len(rows) + 30
    p.append(t(28, fy, "★ default under the economics rule  ·  ◆ quality/time Pareto frontier  ·  "
               "scores apply to the exact checkpoint, quant, runtime and effort shown",
               11.5, MUTED, 400))
    return svg(w, h, "\n".join(p), defs, style)


# ---------------------------------------------------------------- domain heatmap
def heat_color(v):
    # 40 -> deep coral, 70 -> mango, 100 -> cyan
    stops = [(35, (255, 122, 89)), (70, (255, 181, 71)), (85, (150, 220, 200)), (100, (126, 224, 255))]
    v = max(stops[0][0], min(stops[-1][0], v))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if v <= b:
            f = (v - a) / (b - a)
            r, g, bl = (round(ca[k] + (cb[k] - ca[k]) * f) for k in range(3))
            return f"#{r:02x}{g:02x}{bl:02x}"
    return CYAN


def heatmap(rows):
    w = 1200
    top, rh = 104, 32
    h = top + rh * len(rows) + 56
    x0, cw = 380, 128
    style = """
.cell{opacity:0;animation:pop .5s ease forwards}
@keyframes pop{from{opacity:0}to{opacity:1}}
@media (prefers-reduced-motion: reduce){.cell{animation:none;opacity:1}}
"""
    p = [frame(w, h)]
    p.append(t(28, 40, "WHERE EACH MODEL IS STRONG · DOMAIN SCORES /100", 12, MANGO, 700, family=MONO, extra='letter-spacing="2"'))
    p.append(t(28, 62, "The owner's three equal focus areas are human understanding, coding + cybersecurity, and agentic work.", 12, MUTED, 400))
    for j, (_, title) in enumerate(DOMAINS):
        p.append(t(x0 + j * cw + cw / 2, 92, title, 12.5, TEXT, 600, "middle"))
    best = [max(r[3][j] for r in rows) for j in range(len(DOMAINS))]
    for i, (label, q, _, doms) in enumerate(rows):
        y = top + i * rh
        name, quant, _ = NAMES.get(label, (label, "", CYAN))
        p.append(t(28, y + 20, name, 13, TEXT, 600))
        p.append(t(28 + 7.6 * len(name) + 10, y + 20, quant, 10.5, MUTED, 400, family=MONO))
        for j, v in enumerate(doms):
            x = x0 + j * cw
            c = heat_color(v)
            d = 0.03 * (i + j)
            p.append(f'<g class="cell" style="animation-delay:{d:.2f}s">'
                     f'<rect x="{x+4}" y="{y+3}" width="{cw-8}" height="{rh-6}" rx="6" fill="{c}" fill-opacity=".22" '
                     f'stroke="{c}" stroke-opacity="{0.9 if v == best[j] else 0.25}"/>'
                     + t(x + cw / 2, y + 21, f"{v:.0f}", 13, c, 700 if v == best[j] else 500, "middle", MONO)
                     + '</g>')
    fy = top + rh * len(rows) + 30
    p.append(t(28, fy, "Outlined cells are the best score in that column. Same 202-question + 12-agent cohort for every row.", 11.5, MUTED, 400))
    return svg(w, h, "\n".join(p), EDGE, style)


def main():
    rows = load_rows(sys.argv[1] if len(sys.argv) > 1 else None)
    OUT.mkdir(exist_ok=True)
    files = {
        "hero.svg": hero(),
        "mango-stats.svg": stats(),
        "mango-architecture.svg": architecture(),
        "mango-leaderboard.svg": leaderboard(rows),
        "mango-domains.svg": heatmap(rows),
    }
    for name, content in files.items():
        (OUT / name).write_text(content)
        print("wrote", OUT / name, len(content), "bytes")


if __name__ == "__main__":
    main()
