#!/usr/bin/env python3
"""Draw every figure in this repository, light and dark.

    python tools/make_diagrams.py

Four figures, eight files, written to docs/figures/. They are SVG and they are
generated, so a colour or a label changes in one place and both themes stay in
step.

Nothing here is traced from anything. There is no screenshot of the real tool
in this repository and there will not be one: the user interface figure is a
wireframe drawn from the description in the internship report, at the sizes the
report states, with no field values, no part numbers, no supplier names and no
colleague's name. The grid in the first figure is drawn to the shape of the
sheet, not to its contents.
"""

from __future__ import annotations

import html
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "docs" / "figures"

THEMES = {
    "light": dict(
        bg="#F4F6FA", panel="#FFFFFF", ink="#1B2430", muted="#5F6C7D",
        hair="#D8DEE8", violet="#7A6BA8", blue="#4C7CAE", teal="#4E9A92",
        amber="#C08A5A", soft="#E9EDF3",
    ),
    "dark": dict(
        bg="#0E131A", panel="#161D27", ink="#DDE5EE", muted="#8795A6",
        hair="#2A3340", violet="#A99CD6", blue="#87AEDA", teal="#82C0B8",
        amber="#D6A478", soft="#1B2430",
    ),
}

FONT = ("font-family=\"Archivo, 'Segoe UI', Helvetica, Arial, sans-serif\"")
MONO = ("font-family=\"'IBM Plex Mono', 'Cascadia Mono', Consolas, monospace\"")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def text(x, y, s, *, size=15, fill="ink", weight=400, anchor="start", mono=False, C=None):
    return (f'<text x="{x}" y="{y}" {MONO if mono else FONT} font-size="{size}" '
            f'font-weight="{weight}" fill="{C[fill]}" text-anchor="{anchor}">{esc(s)}</text>')


def box(x, y, w, h, *, fill="panel", stroke="hair", r=10, sw=1.5, dash=None, C=None, op=1):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{C[fill]}" stroke="{C[stroke]}" stroke-width="{sw}"{d} opacity="{op}"/>')


def arrow(x1, y1, x2, y2, *, C=None, colour="muted", w=2, head=7):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(a), y2 - head * math.sin(a)
    p = (f'{x2},{y2} '
         f'{bx - head * 0.6 * math.sin(a)},{by + head * 0.6 * math.cos(a)} '
         f'{bx + head * 0.6 * math.sin(a)},{by - head * 0.6 * math.cos(a)}')
    return (f'<line x1="{x1}" y1="{y1}" x2="{bx}" y2="{by}" stroke="{C[colour]}" '
            f'stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{p}" fill="{C[colour]}"/>')


def frame(w, h, C, body):
    ramp = ('<linearGradient id="r" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0%" stop-color="{C["violet"]}"/>'
            f'<stop offset="52%" stop-color="{C["blue"]}"/>'
            f'<stop offset="100%" stop-color="{C["teal"]}"/></linearGradient>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img">'
            f"<defs>{ramp}</defs>"
            f'<rect width="{w}" height="{h}" fill="{C["bg"]}"/>'
            f'<rect width="{w}" height="4" fill="url(#r)"/>'
            f"{body}</svg>")


# ---------------------------------------------------------------- figure 1
def before_after(C) -> str:
    W, H = 1100, 520
    o = [text(40, 52, "Before and after", size=24, weight=700, C=C),
         text(40, 78, "The same question, asked of the same sheet", size=15, fill="muted", C=C)]

    # Before
    o.append(box(40, 104, 490, 376, C=C))
    o.append(text(64, 140, "Before", size=18, weight=600, fill="amber", C=C))
    o.append(text(64, 164, "find one component by eye", size=14, fill="muted", C=C))
    gx, gy, cw, ch, gap = 64, 186, 12, 9, 2.6
    for r in range(18):
        for c in range(30):
            fill = C["amber"] if (r == 11 and c == 19) else C["hair"]
            o.append(f'<rect x="{gx + c * (cw + gap)}" y="{gy + r * (ch + gap)}" '
                     f'width="{cw}" height="{ch}" rx="2" fill="{fill}"/>')
    o.append(text(64, 428, "about 600 rows and 130 or more columns", size=13, mono=True,
                  fill="muted", C=C))
    o.append(text(64, 452, "one row scanned at a time, every time", size=13, mono=True,
                  fill="muted", C=C))

    # After
    o.append(box(570, 104, 490, 376, C=C))
    o.append(text(594, 140, "After", size=18, weight=600, fill="teal", C=C))
    o.append(text(594, 164, "pick, click, read", size=14, fill="muted", C=C))

    steps = [("select the component", "a dropdown, not a search"),
             ("one click", "the UserForm fills itself"),
             ("read the record", "status, milestones, who owns it"),
             ("save", "written straight back to the sheet")]
    for i, (a, b) in enumerate(steps):
        y = 196 + i * 68
        o.append(box(594, y, 442, 54, fill="soft", C=C, r=8))
        o.append(f'<circle cx="624" cy="{y + 27}" r="13" fill="{C["teal"]}" opacity="0.18"/>')
        o.append(text(624, y + 32, str(i + 1), size=14, weight=700, fill="teal",
                      anchor="middle", mono=True, C=C))
        o.append(text(650, y + 23, a, size=15, weight=600, C=C))
        o.append(text(650, y + 42, b, size=13, fill="muted", C=C))
        if i < len(steps) - 1:
            o.append(arrow(624, y + 54, 624, y + 66, C=C, colour="hair", w=2, head=5))

    o.append(arrow(534, 292, 566, 292, C=C, colour="blue", w=2.5))
    return frame(W, H, C, "".join(o))


# ---------------------------------------------------------------- figure 2
def tool_flow(C) -> str:
    W, H = 1100, 420
    o = [text(40, 52, "What the tool does when you click", size=24, weight=700, C=C),
         text(40, 78, "One pass, from the dropdown to the sheet and back", size=15,
              fill="muted", C=C)]

    steps = [("UserForm", "opens on the sheet"),
             ("select", "component from a list"),
             ("look up", "the row behind it"),
             ("fill frames", "grouped by subject"),
             ("edit", "create, update, delete"),
             ("write back", "to the same sheet")]
    x = 40
    for i, (a, b) in enumerate(steps):
        w = 158
        o.append(box(x, 128, w, 92, fill="panel", C=C))
        o.append(f'<rect x="{x}" y="128" width="{w}" height="4" rx="2" '
                 f'fill="{C["blue"] if i < 4 else C["teal"]}"/>')
        o.append(text(x + w / 2, 170, a, size=16, weight=600, anchor="middle", C=C))
        o.append(text(x + w / 2, 192, b, size=12.5, fill="muted", anchor="middle", C=C))
        if i < len(steps) - 1:
            o.append(arrow(x + w + 4, 174, x + w + 26, 174, C=C, colour="hair", w=2))
        x += w + 30

    # The milestone row the form annotates.
    o.append(text(40, 268, "milestones the form annotates", size=13, mono=True,
                  fill="muted", C=C))
    for i, m in enumerate(["X", "P", "B", "K-AE", "BMG", "K"]):
        bx = 40 + i * 86
        o.append(box(bx, 284, 72, 38, fill="soft", C=C, r=8))
        o.append(text(bx + 36, 309, m, size=15, weight=600, anchor="middle", mono=True, C=C))

    o.append(box(618, 268, 442, 54, fill="soft", C=C, r=8))
    o.append(text(642, 291, "two market interfaces", size=15, weight=600, C=C))
    o.append(text(642, 310, "German and Chinese, one codebase behind them", size=13,
                  fill="muted", C=C))

    o.append(text(40, 372, "The write back is the part that mattered: the sheet other people "
                  "read stays the source of truth.", size=14, fill="muted", C=C))
    return frame(W, H, C, "".join(o))


# ---------------------------------------------------------------- figure 3
def architecture(C) -> str:
    W, H = 1100, 440
    o = [text(40, 52, "Where it sits", size=24, weight=700, C=C),
         text(40, 78, "One workbook, two interfaces, and the release system beside them",
              size=15, fill="muted", C=C)]

    o.append(box(40, 112, 420, 290, C=C))
    o.append(text(64, 146, "The workbook", size=17, weight=600, C=C))
    for i, (a, b) in enumerate([("UserForms", "German and Chinese market"),
                                ("VBA modules", "lookup, validation, write back"),
                                ("data sheet", "about 600 rows, 130+ columns")]):
        y = 170 + i * 74
        o.append(box(64, y, 372, 58, fill="soft", C=C, r=8))
        o.append(f'<rect x="64" y="{y}" width="4" height="58" rx="2" fill="{C["violet"]}"/>')
        o.append(text(84, y + 26, a, size=15, weight=600, C=C))
        o.append(text(84, y + 45, b, size=13, fill="muted", C=C))

    o.append(box(640, 112, 420, 290, C=C))
    o.append(text(664, 146, "FREIPRO", size=17, weight=600, fill="teal", C=C))
    o.append(text(664, 168, "the release system every department already used", size=13,
                  fill="muted", C=C))
    o.append(box(664, 190, 372, 92, fill="soft", C=C, r=8))
    o.append(text(688, 224, "the dashboard the buttons reach", size=15, weight=600, C=C))
    o.append(text(688, 248, "so the tool's records stay in step with the company's",
                  size=13, fill="muted", C=C))
    o.append(box(664, 300, 372, 76, fill="soft", C=C, r=8))
    o.append(text(688, 330, "adopted beyond the first department", size=15, weight=600, C=C))
    o.append(text(688, 353, "built for one, later taken up by numerous others", size=13,
                  fill="muted", C=C))

    o.append(arrow(466, 240, 634, 240, C=C, colour="blue", w=2.5))
    o.append(arrow(634, 282, 466, 282, C=C, colour="blue", w=2.5))
    o.append(text(550, 228, "link", size=12.5, mono=True, fill="muted", anchor="middle", C=C))
    return frame(W, H, C, "".join(o))


# ---------------------------------------------------------------- figure 4
def ui_wireframe(C) -> str:
    W, H = 1100, 520
    o = [text(40, 52, "The form, redrawn", size=24, weight=700, C=C),
         text(40, 78, "A wireframe from the report's description. Not a screenshot, and no "
              "field carries a value", size=15, fill="muted", C=C)]

    o.append(box(40, 108, 640, 372, C=C, r=12))
    o.append(text(68, 146, "Release tracking", size=18, weight=600, C=C))
    o.append(text(68, 168, "German market", size=13, mono=True, fill="muted", C=C))

    # The dropdown.
    o.append(box(68, 186, 584, 44, fill="soft", C=C, r=8))
    o.append(text(88, 214, "select component", size=15, fill="muted", C=C))
    o.append(f'<rect x="608" y="198" width="24" height="20" rx="4" fill="{C["blue"]}" '
             f'opacity="0.35"/>')

    # Four frames of grouped fields, drawn as empty rules.
    groups = ["department and location", "part and supplier", "cost and drawings",
              "milestones and lead time"]
    for i, g in enumerate(groups):
        gx = 68 + (i % 2) * 300
        gy = 246 + (i // 2) * 112
        o.append(box(gx, gy, 284, 96, fill="soft", C=C, r=8))
        o.append(text(gx + 16, gy + 24, g, size=13, weight=600, fill="muted", C=C))
        for k in range(3):
            o.append(f'<rect x="{gx + 16}" y="{gy + 38 + k * 18}" width="{150 + k * 40}" '
                     f'height="6" rx="3" fill="{C["hair"]}"/>')

    # The buttons.
    for i, b in enumerate(["create", "update", "delete", "save and close"]):
        bx = 700 + (i % 2) * 180
        by = 186 + (i // 2) * 62
        o.append(box(bx, by, 162, 46, fill="soft", C=C, r=8))
        o.append(text(bx + 81, by + 29, b, size=14, weight=600, anchor="middle", C=C))

    o.append(box(700, 316, 342, 164, fill="panel", C=C, r=12))
    o.append(text(724, 348, "Chinese market", size=16, weight=600, C=C))
    o.append(text(724, 370, "the same form, its own fields", size=13, fill="muted", C=C))
    o.append(box(724, 388, 294, 36, fill="soft", C=C, r=8))
    for k in range(2):
        o.append(f'<rect x="724" y="{436 + k * 16}" width="{240 - k * 60}" height="6" '
                 f'rx="3" fill="{C["hair"]}"/>')
    return frame(W, H, C, "".join(o))


FIGURES = {
    "01-before-after": before_after,
    "02-tool-flow": tool_flow,
    "03-architecture": architecture,
    "04-ui-wireframe": ui_wireframe,
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FIGURES.items():
        for theme, C in THEMES.items():
            suffix = "" if theme == "light" else "-dark"
            path = OUT / f"{name}{suffix}.svg"
            path.write_text(fn(C), encoding="utf-8")
            print(f"  {path.relative_to(OUT.parent.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
