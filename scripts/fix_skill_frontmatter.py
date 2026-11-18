#!/usr/bin/env python3
"""Strip SKILL.md frontmatter fields that make agent hosts reject a skill.

`triggers` only accepts `user` / `model`; some upstreams use it as a keyword
list, which hides the skill entirely. Re-run after every upstream sync.
"""
import pathlib
import re
import sys

VALID_TRIGGERS = {"user", "model"}
FRONTMATTER = re.compile(r"\A---\r?\n(.*?\r?\n)---\r?\n", re.S)


def trigger_values(block):
    head, _, rest = block[0].partition(":")
    inline = rest.strip()
    if inline:
        return [v.strip().strip("'\"") for v in inline.strip("[]").split(",") if v.strip()]
    return [l.strip().lstrip("-").strip().strip("'\"") for l in block[1:] if l.strip()]


def fix(text):
    m = FRONTMATTER.match(text)
    if not m:
        return text
    lines = m.group(1).splitlines(keepends=True)
    out, i, changed = [], 0, False
    while i < len(lines):
        if re.match(r"triggers\s*:", lines[i]):
            j = i + 1
            while j < len(lines) and (lines[j][:1] in (" ", "\t", "-") or not lines[j].strip()):
                j += 1
            values = trigger_values(lines[i:j])
            if values and all(v in VALID_TRIGGERS for v in values):
                out.extend(lines[i:j])
            else:
                changed = True
            i = j
            continue
        out.append(lines[i])
        i += 1
    if not changed:
        return text
    return text[: m.start(1)] + "".join(out) + text[m.end(1):]


def main(root):
    for path in sorted(pathlib.Path(root).glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        fixed = fix(text)
        if fixed != text:
            path.write_text(fixed, encoding="utf-8")
            print(f"  🩹 Removed invalid triggers from {path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "skills")
