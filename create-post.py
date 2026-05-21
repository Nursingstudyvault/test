from pathlib import Path
from datetime import datetime
import re
import subprocess

BASE = "https://nursingstudyvault.online"

categories = {
    "1": ("health-talk", "Health Talk"),
    "2": ("case-study", "Case Study"),
    "3": ("assignment", "Assignment"),
    "4": ("family-folder", "Family Folder"),
    "5": ("health-education", "Health Education"),
    "6": ("nursing-care-plan", "Nursing Care Plan"),
    "7": ("nursing-notes", "Nursing Notes"),
    "8": ("procedure", "Procedure"),
    "9": ("surgical-care-plan", "Surgical Care Plan"),
}

def clean_text(s):
    return " ".join((s or "").replace("\n", " ").split()).strip()

def slugify(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')

def meta_content(html, name):
    m = re.search(rf'<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\']([^"\']*)["\']', html, re.I)
    return clean_text(m.group(1)) if m else ""

def itemprop_content(html, name):
    m = re.search(rf'<meta\s+itemprop=["\']{re.escape(name)}["\']\s+content=["\']([^"\']*)["\']', html, re.I)
    return clean_text(m.group(1)) if m else ""

def title_from_html(html):
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.I | re.S)
    if m:
        return clean_text(re.sub(r'<[^>]+>', '', m.group(1)))
    h = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.S)
    if h:
        return clean_text(re.sub(r'<[^>]+>', '', h.group(1)))
    return ""

def fix_canonical(html, permalink):
    correct = BASE + permalink

    html = re.sub(
        r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']*["\']\s*/?>\s*',
        '',
        html,
        flags=re.I
    )

    if re.search(r'</title>', html, re.I):
        html = re.sub(r'</title>', f'</title>\n<link rel="canonical" href="{correct}">', html, count=1, flags=re.I)
    else:
        html = f'<link rel="canonical" href="{correct}">\n' + html

    return html, correct

print("Select category:")
for k, v in categories.items():
    print(f"{k}. {v[1]}")

choice = input("Category number: ").strip()
if choice not in categories:
    raise SystemExit("Invalid category number")

folder, category = categories[choice]

print("\nPaste full HTML content. End with a single line: END")
lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

html = "\n".join(lines).strip()

title = title_from_html(html)
description = meta_content(html, "description") or itemprop_content(html, "description")
keywords = meta_content(html, "keywords")
subject = meta_content(html, "subject") or "Nursing Practical File"

if not title:
    title = input("Title not found. Enter title: ").strip()
if not description:
    description = input("Description not found. Enter meta description: ").strip()
if not keywords:
    keywords = input("Keywords not found. Enter keywords: ").strip()

slug = slugify(title)
permalink = f"/{folder}/{slug}.html"

Path(folder).mkdir(exist_ok=True)
file = Path(folder) / f"{slug}.md"

html, canonical = fix_canonical(html, permalink)

date = datetime.now().astimezone().isoformat(timespec="seconds")

front = f"""---
layout: post.njk
title: {title}
date: {date}
description: {description}
keywords: {keywords}
subject: {subject}
permalink: {permalink}
canonical: {canonical}
category: {category}
---
"""

file.write_text(front + html + "\n", encoding="utf-8")

print("\nCreated:", file)
print("Title:", title)
print("Permalink:", permalink)
print("Canonical:", canonical)

subprocess.run(["rm", "-rf", "_site"], check=False)
subprocess.run(["npx", "@11ty/eleventy"], check=True)

subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"Add {title}"], check=True)
subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("\nDone! Netlify deploy complete hone ke baad URL live hoga:")
print(canonical)
