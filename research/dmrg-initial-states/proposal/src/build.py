import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from refs import REFS  # noqa: E402
from figs import fig1, fig2  # noqa: E402

FONTS = os.path.join(os.path.dirname(HERE), "fonts")

body = open(os.path.join(HERE, "body.html"), encoding="utf-8").read()
body = body.replace("{{fig1}}", fig1()).replace("{{fig2}}", fig2())

order = []


def number(key):
    if key not in REFS:
        raise SystemExit(f"unknown ref key: {key}")
    if key not in order:
        order.append(key)
    return order.index(key) + 1


def fmt_nums(nums):
    nums = sorted(set(nums))
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        if j - i >= 2:
            out.append(f'<a href="#ref-{nums[i]}">{nums[i]}</a>&ndash;<a href="#ref-{nums[j]}">{nums[j]}</a>')
        else:
            out.extend(f'<a href="#ref-{n}">{n}</a>' for n in nums[i:j + 1])
        i = j + 1
    return '<span class="cite">[' + ", ".join(out) + "]</span>"


def cite(m):
    if m.group(1) == "references":
        return m.group(0)
    keys = [k.strip() for k in m.group(1).split(",")]
    return fmt_nums([number(k) for k in keys])


body = re.sub(r"\{\{([a-z0-9_, ]+)\}\}", cite, body)

items = []
for i, key in enumerate(order, 1):
    text, url = REFS[key]
    if "arXiv:" in text:
        text = re.sub(r"arXiv:([A-Za-z\-\.]*/?[0-9.]+)", lambda mm: f'<a class="arx" href="{url}">arXiv:{mm.group(1)}</a>', text, count=1)
        items.append(f'<li id="ref-{i}">{text}</li>')
    elif url.startswith("https://doi.org/"):
        items.append(f'<li id="ref-{i}">{text} <a class="arx" href="{url}">doi:{url[len("https://doi.org/"):]}</a></li>')
    else:
        items.append(f'<li id="ref-{i}">{text} <a class="url" href="{url}">{url}</a></li>')
body = body.replace("{{references}}", '<ol class="refs">' + "\n".join(items) + "</ol>")

unused = sorted(set(REFS) - set(order))
if unused:
    print("unused refs:", unused, file=sys.stderr)

css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read().replace("FONTDIR", "file://" + FONTS)
html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Learning the starting state: a proposal for neural-network seeds for DMRG</title>
<style>{css}</style></head>
<body>{body}</body></html>"""
open(os.path.join(HERE, "proposal.html"), "w", encoding="utf-8").write(html)
print("refs used:", len(order))
