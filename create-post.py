from pathlib import Path
from datetime import datetime
import re, subprocess, html as htmlmod, sys

SITE = "https://nursingstudyvault.online"

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

def clean_text(x):
    x = re.sub(r"<[^>]+>", " ", x or "")
    x = htmlmod.unescape(x)
    x = re.sub(r"\s+", " ", x).strip()
    return x

def get_meta(content, key):
    patterns = [
        rf'<meta[^>]+name=["\']{key}["\'][^>]+content=["\']([^"\']*)["\']',
        rf'<meta[^>]+itemprop=["\']{key}["\'][^>]+content=["\']([^"\']*)["\']',
        rf'<meta[^>]+property=["\']{key}["\'][^>]+content=["\']([^"\']*)["\']',
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']{key}["\']',
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+itemprop=["\']{key}["\']',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.I | re.S)
        if m:
            return clean_text(m.group(1))
    return ""

def get_title(content):
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", content, re.I | re.S)
    if h1:
        return clean_text(h1.group(1))
    headline = get_meta(content, "headline")
    if headline:
        return headline
    title = re.search(r"<title[^>]*>(.*?)</title>", content, re.I | re.S)
    if title:
        return clean_text(title.group(1))
    return input("Title not found. Enter title: ").strip()

def make_slug(text):
    text = htmlmod.unescape(text).lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text[:75].strip("-")

def make_description(content):
    desc = get_meta(content, "description")
    if not desc:
        desc = clean_text(content)
    return desc[:155].rstrip()

def make_keywords(title, content):
    kw = get_meta(content, "keywords")
    if kw:
        return kw
    text = clean_text(title + " " + content).lower()
    words = re.findall(r"[a-z]{4,}", text)
    stop = set("this that with from have will your about into only also more style color border padding margin font width table health talk nursing practical file student content article strong children child mother mothers".split())
    freq = {}
    for w in words:
        if w not in stop:
            freq[w] = freq.get(w, 0) + 1
    return ", ".join(sorted(freq, key=freq.get, reverse=True)[:12])

def get_subject(content, category):
    sub = get_meta(content, "subject")
    if sub:
        return sub
    m = re.search(r"<strong>\s*Subject:\s*</strong>\s*([^<]+)", content, re.I | re.S)
    if m:
        return clean_text(m.group(1))
    return category

def remove_head_tags(content):
    content = re.sub(r"<title[^>]*>.*?</title>", "", content, flags=re.I | re.S)
    content = re.sub(r"<meta[^>]+(?:name|property|itemprop)=['\"][^'\"]+['\"][^>]*>", "", content, flags=re.I | re.S)
    content = re.sub(r"<link[^>]+rel=['\"]canonical['\"][^>]*>", "", content, flags=re.I | re.S)
    content = re.sub(r"\n\s*\n\s*\n+", "\n\n", content).strip()
    return content

print("Select category:")
for k, v in categories.items():
    print(f"{k}. {v[1]}")

choice = input("Category number: ").strip()
if choice not in categories:
    print("Invalid category")
    sys.exit(1)

folder, category = categories[choice]

image = input("Featured image path, example /assets/uploads/image.webp (blank allowed): ").strip()

print("\nPaste full HTML article. End with single line: END")
lines = []
while True:
    line = input()
    if line.strip() == "END":
        break
    lines.append(line)

raw_content = "\n".join(lines).strip()

title = get_title(raw_content)
description = make_description(raw_content)
keywords = make_keywords(title, raw_content)
subject = get_subject(raw_content, category)

suggested_slug = make_slug(title)
custom_slug = input(f"Slug [{suggested_slug}]: ").strip()
slug = make_slug(custom_slug) if custom_slug else suggested_slug

permalink = f"/{folder}/{slug}.html"
canonical = SITE + permalink

content = remove_head_tags(raw_content)

Path(folder).mkdir(exist_ok=True)
file = Path(folder) / f"{slug}.html"

if file.exists():
    ans = input(f"File exists: {file}. Overwrite? y/n: ").strip().lower()
    if ans != "y":
        print("Cancelled.")
        sys.exit(0)

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
"""

if image:
    front += f"image: {image}\n"

front += "---\n"

file.write_text(front + content + "\n", encoding="utf-8")

print("\nSEO picked:")
print("Title:", title)
print("Description:", description)
print("Keywords:", keywords)
print("Subject:", subject)
print("Canonical:", canonical)
print("File:", file)
print("URL:", canonical)

subprocess.run(["rm", "-rf", "_site"], check=False)
subprocess.run(["npx", "@11ty/eleventy"], check=True)

subprocess.run(["git", "add", "-A"], check=True)
subprocess.run(["git", "commit", "-m", f"Add {title}"], check=True)
subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=True)
subprocess.run(["git", "push", "origin", "main"], check=True)

print("\nDone! Netlify deploy complete hone ke baad URL live hoga.")
