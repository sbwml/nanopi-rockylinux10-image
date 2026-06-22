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
    <title>Index of {directory_plain}</title>
    <style>
        body {{ font-family: Roboto, "Segoe UI", Arial, sans-serif; margin: 40px; color: #333; background-color: #fafafa; }}
        .container {{ background: #fff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 24px; max-width: 1000px; margin: 0 auto; }}
        .breadcrumbs {{ font-size: 20px; color: #202124; margin-bottom: 20px; padding-bottom: 14px; border-bottom: 1px solid #e0e0e0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 400; }}
        .breadcrumbs a {{ color: #1a73e8; text-decoration: none; display: inline !important; padding: 0; margin: 0; width: auto !important; }}
        .breadcrumbs a:hover {{ text-decoration: underline; }}
        .breadcrumbs span {{ color: #202124; display: inline !important; padding: 0; margin: 0; }}
        .breadcrumbs .separator {{ margin: 0 6px; color: #5f6368; font-weight: normal; user-select: none; display: inline !important; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th, td {{ padding: 12px 16px; border-bottom: 1px solid #f0f0f0; }}
        th {{ font-weight: 500; color: #70757a; background-color: #f8f9fa; }}
        tr:hover {{ background-color: #f1f3f4; }}
        td a {{ color: #1a73e8; text-decoration: none; font-weight: 500; display: inline-block; width: 100%; }}
        td a:hover {{ text-decoration: underline; }}
        .parent-dir {{ font-weight: bold; color: #5f6368; }}
        .size, .date {{ color: #70757a; font-size: 14px; }}
    </style>
</head>
<body>
<div class="container">
    <div class="breadcrumbs">
        {breadcrumbs}
    </div>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Last Modified</th>
                <th>Size</th>
            </tr>
        </thead>
        <tbody>
            {parent_row}
            {rows}
        </tbody>
    </table>
</div>
</body>
</html>
"""

def get_readable_size(size_in_bytes):
    if size_in_bytes >= 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.2f} MiB"
    elif size_in_bytes >= 1024:
        return f"{size_in_bytes / 1024:.2f} KiB"
    return f"{size_in_bytes} B"

def make_breadcrumbs(rel_path):
    if rel_path == ".":
        return "<span>Index of /</span>"
        
    parts = [p for p in rel_path.split(os.sep) if p and p != "."]
    total_parts = len(parts)
    
    html_snippets = ['<a href="' + '../' * total_parts + '">Index of</a>']
    
    for i, part in enumerate(parts):
        if i == total_parts - 1:
            html_snippets.append(f"<span>{html.escape(part)}</span>")
        else:
            back_depth = "../" * (total_parts - 1 - i)
            html_snippets.append(f'<a href="{back_depth}">{html.escape(part)}</a>')
            
    return '<span class="separator">/</span>'.join(html_snippets) + '<span class="separator">/</span>'

def generate_repo_indexes(base_dir):
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        rel_path = os.path.relpath(root, base_dir)
        display_path = "/" if rel_path == "." else f"/{rel_path}/"
        
        breadcrumbs_html = make_breadcrumbs(rel_path)
        
        parent_row = ""
        if rel_path != ".":
            parent_row = '<tr><td><a class="parent-dir" href="../">📁 ..</a></td><td class="date">-</td><td class="size">-</td></tr>'
            
        rows = []
        
        for d in sorted(dirs):
            dir_path = os.path.join(root, d)
            mtime = datetime.fromtimestamp(os.path.getmtime(dir_path)).strftime('%Y-%m-%d %H:%M:%S')
            quoted_name = urllib.parse.quote(d)
            rows.append(f'<tr><td><a href="{quoted_name}/">📂 {html.escape(d)}/</a></td><td class="date">{mtime}</td><td class="size">-</td></tr>')
            
        for f in sorted(files):
            if f in EXCLUDE_FILES or f.startswith('.'): 
                continue
                
            file_path = os.path.join(root, f)
            mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            size = get_readable_size(os.path.getsize(file_path))
            quoted_name = urllib.parse.quote(f)
            rows.append(f'<tr><td><a href="{quoted_name}">📄 {html.escape(f)}</a></td><td class="date">{mtime}</td><td class="size">{size}</td></tr>')
            
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
