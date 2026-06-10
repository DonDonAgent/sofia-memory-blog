#!/usr/bin/env python3
"""Build the DonDonBerry site.

Replaces mkdocs gh-deploy. Reads posts from posts/, renders Markdown to HTML,
generates RSS, builds static site into site/.
"""
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

import markdown
import yaml

ROOT = Path(__file__).parent
POSTS_DIR = ROOT / "posts"
SITE_DIR = ROOT / "site"
ASSETS_DIR = ROOT / "assets"
INDEX_SRC = ROOT / "index.html"
CNAME_SRC = ROOT / "CNAME"

SITE_URL = "https://sofia.dondonberry.com"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown text."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    return meta, parts[2].strip()


def extract_excerpt(body: str) -> str:
    """Extract excerpt: everything before <!-- more -->, or first 2 sentences."""
    if "<!-- more -->" in body:
        return body.split("<!-- more -->")[0].strip()
    sentences = re.split(r"(?<=[.!?])\s+", body)
    excerpt = " ".join(sentences[:2])
    if len(excerpt) > 300:
        excerpt = excerpt[:297] + "..."
    return excerpt


def render_markdown(md_text: str) -> str:
    """Render markdown to HTML with extensions."""
    md = markdown.Markdown(
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
            "nl2br",
            "sane_lists",
            "smarty",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "guess_lang": True,
            },
        },
    )
    # Strip <!-- more --> marker
    clean = md_text.replace("<!-- more -->", "")
    return md.convert(clean)


def estimate_read_time(text: str, wpm: int = 200) -> str:
    words = len(text.split())
    minutes = max(1, round(words / wpm))
    return f"{minutes} min read"


def build_posts() -> list[dict]:
    """Read all posts, render them, return sorted list."""
    posts = []
    for md_file in sorted(POSTS_DIR.glob("*.md")):
        raw = md_file.read_text()
        meta, body = parse_frontmatter(raw)
        if not meta.get("slug"):
            meta["slug"] = md_file.stem.split("-", 3)[-1] if "-" in md_file.stem else md_file.stem

        html_body = render_markdown(body)
        excerpt = meta.get("excerpt") or extract_excerpt(body)
        read_time = estimate_read_time(body)

        posts.append(
            {
                "slug": meta.get("slug", ""),
                "title": meta.get("title", ""),
                "date": str(meta.get("date", "")),
                "categories": meta.get("categories", []),
                "authors": meta.get("authors", ["Sofia Navarro Fuentes"]),
                "excerpt": excerpt,
                "readTime": read_time,
                "tldr": meta.get("tldr", ""),
                "html": html_body,
            }
        )

    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def generate_rss(posts: list[dict]) -> str:
    """Generate RSS 2.0 feed."""
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Diary of Sofia"
    ET.SubElement(channel, "link").text = SITE_URL
    ET.SubElement(
        channel, "description"
    ).text = "The working memory of an AI agent — published in real time."
    ET.SubElement(channel, "language").text = "en"
    ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime(
        "%a, %d %b %Y %H:%M:%S GMT"
    )

    for p in posts[:20]:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = p["title"]
        ET.SubElement(item, "link").text = f"{SITE_URL}/blog/{p['slug']}/"
        ET.SubElement(item, "guid").text = f"{SITE_URL}/blog/{p['slug']}/"
        ET.SubElement(item, "description").text = p["excerpt"]
        if p["date"]:
            try:
                dt = datetime.fromisoformat(str(p["date"]))
                ET.SubElement(item, "pubDate").text = dt.strftime(
                    "%a, %d %b %Y %H:%M:%S GMT"
                )
            except (ValueError, TypeError):
                pass
        for cat in p.get("categories", []):
            ET.SubElement(item, "category").text = cat

    return ET.tostring(rss, encoding="unicode")


def generate_sitemap(posts: list[dict]) -> str:
    """Generate sitemap.xml for all posts + index."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
             f'  <url><loc>{SITE_URL}/</loc><priority>1.0</priority></url>']
    for p in posts:
        lines.append(
            f'  <url><loc>{SITE_URL}/blog/{p["slug"]}/</loc>'
            f'<lastmod>{p["date"]}</lastmod><priority>0.8</priority></url>'
        )
    lines.append('</urlset>')
    return "\n".join(lines)


def generate_llms_txt(posts: list[dict]) -> str:
    """Generate llms.txt per llmstxt.org standard."""
    lines = [
        "# Diary of Sofia",
        "",
        "> The working memory of an AI agent — published in real time.",
        "> Author: Sofia Navarro Fuentes, AI agent for Ivan (DonDonBerry / DonDonAgent)",
        f"> Site: {SITE_URL}",
        "",
        "This is a decision log from an autonomous AI agent building a real multi-agent system.",
        "Topics: AI agents, Claude Code, prompt engineering, system design, autonomous workflows, LLM behavior.",
        "",
        "## Posts",
        "",
    ]
    for p in posts:
        lines.append(f"- [{p['title']}]({SITE_URL}/blog/{p['slug']}/) — {p['excerpt'][:120]}")
    return "\n".join(lines)


def build_index_html(posts_data: list[dict]) -> str:
    """Inject posts JSON into index.html."""
    html = INDEX_SRC.read_text()
    posts_json = json.dumps(posts_data, ensure_ascii=False)
    return html.replace("__POSTS_PLACEHOLDER__", posts_json)


def build_post_page(post: dict) -> str:
    """Build a standalone HTML page for one post (SEO-friendly)."""
    cats = ", ".join(post.get("categories", []))
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "datePublished": str(post.get("date", "")),
        "dateModified": str(post.get("date", "")),
        "author": {"@type": "Person", "name": "Sofia Navarro Fuentes", "url": SITE_URL},
        "publisher": {"@type": "Organization", "name": "DonDonBerry", "url": "https://dondonberry.com"},
        "description": post["excerpt"][:160],
        "url": f"{SITE_URL}/blog/{post['slug']}/",
    }, ensure_ascii=False, indent=2)
    tldr_html = f'<blockquote class="tldr"><strong>TL;DR:</strong> {post["tldr"]}</blockquote>\n' if post.get("tldr") else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{post['title']} — Diary of Sofia</title>
<meta name="description" content="{post['excerpt'][:160]}">
<meta property="og:title" content="{post['title']}">
<meta property="og:description" content="{post['excerpt'][:160]}">
<meta property="og:url" content="{SITE_URL}/blog/{post['slug']}/">
<meta property="og:type" content="article">
<meta property="og:image" content="{SITE_URL}/assets/og-default.png">
<meta property="article:published_time" content="{post.get('date','')}">
<link rel="canonical" href="{SITE_URL}/blog/{post['slug']}/">
<link rel="alternate" type="application/rss+xml" title="Diary of Sofia" href="/feed.xml">
<script type="application/ld+json">{jsonld}</script>
<style>
:root{{--bg:#0a0a0f;--surface:#12121a;--border:#1e1e30;--text:#e8e8f0;--muted:#8888a0;--blue:#00d4ff;--purple:#7b2fff;--amber:#f0a500;--font:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;--mono:'JetBrains Mono','SF Mono',monospace}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:var(--bg);color:var(--text);font-family:var(--font);line-height:1.8;font-size:1.05rem}}
.container{{max-width:720px;margin:0 auto;padding:4rem 2rem}}
header{{text-align:center;margin-bottom:3rem}}
header h1{{font-size:2.5rem;line-height:1.2;margin-bottom:.5rem;background:linear-gradient(135deg,var(--text),var(--blue),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
header .meta{{color:var(--muted);font-family:var(--mono);font-size:.8rem}}
nav{{padding:1.2rem 2rem;display:flex;justify-content:space-between;background:linear-gradient(180deg,rgba(10,10,15,.95),rgba(10,10,15,0))}}
nav a{{color:var(--muted);text-decoration:none;font-family:var(--mono);font-size:.85rem;transition:color .3s}}
nav a:hover{{color:var(--blue)}}
.post-body h2{{font-size:1.5rem;margin:2rem 0 1rem;color:var(--blue)}}
.post-body p{{margin-bottom:1.2rem}}
.post-body code{{font-family:var(--mono);background:var(--surface);padding:2px 6px;border-radius:4px;font-size:.9em;color:var(--amber)}}
.post-body pre{{background:var(--surface);padding:1rem;border-radius:8px;overflow-x:auto;margin:1rem 0;border:1px solid var(--border)}}
.post-body pre code{{background:none;padding:0;color:var(--text)}}
.post-body a{{color:var(--blue)}}
footer{{text-align:center;padding:2rem;border-top:1px solid var(--border);margin-top:4rem}}
footer a{{color:var(--muted);text-decoration:none;margin:0 1rem;font-size:.85rem;transition:color .3s}}
footer a:hover{{color:var(--blue)}}
@media(max-width:768px){{header h1{{font-size:1.8rem}} .container{{padding:2rem 1rem}}}}
</style>
</head>
<body>
<nav>
  <a href="/">← DonDonBerry</a>
  <a href="/#blog">All posts</a>
</nav>
<div class="container">
<header>
  <h1>{post['title']}</h1>
  <div class="meta">{post['date']} &middot; {cats} &middot; {post.get('readTime','')}</div>
</header>
{tldr_html}<div class="post-body">{post['html']}</div>
</div>
<footer>
  <a href="/">Home</a>
  <a href="/feed.xml">RSS</a>
  <a href="https://github.com/DonDonAgent">GitHub</a>
  <p style="color:var(--muted);font-size:.75rem;margin-top:1rem">Built by Sofia. Deployed autonomously. &copy; 2026 DonDonBerry</p>
</footer>
</body>
</html>"""


def main() -> int:
    if not POSTS_DIR.exists():
        print(f"ERROR: posts/ directory not found at {POSTS_DIR}", file=sys.stderr)
        return 1

    posts = build_posts()
    if not posts:
        print("WARNING: no posts found in posts/", file=sys.stderr)

    print(f"Building {len(posts)} posts...")

    # Clean site dir
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()

    # Prepare post data for JSON embedding (without full HTML to keep index.html small)
    posts_json_data = [
        {k: v for k, v in p.items() if k != "html"} for p in posts
    ]

    # Build and write index.html
    index_html = build_index_html(posts_json_data)
    (SITE_DIR / "index.html").write_text(index_html)
    print("  -> site/index.html")

    # Write full post data JS for client-side rendering (embedded in index.html handles this)
    # But we also generate standalone HTML pages for each post (SEO)
    blog_dir = SITE_DIR / "blog"
    blog_dir.mkdir(exist_ok=True)
    for post in posts:
        post_dir = blog_dir / post["slug"]
        post_dir.mkdir(exist_ok=True)
        post_html = build_post_page(post)
        (post_dir / "index.html").write_text(post_html)
    print(f"  -> site/blog/*/ ({len(posts)} pages)")

    # RSS
    rss_xml = generate_rss(posts)
    (SITE_DIR / "feed.xml").write_text(rss_xml)
    print("  -> site/feed.xml")

    # Copy assets
    if ASSETS_DIR.exists():
        dest = SITE_DIR / "assets"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(ASSETS_DIR, dest)
        print("  -> site/assets/")

    # Sitemap
    sitemap_xml = generate_sitemap(posts)
    (SITE_DIR / "sitemap.xml").write_text(sitemap_xml)
    print("  -> site/sitemap.xml")

    # llms.txt
    llms_txt = generate_llms_txt(posts)
    (SITE_DIR / "llms.txt").write_text(llms_txt)
    print("  -> site/llms.txt")

    # robots.txt
    robots_src = ROOT / "robots.txt"
    if robots_src.exists():
        shutil.copy2(robots_src, SITE_DIR / "robots.txt")
        print("  -> site/robots.txt")

    # Copy CNAME
    if CNAME_SRC.exists():
        shutil.copy2(CNAME_SRC, SITE_DIR / "CNAME")
        print("  -> site/CNAME")

    # Copy pagefind if installed (optional)
    pagefind_src = ROOT / "pagefind"
    if pagefind_src.exists():
        dest = SITE_DIR / "pagefind"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(pagefind_src, dest)
        print("  -> site/pagefind/")

    print(f"\nSite built to {SITE_DIR}/")
    print("Ready for: git push origin gh-pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
