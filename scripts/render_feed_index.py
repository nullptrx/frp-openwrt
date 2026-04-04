#!/usr/bin/env python3

from pathlib import Path


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Frp's Feed</title>
  <style>
    :root {{ color-scheme: light; }}
    body {{
      margin: 0;
      padding: 24px 16px 48px;
      background: #f4f4f4;
      color: #111;
      font-family: "SFMono-Regular", Menlo, Consolas, "Liberation Mono", monospace;
    }}
    .wrap {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    h1 {{
      margin: 0 0 24px;
      font-size: clamp(30px, 4.5vw, 54px);
      line-height: 1;
      letter-spacing: -0.04em;
    }}
    pre {{
      margin: 0;
      padding: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-size: clamp(12px, 1.5vw, 20px);
      line-height: 1.35;
    }}
    a {{
      color: #1f33ff;
      text-decoration: none;
    }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>Frp's Feed</h1>
    <pre>{tree}</pre>
  </div>
</body>
</html>
"""


def walk(root: Path, path: Path, prefix: str = ""):
    entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    entries = [p for p in entries if p.name not in {".nojekyll", "CNAME", "index.html"}]
    lines = []

    for index, entry in enumerate(entries):
        last = index == len(entries) - 1
        branch = "└── " if last else "├── "
        if entry.is_file():
            href = entry.relative_to(root).as_posix()
            lines.append(f'{prefix}{branch}<a href="{href}">{entry.name}</a>')
        else:
            lines.append(f"{prefix}{branch}{entry.name}")
        if entry.is_dir():
            lines.extend(walk(root, entry, prefix + ("    " if last else "│   ")))

    return lines


def main() -> int:
    root = Path("pages")
    tree = "\n".join(walk(root, root))
    (root / "index.html").write_text(HTML_TEMPLATE.format(tree=tree), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
