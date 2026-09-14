#!/usr/bin/env python3
"""Generate the paper's replacement diagrams as SVG and high-resolution PNG files."""

from __future__ import annotations

import html
import math
import subprocess
from pathlib import Path


OUT = Path(__file__).resolve().parent

NAVY = "#17324D"
BLUE = "#2F6FAD"
LIGHT_BLUE = "#DCEEFF"
ORANGE = "#E58B2A"
LIGHT_ORANGE = "#FCE7CE"
GREEN = "#2A9D8F"
RED = "#C94747"
PURPLE = "#7C5CFC"
GRAY = "#607080"
LIGHT_GRAY = "#EEF2F5"


def start(width: int, height: int, title: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f"<title>{html.escape(title)}</title>",
        "<defs>",
        '<marker id="arrow" markerWidth="12" markerHeight="8" refX="10" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L12,4 L0,8 z" fill="#17324D"/></marker>',
        '<marker id="arrowOrange" markerWidth="12" markerHeight="8" refX="10" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L12,4 L0,8 z" fill="#E58B2A"/></marker>',
        '<marker id="arrowStart" markerWidth="12" markerHeight="8" refX="2" refY="4" orient="auto" markerUnits="strokeWidth"><path d="M12,0 L0,4 L12,8 z" fill="#17324D"/></marker>',
        "<style>",
        "text{font-family:'DejaVu Sans',Arial,sans-serif;fill:#17324D}",
        ".title{font-size:32px;font-weight:700}.heading{font-size:27px;font-weight:700}.axis{font-size:29px;font-weight:700}.label{font-size:25px}.small{font-size:20px}.tiny{font-size:17px}",
        ".math{font-family:'DejaVu Serif',serif;font-size:27px;font-style:italic}",
        "</style>",
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="white"/>',
    ]


def text(x: float, y: float, value: str, cls: str = "label", anchor: str = "middle", extra: str = "") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}" {extra}>{html.escape(value)}</text>'


def finish(name: str, parts: list[str]) -> None:
    parts.append("</svg>")
    svg_path = OUT / f"{name}.svg"
    png_path = OUT / f"{name}.png"
    svg_path.write_text("\n".join(parts), encoding="utf-8")
    subprocess.run(
        [
            "convert",
            "-background",
            "white",
            "-density",
            "192",
            str(svg_path),
            "-strip",
            str(png_path),
        ],
        check=True,
    )


def bsc_diagram() -> None:
    p = start(1100, 520, "Binary symmetric channel transition diagram")
    p += [
        text(180, 95, "Channel input X", "heading"),
        text(920, 95, "Channel output Y", "heading"),
    ]
    for x, y, bit in [(180, 180, "0"), (180, 365, "1"), (920, 180, "0"), (920, 365, "1")]:
        p.append(f'<circle cx="{x}" cy="{y}" r="42" fill="{LIGHT_BLUE}" stroke="{BLUE}" stroke-width="3"/>')
        p.append(text(x, y + 10, bit, "heading"))
    p += [
        f'<line x1="225" y1="180" x2="875" y2="180" stroke="{NAVY}" stroke-width="4" marker-end="url(#arrow)"/>',
        f'<line x1="225" y1="365" x2="875" y2="365" stroke="{NAVY}" stroke-width="4" marker-end="url(#arrow)"/>',
        f'<path d="M220 195 C450 225, 650 320, 878 350" fill="none" stroke="{ORANGE}" stroke-width="4" marker-end="url(#arrowOrange)"/>',
        f'<path d="M220 350 C450 320, 650 225, 878 195" fill="none" stroke="{ORANGE}" stroke-width="4" marker-end="url(#arrowOrange)"/>',
        text(550, 165, "1 − p", "math"),
        text(550, 395, "1 − p", "math"),
        text(430, 265, "p", "math"),
        text(670, 265, "p", "math"),
        f'<line x1="300" y1="470" x2="390" y2="470" stroke="{NAVY}" stroke-width="4"/>',
        text(405, 478, "unchanged", "small", "start"),
        f'<line x1="610" y1="470" x2="700" y2="470" stroke="{ORANGE}" stroke-width="4"/>',
        text(715, 478, "flipped", "small", "start"),
    ]
    finish("bsc_diagram", p)


def bec_diagram() -> None:
    p = start(1100, 600, "Binary erasure channel transition diagram")
    p += [
        text(180, 85, "Channel input X", "heading"),
        text(920, 85, "Channel output Y", "heading"),
    ]
    for x, y, symbol, fill, stroke in [
        (180, 190, "0", LIGHT_BLUE, BLUE),
        (180, 430, "1", LIGHT_BLUE, BLUE),
        (920, 140, "0", LIGHT_BLUE, BLUE),
        (920, 310, "?", LIGHT_ORANGE, ORANGE),
        (920, 480, "1", LIGHT_BLUE, BLUE),
    ]:
        p.append(f'<circle cx="{x}" cy="{y}" r="42" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
        p.append(text(x, y + 10, symbol, "heading"))
    p += [
        f'<path d="M224 184 C470 165, 660 150, 875 142" fill="none" stroke="{NAVY}" stroke-width="4" marker-end="url(#arrow)"/>',
        f'<path d="M224 436 C470 455, 660 470, 875 478" fill="none" stroke="{NAVY}" stroke-width="4" marker-end="url(#arrow)"/>',
        f'<path d="M218 214 C460 240, 650 285, 877 304" fill="none" stroke="{ORANGE}" stroke-width="4" marker-end="url(#arrowOrange)"/>',
        f'<path d="M218 406 C460 380, 650 335, 877 316" fill="none" stroke="{ORANGE}" stroke-width="4" marker-end="url(#arrowOrange)"/>',
        text(545, 145, "1 − ε", "math"),
        text(545, 500, "1 − ε", "math"),
        text(555, 255, "ε", "math"),
        text(555, 375, "ε", "math"),
    ]
    finish("bec_diagram", p)


def hamming_balls_discrete() -> None:
    p = start(1200, 540, "Discrete Hamming balls around two codewords")
    centers = [(300, 285, BLUE, LIGHT_BLUE, "c"), (900, 285, ORANGE, LIGHT_ORANGE, "c′")]
    offsets = [(-115, -70), (-100, 55), (-55, -125), (-45, 110), (0, -145), (20, 135), (65, -105), (80, 100), (120, -45), (125, 55)]
    for cx, cy, color, pale, label in centers:
        p.append(f'<circle cx="{cx}" cy="{cy}" r="190" fill="{pale}" fill-opacity="0.42" stroke="{color}" stroke-width="3" stroke-dasharray="8 7"/>')
        for dx, dy in offsets:
            p.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="12" fill="{pale}" stroke="{color}" stroke-width="2"/>')
        p.append(f'<rect x="{cx-18}" y="{cy-18}" width="36" height="36" rx="4" fill="{color}" stroke="{NAVY}" stroke-width="2"/>')
        p.append(text(cx, cy + 8, label, "heading", extra='fill="white"'))
        p.append(text(cx, cy - 160, f"Bₜ({label})", "heading"))
    p += [
        f'<line x1="335" y1="285" x2="865" y2="285" stroke="{NAVY}" stroke-width="3" stroke-dasharray="9 8" marker-start="url(#arrowStart)" marker-end="url(#arrow)"/>',
        '<text x="600" y="240" class="small" text-anchor="middle"><tspan font-style="italic">d</tspan><tspan baseline-shift="sub" font-size="15">H</tspan><tspan>(c,c′) = </tspan><tspan font-style="italic">d</tspan><tspan baseline-shift="sub" font-size="15">min</tspan><tspan> &gt; 2t</tspan></text>',
    ]
    finish("hamming_balls_discrete", p)


def xor_table() -> None:
    p = start(760, 440, "Truth table for XOR")
    left, top, col_w, row_h = 110, 30, 180, 78
    headers = ["x₁", "x₂"]
    rows = [("0", "0", "0"), ("0", "1", "1"), ("1", "0", "1"), ("1", "1", "0")]
    for c in range(3):
        p.append(f'<rect x="{left+c*col_w}" y="{top}" width="{col_w}" height="{row_h}" fill="{NAVY}" stroke="white" stroke-width="2"/>')
        if c < 2:
            p.append(text(left + (c + 0.5) * col_w, top + 51, headers[c], "heading", extra='fill="white"'))
    header_y = top + 43
    p += [
        text(515, header_y + 8, "x₁", "heading", extra='fill="white"'),
        f'<circle cx="560" cy="{header_y}" r="13" fill="none" stroke="white" stroke-width="2"/>',
        f'<line x1="552" y1="{header_y}" x2="568" y2="{header_y}" stroke="white" stroke-width="2"/>',
        f'<line x1="560" y1="{header_y-8}" x2="560" y2="{header_y+8}" stroke="white" stroke-width="2"/>',
        text(605, header_y + 8, "x₂", "heading", extra='fill="white"'),
    ]
    for r, row in enumerate(rows):
        fill = LIGHT_BLUE if r % 2 == 0 else "white"
        for c, value in enumerate(row):
            y = top + (r + 1) * row_h
            p.append(f'<rect x="{left+c*col_w}" y="{y}" width="{col_w}" height="{row_h}" fill="{fill}" stroke="{NAVY}" stroke-width="2"/>')
            p.append(text(left + (c + 0.5) * col_w, y + 51, value, "heading"))
    finish("xor_truth_table", p)


def binomial_typical_set() -> None:
    n, prob, eps = 100, 0.10, 0.05
    ks = list(range(0, 31))
    pmf = [math.comb(n, k) * prob**k * (1 - prob) ** (n - k) for k in ks]
    tail = sum(math.comb(n, k) * prob**k * (1 - prob) ** (n - k) for k in range(n + 1) if k < 5 or k > 15)
    p = start(1200, 720, "Binomial concentration and the typical flip interval")
    x0, y0, pw, ph = 110, 610, 1010, 470
    ymax = max(pmf) * 1.14
    p += [
        f'<line x1="{x0}" y1="{y0}" x2="{x0+pw}" y2="{y0}" stroke="{NAVY}" stroke-width="3" marker-end="url(#arrow)"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-ph}" stroke="{NAVY}" stroke-width="3" marker-end="url(#arrow)"/>',
        text(620, 682, "number of flipped bits k", "label"),
        text(115, 118, "Pr(Kₙ = k)", "small", "start"),
    ]
    bar_w = pw / 33
    for k, val in zip(ks, pmf):
        x = x0 + (k + 0.7) * pw / 31
        h = val / ymax * ph
        color = BLUE if 5 <= k <= 15 else ORANGE
        p.append(f'<rect x="{x-bar_w/2:.1f}" y="{y0-h:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{color}" opacity="0.9"/>')
    for k in range(0, 31, 5):
        x = x0 + (k + 0.7) * pw / 31
        p.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0+8}" stroke="{NAVY}" stroke-width="2"/>')
        p.append(text(x, y0 + 35, str(k), "small"))
    for k, label in [(5, "(p−ε)n = 5"), (10, "np = 10"), (15, "(p+ε)n = 15")]:
        x = x0 + (k + 0.7) * pw / 31
        color = GREEN if k == 10 else GRAY
        p.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0-ph}" stroke="{color}" stroke-width="3" stroke-dasharray="9 7"/>')
        p.append(text(x, 105 if k == 10 else 132, label, "small"))
    p += [
        f'<rect x="770" y="165" width="330" height="185" rx="14" fill="{LIGHT_GRAY}" stroke="{GRAY}" stroke-width="2"/>',
        text(935, 205, "Example: n=100, p=0.10, ε=0.05", "small"),
        text(935, 240, f"Pr(outside the interval) ≈ {tail:.3f}", "small"),
        text(935, 270, "For fixed ε, this tends to 0 as n grows.", "tiny"),
        f'<rect x="810" y="295" width="20" height="20" fill="{BLUE}"/><text x="840" y="312" class="tiny">typical interval</text>',
        f'<rect x="950" y="295" width="20" height="20" fill="{ORANGE}"/><text x="980" y="312" class="tiny">tail events</text>',
    ]
    finish("binomial_typical_set", p)


def binary_entropy() -> None:
    p = start(1000, 700, "Binary entropy function")
    x0, y0, pw, ph = 110, 610, 800, 500
    p += [
        f'<line x1="{x0}" y1="{y0}" x2="{x0+pw}" y2="{y0}" stroke="{NAVY}" stroke-width="3" marker-end="url(#arrow)"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-ph}" stroke="{NAVY}" stroke-width="3" marker-end="url(#arrow)"/>',
        text(520, 680, "p", "axis"),
        text(110, 82, "h₂(p) (bits)", "axis", "start"),
    ]
    points = []
    for i in range(401):
        q = i / 400
        h = 0.0 if q in (0.0, 1.0) else -q * math.log2(q) - (1 - q) * math.log2(1 - q)
        points.append(f"{x0+q*pw:.2f},{y0-h*ph:.2f}")
    p.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{BLUE}" stroke-width="6"/>')
    for q, h, label, dx, dy in [(0, 0, "(0, 0)", 45, -12), (0.5, 1, "(1/2, 1)", 0, -20), (1, 0, "(1, 0)", -45, -12)]:
        x, y = x0 + q * pw, y0 - h * ph
        p.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{RED}" stroke="white" stroke-width="3"/>')
        p.append(text(x + dx, y + dy, label, "small"))
    for q in [0, 0.25, 0.5, 0.75, 1.0]:
        x = x0 + q * pw
        p.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0+8}" stroke="{NAVY}" stroke-width="2"/>')
        p.append(text(x, y0 + 35, f"{q:g}", "small"))
    for h in [0, 0.5, 1.0]:
        y = y0 - h * ph
        p.append(f'<line x1="{x0-8}" y1="{y}" x2="{x0}" y2="{y}" stroke="{NAVY}" stroke-width="2"/>')
        p.append(text(x0 - 18, y + 7, f"{h:g}", "small", "end"))
        if h > 0:
            p.append(f'<line x1="{x0}" y1="{y}" x2="{x0+pw}" y2="{y}" stroke="{LIGHT_GRAY}" stroke-width="2"/>')
    finish("binary_entropy", p)


def typical_region_ambiguity() -> None:
    p = start(1250, 620, "Noise-cloud overlap and minimum-distance comparison")
    x1, x2, cy, radius = 385, 865, 315, 285
    # Circular noise clouds, with their overlap drawn explicitly in a third color.
    p += [
        f'<circle cx="{x1}" cy="{cy}" r="{radius}" fill="{LIGHT_BLUE}" fill-opacity="0.68"/>',
        f'<circle cx="{x2}" cy="{cy}" r="{radius}" fill="{LIGHT_ORANGE}" fill-opacity="0.68"/>',
        f'<path d="M625 161.3 A285 285 0 0 1 625 468.7 A285 285 0 0 1 625 161.3 Z" fill="{GREEN}" fill-opacity="0.72"/>',
        f'<circle cx="{x1}" cy="{cy}" r="{radius}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-dasharray="8 7"/>',
        f'<circle cx="{x2}" cy="{cy}" r="{radius}" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-dasharray="8 7"/>',
    ]
    offsets = [(-150, -85), (-110, 75), (-65, -130), (-35, 115), (20, -105), (70, 95), (115, -55), (145, 50)]
    for cx, color, pale in [(x1, BLUE, LIGHT_BLUE), (x2, ORANGE, LIGHT_ORANGE)]:
        for dx, dy in offsets:
            p.append(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="10" fill="{pale}" stroke="{color}" stroke-width="2"/>')
    yx, yy = 625, 315
    p += [
        f'<rect x="{x1-20}" y="{cy-20}" width="40" height="40" rx="4" fill="{BLUE}"/>',
        f'<rect x="{x2-20}" y="{cy-20}" width="40" height="40" rx="4" fill="{ORANGE}"/>',
        f'<polygon points="{yx},{yy-22} {yx+22},{yy} {yx},{yy+22} {yx-22},{yy}" fill="{PURPLE}" stroke="{NAVY}" stroke-width="2"/>',
        text(x1, cy - 55, "x = f(u)", "math"),
        text(x2, cy - 55, "x′ = f(u′)", "math"),
        text(yx, yy + 108, "received word y", "math"),
        text(x1, 72, "noise cloud centered at x", "small"),
        text(x2, 72, "noise cloud centered at x′", "small"),
        f'<line x1="{yx-25}" y1="{yy-8}" x2="{x1+25}" y2="{cy-8}" stroke="{NAVY}" stroke-width="3" marker-end="url(#arrow)"/>',
        f'<line x1="{yx+25}" y1="{yy+8}" x2="{x2-25}" y2="{cy+8}" stroke="{NAVY}" stroke-width="3" marker-end="url(#arrow)"/>',
        text(450, 350, "distance from y to x", "small"),
        text(800, 350, "distance from y to x′", "small"),
    ]
    finish("typical_region_ambiguity", p)


def mutual_information_heuristic() -> None:
    p = start(1100, 610, "Mutual-information heuristic")
    p += [
        f'<circle cx="420" cy="300" r="190" fill="{RED}" fill-opacity="0.55"/>',
        f'<circle cx="680" cy="300" r="190" fill="{BLUE}" fill-opacity="0.55"/>',
        f'<path d="M550 161.4 A190 190 0 0 1 550 438.6 A190 190 0 0 1 550 161.4 Z" fill="{GREEN}" fill-opacity="0.88"/>',
        f'<circle cx="420" cy="300" r="190" fill="none" stroke="{RED}" stroke-width="4"/>',
        f'<circle cx="680" cy="300" r="190" fill="none" stroke="{BLUE}" stroke-width="4"/>',
        text(300, 105, "H(X)", "heading"),
        text(800, 105, "H(Y)", "heading"),
        text(330, 305, "H(X | Y)", "heading"),
        text(550, 305, "I(X;Y)", "heading"),
        text(770, 305, "H(Y | X)", "heading"),
        f'<path d="M230 520 v25 h640 v-25" fill="none" stroke="{NAVY}" stroke-width="4"/>',
        text(550, 585, "H(X,Y)", "heading"),
    ]
    finish("mutual_information_heuristic", p)


def polar_kernel() -> None:
    p = start(1080, 400, "Two-bit polar transform")
    for x, y, label, width in [(120, 150, "U", 150), (120, 335, "V", 150), (925, 150, "", 260), (925, 335, "x₂ = V", 260)]:
        p.append(f'<rect x="{x-width/2}" y="{y-35}" width="{width}" height="70" rx="30" fill="{LIGHT_BLUE}" stroke="{BLUE}" stroke-width="3"/>')
        if label:
            p.append(text(x, y + 9, label, "heading"))
    p += [
        f'<line x1="195" y1="150" x2="485" y2="150" stroke="{NAVY}" stroke-width="4"/>',
        f'<line x1="195" y1="335" x2="790" y2="335" stroke="{NAVY}" stroke-width="4" marker-end="url(#arrow)"/>',
        f'<line x1="310" y1="335" x2="495" y2="175" stroke="{NAVY}" stroke-width="4"/>',
        f'<circle cx="520" cy="150" r="34" fill="{LIGHT_ORANGE}" stroke="{ORANGE}" stroke-width="4"/>',
        f'<line x1="502" y1="150" x2="538" y2="150" stroke="{NAVY}" stroke-width="4"/>',
        f'<line x1="520" y1="132" x2="520" y2="168" stroke="{NAVY}" stroke-width="4"/>',
        f'<line x1="554" y1="150" x2="790" y2="150" stroke="{NAVY}" stroke-width="4" marker-end="url(#arrow)"/>',
        text(858, 159, "x₁ = U", "heading"),
        f'<circle cx="953" cy="150" r="14" fill="none" stroke="{NAVY}" stroke-width="2"/>',
        f'<line x1="944" y1="150" x2="962" y2="150" stroke="{NAVY}" stroke-width="2"/>',
        f'<line x1="953" y1="141" x2="953" y2="159" stroke="{NAVY}" stroke-width="2"/>',
        text(995, 159, "V", "heading"),
    ]
    finish("polar_kernel", p)


def polarization_recursion() -> None:
    p = start(1500, 700, "Recursive channel polarization")
    ys = [125 + 72 * i for i in range(8)]
    p += [
        text(190, 85, "n = 8 identical uses of W", "heading"),
        text(1200, 85, "n = 8 synthetic channels", "heading"),
        f'<rect x="360" y="110" width="560" height="560" rx="30" fill="{LIGHT_GRAY}" stroke="{GRAY}" stroke-width="3"/>',
        text(640, 160, "m = log₂n = 3 recursive stages", "heading"),
    ]
    for i, y in enumerate(ys, 1):
        p.append(f'<rect x="90" y="{y-22}" width="120" height="44" rx="8" fill="{LIGHT_BLUE}" stroke="{BLUE}" stroke-width="2"/>')
        p.append(text(150, y + 7, f"W use {i}", "small"))
        p.append(f'<line x1="210" y1="{y}" x2="360" y2="{y}" stroke="{GRAY}" stroke-width="2"/>')
    # A representative minus/plus split inside the recursion block.
    p += [
        f'<circle cx="505" cy="380" r="38" fill="white" stroke="{NAVY}" stroke-width="3"/>',
        text(505, 389, "W", "heading"),
        f'<line x1="543" y1="370" x2="710" y2="295" stroke="{NAVY}" stroke-width="3" marker-end="url(#arrow)"/>',
        f'<line x1="543" y1="390" x2="710" y2="465" stroke="{NAVY}" stroke-width="3" marker-end="url(#arrow)"/>',
        f'<rect x="710" y="260" width="145" height="65" rx="16" fill="{LIGHT_ORANGE}" stroke="{ORANGE}" stroke-width="3"/>',
        f'<rect x="710" y="435" width="145" height="65" rx="16" fill="{LIGHT_BLUE}" stroke="{BLUE}" stroke-width="3"/>',
        text(782, 300, "W⁻", "heading"),
        text(782, 475, "W⁺", "heading"),
        text(782, 345, "less reliable", "small"),
        text(782, 530, "more reliable", "small"),
        text(640, 610, "Apply this split recursively to every descendant", "small"),
    ]
    for i, y in enumerate(ys, 1):
        p.append(f'<line x1="920" y1="{y}" x2="1080" y2="{y}" stroke="{GRAY}" stroke-width="2"/>')
        p.append(f'<rect x="1080" y="{y-22}" width="235" height="44" rx="8" fill="{LIGHT_BLUE}" stroke="{BLUE}" stroke-width="2"/>')
        p.append(text(1198, y + 7, f"W₈ ({i})", "heading"))
    finish("polarization_recursion", p)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    bsc_diagram()
    bec_diagram()
    xor_table()
    binomial_typical_set()
    binary_entropy()
    mutual_information_heuristic()
    polar_kernel()


if __name__ == "__main__":
    main()
