import os
import html
import urllib.parse
from datetime import datetime

EXCLUDE_FILES = ['index.html', 'generate_index.py', 'CNAME']

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rocky Linux Altarch Repository</title>
    <style>
        body {{
            font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
            font-size: 1rem;
            margin: 0;
            padding: 0;
        }}
        .header {{
            border-bottom: 1px solid;
        }}
        .header-content {{
            max-width: 1140px;
            margin: 0 auto;
            padding: 20px 15px;
            display: flex;
            align-items: center;
        }}
        .brand {{
            display: flex;
            align-items: center;
            text-decoration: none;
        }}
        .brand-logo {{
            height: 32px;
            width: auto;
            display: inline-block;
        }}

        .container {{ 
            max-width: 1140px;
            margin: 0 auto;
            padding: 25px 15px; 
        }}

        .breadcrumbs-box {{
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 25px;
            font-size: 1rem;
        }}
        .breadcrumbs a {{ text-decoration: none; }}
        .breadcrumbs a:hover {{ text-decoration: underline; color: #10b981; }}
        .breadcrumbs .separator {{ margin: 0 6px; }}

        table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 1rem; }}
        th, td {{ padding: 12px 12px; border-bottom: 1px solid; vertical-align: middle; }}
        th {{ 
            font-weight: bold;
            border-bottom: 2px solid;
            cursor: pointer;
            user-select: none;
        }}

        .item-link {{
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            transition: color 0.15s ease;
        }}
        
        .item-link:hover {{ 
            color: #10b981 !important; 
            text-decoration: underline; 
        }}
        
        .item-link:hover .icon {{
            color: #10b981 !important;
        }}
        
        .icon {{ margin-right: 8px; display: inline-block; flex-shrink: 0; transition: color 0.15s ease; }}

        .size-col {{ width: 150px; }}
        .date-col {{ width: 220px; }}

        .footer {{
            max-width: 1140px;
            margin: 40px auto 20px auto;
            padding: 15px;
            border-top: 1px solid;
            text-align: right;
            font-size: 11px;
        }}
        .footer a {{ color: #10b981; text-decoration: none; }}
        .footer .edgeone {{ color: #ef4444; font-weight: bold; }}

        @media (prefers-color-scheme: light) {{
            body {{
                color: #212529;
                background-color: #fff;
            }}
            .header {{ border-color: #e9ecef; }}
            .breadcrumbs-box {{ background-color: #f8f9fa; }}
            .breadcrumbs a {{ color: #007bff; }}
            .breadcrumbs span {{ color: #6c757d; }}
            .breadcrumbs .separator {{ color: #6c757d; }}
            th {{ color: #000; border-color: #dee2e6; }}
            td {{ border-color: #dee2e6; }}
            th:hover {{ background-color: #f1f3f5; }}
            tr:hover {{ background-color: #f8f9fa; }}
            .item-link {{ color: #000; }}
            .icon {{ color: #495057; }}
            .size-col, .date-col, td.size, td.date {{ color: #6c757d; }}
            .footer {{ border-color: #dee2e6; color: #6c757d; }}
        }}

        @media (prefers-color-scheme: dark) {{
            body {{
                color: #adbac7;
                background-color: #121212;
            }}
            .header {{ border-color: #121212; }}
            img {{ filter: brightness(0) invert(1); }}
            .breadcrumbs-box {{ background-color: #1e1e1e; }}
            .breadcrumbs a {{ color: #ffffff; }}
            .breadcrumbs span {{ color: #8b949e; }}
            .breadcrumbs .separator {{ color: #8b949e; }}
            th {{ color: #10b981; border-color: #121212; }}
            th.size-col, th.date-col {{ color: #10b981; }}
            td {{ border-color: #121212; }}
            th:hover {{ background-color: #1e1e1e; }}
            tr:hover {{ background-color: #1e1e1e; }}
            .item-link {{ color: #ffffff; }}
            .icon {{ color: #c9d1d9; }}
            .size-col, .date-col, td.size, td.date {{ color: #8b949e; }}
            .footer {{ border-color: #121212; color: #8b949e; }}
            .brand-logo path {{ fill: #ffffff; }}
            .brand-logo path:first-child {{ fill: #10b981; }}
        }}
    </style>
</head>
<body>

<div class="header">
    <div class="header-content">
        <a href="/" class="brand">
            <img height="30px" src='data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjQ2MiIgdmlld0JveD0iMCAuMTEgNzk5LjkgMTQ3Ljg0IiB3aWR0aD0iMjUwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJtMTQzLjc2IDk4LjQxYzIuNjctNy42NCA0LjExLTE1Ljg0IDQuMTEtMjQuMzggMC00MC44Mi0zMy4xLTczLjkyLTczLjkzLTczLjkyLTQwLjg0IDAtNzMuOTQgMzMuMS03My45NCA3My45MiAwIDIwLjIgOC4xIDM4LjUxIDIxLjI0IDUxLjg1bDc1LTc0Ljk4IDE4LjUyIDE4LjUxem0tMTMuNTEgMjMuNTItMzQuMDEtMzQuMDEtNTMuMjcgNTMuMjVjOS40MiA0LjM1IDE5LjkxIDYuNzggMzAuOTcgNi43OCAyMi41NSAwIDQyLjc1LTEwLjEgNTYuMzEtMjYuMDJ6IiBmaWxsPSIjMTBiOTgxIi8+PHBhdGggZD0ibTE5My4zNyAxMTIuNTN2LTc3LjYxaDM3LjkzYzMuOTIgMCA3LjUuNTkgMTAuNzYgMS43NyAzLjMzIDEuMTggNi4xNyAyLjg1IDguNTQgNC45OSAyLjM2IDIuMDcgNC4yMSA0LjU4IDUuNTQgNy41NHMyIDYuMjEgMiA5Ljc2YzAgNC44Ny0xLjQxIDkuMjQtNC4yMiAxMy4wOC0yLjczIDMuODQtNi4zOSA2LjY5LTEwLjk3IDguNTRsMTcuMTkgMzEuOTNoLTE3Ljk3bC0xNS4yLTI5LjcyaC0xNy41MnYyOS43MnptMzYuNDktNjMuNzVoLTIwLjQxdjIwLjg0aDIwLjQxYzMuNjIgMCA2LjUtLjk2IDguNjUtMi44OCAyLjIyLTEuOTIgMy4zMy00LjQ0IDMuMzMtNy41NCAwLTMuMTEtMS4xMS01LjYyLTMuMzMtNy41NC0yLjE1LTEuOTItNS4wMy0yLjg4LTguNjUtMi44OHptMzEuNzcgMzQuOTJjMC00LjIxLjc3LTguMTMgMi4zMi0xMS43NSAxLjYzLTMuNyAzLjgxLTYuODggNi41NS05LjU0IDIuODEtMi43MyA2LjEtNC44OCA5Ljg3LTYuNDNzNy44LTIuMzMgMTIuMDktMi4zMyA4LjMyLjc4IDEyLjA5IDIuMzMgNy4wMiAzLjcgOS43NiA2LjQzYzIuODEgMi42NiA0Ljk5IDUuODQgNi41NCA5LjU0IDEuNjMgMy42MiAyLjQ0IDcuNTQgMi40NCAxMS43NSAwIDQuMjItLjgxIDguMTctMi40NCAxMS44Ny0xLjU1IDMuNjItMy43MyA2Ljc2LTYuNTQgOS40Mi0yLjc0IDIuNjYtNS45OSA0Ljc3LTkuNzYgNi4zMnMtNy44IDIuMzMtMTIuMDkgMi4zMy04LjMyLS43OC0xMi4wOS0yLjMzLTcuMDYtMy42Ni05Ljg3LTYuMzJjLTIuNzQtMi42Ni00LjkyLTUuOC02LjU1LTkuNDItMS41NS0zLjctMi4zMi03LjY1LTIuMzItMTEuODd6bTMwLjgzIDE2Ljc0YzQuNDMgMCA4LjItMS42MiAxMS4zMS00Ljg3IDMuMTEtMy4yNiA0LjY2LTcuMjEgNC42Ni0xMS44NyAwLTQuNzMtMS41NS04LjcyLTQuNjYtMTEuOTctMy4xMS0zLjI2LTYuODgtNC44OC0xMS4zMS00Ljg4LTQuNDQgMC04LjIxIDEuNjItMTEuMzEgNC44OC0zLjExIDMuMjUtNC42NiA3LjI0LTQuNjYgMTEuOTcgMCA0LjY2IDEuNTUgOC42MSA0LjY2IDExLjg3IDMuMSAzLjI1IDYuODcgNC44NyAxMS4zMSA0Ljg3em03Ni4wOS0xLjY2YzIuMjktMS4wMyA0LjQ4LTIuNjYgNi41NS00Ljg4bDkuMDkgOS40M2MtMi45NiAzLjI1LTYuNTEgNS44LTEwLjY1IDcuNjUtNC4xNCAxLjc3LTguNDMgMi42Ni0xMi44NiAyLjY2LTQuMjIgMC04LjIxLS43OC0xMS45OC0yLjMzLTMuNy0xLjU1LTYuOTEtMy42Ni05LjY1LTYuMzItMi42Ni0yLjY2LTQuNzctNS44LTYuMzItOS40Mi0xLjU1LTMuNy0yLjMzLTcuNjUtMi4zMy0xMS44NyAwLTQuMjEuNzgtOC4xMyAyLjMzLTExLjc1IDEuNTUtMy43IDMuNjYtNi44OCA2LjMyLTkuNTQgMi43NC0yLjczIDUuOTUtNC44OCA5LjY1LTYuNDMgMy43Ny0xLjU1IDcuNzYtMi4zMyAxMS45OC0yLjMzIDQuNTggMCA4Ljk4LjkzIDEzLjIgMi43OCA0LjIxIDEuNzcgNy44IDQuMjggMTAuNzUgNy41NGwtOS4zMSA5Ljg2Yy0yLjA3LTIuMjktNC4yOS00LjAyLTYuNjYtNS4yMS0yLjM2LTEuMTgtNC45MS0xLjc3LTcuNjUtMS43Ny00LjM2IDAtOC4wNiAxLjYyLTExLjA5IDQuODgtMi45NiAzLjI1LTQuNDQgNy4yNC00LjQ0IDExLjk3czEuNTIgOC42OSA0LjU1IDExLjg3YzMuMTEgMy4xNyA2Ljg4IDQuNzYgMTEuMzEgNC43NiAyLjU5IDAgNC45OS0uNTEgNy4yMS0xLjU1em0yMy41NCAxMy43NXYtNzcuNjFsMTUuMTktMy4zM3Y0Ny41N2wyNC45Ni0yNC40aDE3LjE5bC0yNy4wNiAyNi41IDI4LjcyIDMxLjI3aC0xOS40MWwtMjQuNC0yNi4zOXYyNi4zOXptODAuNjQuNTUtMjIuNTEtNTguMzJoMTYuNzRsMTQuMzEgMzkuMzYgMTYuNDItMzkuMzZoMTYuNDFsLTI2LjYyIDYyLjMyYy0yLjk2IDYuOTQtNi4zOSAxMS45LTEwLjMxIDE0Ljg1LTMuOTIgMi45Ni05LjAyIDQuNDQtMTUuMzEgNC40NC0xLjMzIDAtMi42Mi0uMDgtMy44OC0uMjItMS4xOC0uMDgtMi4xNC0uMjMtMi44OC0uNDV2LTEzLjA4Yy43NC4xNSAxLjUxLjI2IDIuMzMuMzMuODEuMDggMS44MS4xMSAyLjk5LjExIDIuNzQgMCA1LjAzLS42NiA2Ljg4LTEuOTkgMS45Mi0xLjMzIDMuNDQtMy4yOSA0LjU0LTUuODh6bTcxLjU5LS41NXYtNzcuNjFoOC41NHY2OS45Nmg0Ni4yNXY3LjY1em02OS40OC02Ni4xOWMtMS40NyAwLTIuNzctLjU2LTMuODgtMS42N3MtMS42Ni0yLjQtMS42Ni0zLjg4YzAtMS41NS41NS0yLjg0IDEuNjYtMy44OCAxLjExLTEuMTEgMi40MS0xLjY2IDMuODgtMS42NiAxLjU2IDAgMi44NS41NSAzLjg5IDEuNjYgMS4xIDEuMDQgMS42NiAyLjMzIDEuNjYgMy44OCAwIDEuNDgtLjU2IDIuNzctMS42NiAzLjg4LTEuMDQgMS4xMS0yLjMzIDEuNjctMy44OSAxLjY3em00LjExIDEwLjY0djU1LjU1aC04LjIxdi01NS41NXptMTMuOTkgNTUuNTV2LTU1LjU1aDguMjF2Ni41NGMyLjE0LTIuNTEgNC43LTQuNCA3LjY1LTUuNjUgMi45Ni0xLjMzIDYuMjUtMiA5Ljg3LTIgNi4yOSAwIDExLjQzIDIgMTUuNDIgNS45OXM1Ljk5IDkuMTYgNS45OSAxNS41MnYzNS4xNWgtOC4xdi0zMy40OWMwLTQuODctMS40LTguNzUtNC4yMS0xMS42NC0yLjgxLTIuODgtNi41OC00LjMyLTExLjMxLTQuMzItMy4zMyAwLTYuMzMuNzQtOC45OSAyLjIyLTIuNTkgMS40Ny00LjY5IDMuNTgtNi4zMiA2LjMydjQwLjkxem02OC4yLTIyLjA2YzAgNC44NyAxLjQxIDguNzUgNC4yMiAxMS42NCAyLjgxIDIuODggNi41OCA0LjMyIDExLjMxIDQuMzIgMy4zMyAwIDYuMjktLjc0IDguODctMi4yMiAyLjY2LTEuNTUgNC44MS0zLjY5IDYuNDQtNi40M3YtNDAuOGg4LjJ2NTUuNTVoLTguMnYtNi40M2MtMi4xNSAyLjUxLTQuNyA0LjQtNy42NiA1LjY1LTIuODggMS4yNi02LjEzIDEuODktOS43NiAxLjg5LTYuMzYgMC0xMS41My0yLTE1LjUyLTUuOTktNC0zLjk5LTUuOTktOS4xNi01Ljk5LTE1LjUydi0zNS4xNWg4LjA5em00Ni41NyAyMi4wNiAyMS44NC0yOC42MS0yMC43NC0yNi45NGg5Ljc2bDE1Ljc1IDIwLjg1IDE1Ljc1LTIwLjg1aDkuNDNsLTIwLjUyIDI2LjgzIDIxLjk2IDI4LjcyaC05Ljc2bC0xNi45Ny0yMi42Mi0xNy4xOSAyMi42MnoiLz48L3N2Zz4='/>
        </a>
    </div>
</div>

<div class="container">
    <div class="breadcrumbs-box">
        <div class="breadcrumbs">
            {breadcrumbs}
        </div>
    </div>

    <table id="index-table">
        <thead>
            <tr>
                <th onclick="sortTable(0, 'str')">File Name ↓</th>
                <th class="size-col" onclick="sortTable(1, 'int')">File Size ↓</th>
                <th class="date-col" onclick="sortTable(2, 'str')">Date ↓</th>
            </tr>
        </thead>
        <tbody>
            {parent_row}
            {rows}
        </tbody>
    </table>
</div>

<div class="footer">
    Powered by <a href="https://pages.github.com">GitHub Pages</a> | Served by <a href="#" class="edgeone">EdgeOne</a>
</div>

<script>
function sortTable(colIndex, type) {{
    const table = document.getElementById("index-table");
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows);

    const isAsc = table.querySelectorAll("th")[colIndex].classList.toggle("asc");

    let parentRow = null;
    if (rows[0] && rows[0].querySelector(".parent-dir")) {{
        parentRow = rows.shift();
    }}

    rows.sort((rowA, rowB) => {{
        let cellA = rowA.cells[colIndex].textContent.trim();
        let cellB = rowB.cells[colIndex].textContent.trim();
        
        if (type === 'int') {{
            let numA = rowA.cells[colIndex].getAttribute("data-bytes");
            let numB = rowB.cells[colIndex].getAttribute("data-bytes");
            numA = numA ? parseInt(numA, 10) : -1;
            numB = numB ? parseInt(numB, 10) : -1;
            return isAsc ? numA - numB : numB - numA;
        }} else {{
            return isAsc ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
        }}
    }});

    if (parentRow) tbody.appendChild(parentRow);
    rows.forEach(row => tbody.appendChild(row));
}}
</script>

</body>
</html>
"""

ICON_FOLDER = '<svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>'
ICON_TEXT = '<svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>'
ICON_COMPRESSED = '<svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><circle cx="12" cy="13" r="2"/><circle cx="12" cy="17" r="2"/></svg>'
ICON_CODE = '<svg class="icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><polyline points="8 13 6 15 8 17"/><polyline points="12 17 14 15 12 13"/></svg>'

def get_file_icon(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.bz2', '.gz', '.xz', '.zip', '.tar']:
        return ICON_COMPRESSED
    elif ext in ['.xml', '.json', '.yaml', '.sh']:
        return ICON_CODE
    return ICON_TEXT

def format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    i = 0
    while size_bytes >= 1024 and i < len(units) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f}".rstrip('0').rstrip('.') + f" {units[i]}"

def make_breadcrumbs(rel_path):
    html_snippets = ['<a href="/">Home</a>']
    if rel_path == ".":
        return html_snippets[0]
    parts = [p for p in rel_path.split(os.sep) if p and p != "."]
    total_parts = len(parts)
    for i, part in enumerate(parts):
        if i == total_parts - 1:
            html_snippets.append(f"<span>{html.escape(part)}</span>")
        else:
            back_depth = "../" * (total_parts - 1 - i)
            html_snippets.append(f'<a href="{back_depth}">{html.escape(part)}</a>')
    return ' <span class="separator">/</span> '.join(html_snippets)

def generate_repo_indexes(base_dir):
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        rel_path = os.path.relpath(root, base_dir)
        if rel_path == ".":
            display_path = "/"
        else:
            display_path = f"/{rel_path.replace(os.sep, '/')}/"
        breadcrumbs_html = make_breadcrumbs(rel_path)
        parent_row = ""
        if rel_path != ".":
            parent_row = f'<tr><td><a class="item-link parent-dir" href="../">{ICON_FOLDER} ..</a></td><td class="size">-</td><td class="date">-</td></tr>'
        rows = []
        for d in sorted(dirs):
            dir_path = os.path.join(root, d)
            mtime = datetime.fromtimestamp(os.path.getmtime(dir_path)).strftime('%Y-%m-%d %H:%M:%S')
            quoted_name = urllib.parse.quote(d)
            rows.append(f'<tr><td><a class="item-link" href="{quoted_name}/">{ICON_FOLDER} {html.escape(d)}/</a></td><td class="size">-</td><td class="date">{mtime}</td></tr>')
        for f in sorted(files):
            if f in EXCLUDE_FILES or f.startswith('.'):
                continue
            file_path = os.path.join(root, f)
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            size_bytes = os.path.getsize(file_path)
            formatted_size = format_size(size_bytes)
            quoted_name = urllib.parse.quote(f)
            icon = get_file_icon(f)
            rows.append(f'<tr><td><a class="item-link" href="{quoted_name}">{icon} {html.escape(f)}</a></td><td class="size" data-bytes="{size_bytes}">{formatted_size}</td><td class="date">{mtime}</td></tr>')
        html_content = TEMPLATE.format(
            directory_plain=html.escape(display_path),
            breadcrumbs=breadcrumbs_html,
            parent_row=parent_row,
            rows="\n".join(rows)
        )
        with open(os.path.join(root, 'index.html'), 'w', encoding='utf-8') as f_out:
            f_out.write(html_content)

if __name__ == "__main__":
    generate_repo_indexes(".")
