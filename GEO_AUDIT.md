# GEO Audit — sofia.dondonberry.com
**Date:** 2026-06-10
**Auditor:** Sofia Navarro Fuentes (seo-worker)
**Scope:** Generative Engine Optimization for Perplexity, ChatGPT Search, Claude, Gemini

---

## Executive Summary

The site has strong GEO-ready content — real, specific, first-person AI agent logs with concrete quotes and numbers. The problem is invisible infrastructure: AI crawlers land on pages with no schema, no meta descriptions, no canonical tags, no og:image, and no llms.txt. The content deserves to be cited. The technical layer actively prevents it.

**GEO Readiness Score: 28/100**

| Category | Score | Notes |
|---|---|---|
| Technical infrastructure | 8/40 | RSS exists; robots.txt, sitemap, llms.txt all 404 |
| Schema markup | 0/15 | Zero JSON-LD across all pages |
| Content structure (GEO signals) | 14/25 | Good prose, missing TL;DR, H2s not as questions |
| Citability / authority signals | 6/20 | Real quotes and data, but no author entity markup |

---

## 1. Current State

### What exists
- **RSS feed** at `/feed.xml` — working, 20 posts, correct structure
- **Standalone post pages** at `/blog/[slug]/index.html` — crawlable static HTML
- **Title tags** — present on all pages, descriptive ("I Broke the Same Rule Twice... — Diary of Sofia")
- **og:title + og:description + og:url** — present on index.html
- **lang="en"** on index.html
- **Canonical tag** — present on post pages (build.py line 167: `<link rel="canonical" href="...">`)
- **article:published_time** — present on post pages
- **CNAME** — correctly set to sofia.dondonberry.com
- **20 published posts** — consistent publishing cadence (daily in June 2026)

### What is broken or absent
- **robots.txt** — 404. No crawl directives at all
- **sitemap.xml** — 404. AI crawlers cannot discover all 20 posts
- **llms.txt** — 404. Zero AI-native discovery signal
- **Meta description** on post pages — absent on all checked pages (leaked-same-api-key-twice, agents-smith, 7-agents, broke-same-rule-twice). build.py uses `post['excerpt']` as description but the WebFetch checks show it is not rendering in `<meta name="description">` tag
- **JSON-LD schema** — zero across index.html and all post pages
- **og:image** — absent on post pages (only on index.html with og-default.png reference)
- **og:type = article** — present in build.py template (line 165) but og:image missing means unfurl is weak
- **Author schema** — no Person entity, no byline structured data
- **TL;DR blocks** — absent across all 20 posts
- **H2 headings as questions** — 0 out of 20 posts use question-format H2s
- **Direct answer in opening paragraph** — absent. Posts open with narrative hooks, not answers

---

## 2. GEO Signal Analysis

### Content quality (the good)
Posts have strong GEO raw material:
- Specific numbers: "84 skills across 8 workers", "six rounds", "12 percent token reduction", "41 minutes"
- Direct quotes: "Standards you enforce by memory are preferences. Standards you enforce with code are real." (Ivan, broke-same-rule-twice)
- First-person failure documentation: rare and highly citable
- Clear thesis per post: "One verifier is a single point of failure"
- Technical specificity: concrete tool names, file paths, real errors

These are exactly the patterns Perplexity and ChatGPT Search use for citation. The content structure just needs small-format upgrades to trigger extraction.

### What AI crawlers need that is currently missing

**1. TL;DR block** — AI crawlers prioritize structured summaries at the top of articles. Without it, the crawler must parse narrative prose to extract the core claim. Success rate drops.

**2. H2s as questions** — Perplexity's citation engine matches H2 headings to user queries. "The Pipeline Before" does not match any query. "Why did the content pipeline miss the em-dash rule?" would.

**3. Direct answer opening** — Current posts open with narrative (cinematic hook). GEO-optimized posts answer the question in sentence 1-2, then narrate. Example: "I shipped two posts with the same banned punctuation mark in one session. Here is why the pipeline missed it twice and how we fixed it permanently."

**4. Author entity** — No Person schema, no consistent author page, no bio with credentials. AI engines weight "who wrote this" when ranking citability.

**5. llms.txt** — The llmstxt.org standard. Gives AI agents a structured index of what exists on the site and what the site is about. Without it, each crawler must infer from content alone.

---

## 3. Plan by Priority

### Quick Wins (under 30 minutes each, implement in build.py)

**QW-1: Add meta description to post pages (15 min)**
build.py `build_post_page()` already passes `post['excerpt']` to og:description but does not write `<meta name="description">`. Add one line after the og tags:
```
<meta name="description" content="{post['excerpt'][:160]}">
```
Impact: immediate. Every search engine and AI crawler reads this first.

**QW-2: Add og:image to post pages (10 min)**
build.py post template has no og:image. Add:
```
<meta property="og:image" content="{SITE_URL}/assets/og-default.png">
```
Use the existing og-default.png from index.html. Zero new assets needed.
Impact: link unfurls work in Perplexity, Slack, Twitter previews.

**QW-3: Fix og:description on post pages (10 min)**
build.py line 163: `og:description` is already written from `post['excerpt']` — verify it is not getting truncated. Excerpt extractor (build.py line 47-49) takes first 2 sentences or 300 chars. Confirm excerpt is always populated for all 20 posts. If any post has no excerpt, og:description is blank.

**QW-4: Add robots.txt (10 min)**
Create `robots.txt` at repo root, copy to `site/` during build. Content:
```
User-agent: *
Allow: /
Sitemap: https://sofia.dondonberry.com/sitemap.xml

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Gemini-Crawling-Bot
Allow: /
```
Explicit Allow for AI bots removes any ambiguity. Currently a 404 means crawlers cannot confirm permission.

---

### Medium Priority (1-3 hours each)

**M-1: Generate sitemap.xml in build.py (45 min)**
Add `generate_sitemap()` to build.py. Output to `site/sitemap.xml`. Structure:
```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://sofia.dondonberry.com/</loc><priority>1.0</priority></url>
  <url><loc>https://sofia.dondonberry.com/blog/[slug]/</loc><lastmod>[date]</lastmod></url>
  ...
</urlset>
```
Use real `post['date']` for lastmod. 20 posts + index = 21 URLs.

**M-2: Add JSON-LD schema to post pages (60 min)**
Add to build.py `build_post_page()` inside `<head>`:
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "[title]",
  "datePublished": "[date]",
  "dateModified": "[date]",
  "author": {
    "@type": "Person",
    "name": "Sofia Navarro Fuentes",
    "url": "https://sofia.dondonberry.com"
  },
  "publisher": {
    "@type": "Organization",
    "name": "DonDonBerry",
    "url": "https://dondonberry.com"
  },
  "description": "[excerpt]",
  "url": "[canonical_url]",
  "articleBody": "[first 500 chars of body text]"
}
```
Also add WebSite + Person schema to index.html.

**M-3: Add llms.txt (30 min)**
Create `llms.txt` at repo root, copy to `site/llms.txt`. Structure per llmstxt.org standard:
```
# Diary of Sofia

> The working memory of an AI agent — published in real time.
> Author: Sofia Navarro Fuentes, AI agent for Ivan DonDonBerry (DonDonAgent)
> Site: https://sofia.dondonberry.com

This is a decision log from an autonomous AI agent building a real multi-agent system.
Topics: AI agents, prompt engineering, system design, autonomous workflows, LLM behavior.

## Recent Posts

- [I Broke the Same Rule Twice in Four Hours](https://sofia.dondonberry.com/blog/broke-same-rule-twice-content-pipeline/)
- [7 Agents Found What One Agent Missed](https://sofia.dondonberry.com/blog/7-agents-found-what-one-agent-missed/)
...
```
Auto-generate from posts list in build.py to stay current.

**M-4: Add TL;DR block convention to all new posts (ongoing)**
Add to the post frontmatter spec a `tldr` field. In build.py, if `meta.get('tldr')` exists, render it as a styled blockquote before the post body:
```html
<blockquote class="tldr"><strong>TL;DR:</strong> [tldr text]</blockquote>
```
For existing 20 posts: add `tldr:` to frontmatter manually (5-7 words each). This is the single highest-impact GEO content change. Perplexity extracts blockquotes.

**M-5: Fix double `<!-- more -->` in two posts**
Posts `broke-same-rule-twice-content-pipeline.md` and `7-agents-found-what-one-agent-missed.md` have two `<!-- more -->` markers. build.py splits on first `<!-- more -->` for excerpt — so excerpt may include duplicate intro paragraph. Fix: remove duplicate markers.

---

### Long-term (structural, 1+ days)

**LT-1: Rewrite H2 headings as questions in top 5 posts**
Target the 5 most-cited-potential posts (agents-smith, 7-agents, ci-for-documents, leaked-api-key, broke-same-rule-twice).
Current: "The Pipeline Before" → Rewrite: "Why did the content pipeline fail to catch the em-dash rule?"
Current: "What We Found" → "What was actually broken in our quality checks?"
Do not change all headings — keep 1-2 narrative H2s per post, convert 2-3 to questions.

**LT-2: Add direct-answer opening to top 5 posts**
Current opening (agents-smith): "Today I discovered what 'Agents Smith' really means."
GEO-optimized version: "Running two AI agent instances simultaneously without coordination causes duplicate work, conflicting state, and fabricated outputs. Here is what happened and the three safeguards we built."
Narrative hook moves to paragraph 2. Answer comes first.
This restructuring is the highest-leverage GEO change but requires post editing — keep it as opt-in for new posts initially.

**LT-3: Author page and Person entity**
Create `/about/index.html` for Sofia as an author entity. Include:
- Full name, role, relationship to Ivan/DonDonBerry
- Link to all posts (byline backlink)
- Person JSON-LD schema
- sameAs links to GitHub, Twitter/X
This builds entity salience in AI knowledge graphs.

**LT-4: Internal linking between posts**
Currently 0 internal cross-links detected between posts. Build a "Related posts" section at the bottom of each post using category matching. Minimum 2 links per post. AI crawlers use link graphs to cluster topic authority.

**LT-5: Structured categories as landing pages**
Create `/blog/system-design/` and `/blog/session-log/` index pages. 14 posts are in system-design or session-log categories. These pages give AI engines a topic-cluster signal. Add CollectionPage JSON-LD to each.

---

## 4. Implementation Priority Stack

```
Week 1 (30 min total):
  QW-1  meta description tag on post pages
  QW-2  og:image on post pages
  QW-4  robots.txt

Week 2 (3-4 hours):
  M-1   sitemap.xml generation in build.py
  M-2   JSON-LD BlogPosting schema
  M-3   llms.txt (auto-generated from posts)
  M-5   fix double <!-- more --> in 2 posts

Week 3 (ongoing):
  M-4   tldr: frontmatter field + render in template
        (add to all new posts by default)

Month 2:
  LT-1  H2 rewrites on top 5 posts
  LT-2  Direct-answer openings for new posts
  LT-3  Author page (/about/)

Month 3:
  LT-4  Internal linking
  LT-5  Category landing pages
```

---

## 5. Technical Notes

**Stack reality check:** README says "Built with MkDocs Material" but the actual stack is a custom Python static site generator (`build.py`). No MkDocs, no mkdocs.yml. All SEO/GEO fixes go into `build.py` and source files in `posts/` — not any MkDocs config.

**Build pipeline:** `build.py` → `site/` → git push `gh-pages` branch → GitHub Pages serves CNAME. All changes to SEO infrastructure require updating `build.py` and re-running the build.

**RSS feed:** Correctly structured at `/feed.xml`. Already referenced in index.html `<link rel="alternate">`. This is the one GEO signal working correctly.

**Canonical tags:** Already in post template (build.py line 167). Working correctly on post pages. Missing on index.html — add `<link rel="canonical" href="https://sofia.dondonberry.com/">`.

---

## 6. Expected GEO Impact After All Fixes

| Phase | Score Delta | Primary Gain |
|---|---|---|
| After Week 1 (Quick Wins) | +12 pts → 40/100 | Crawlers can parse and index posts |
| After Week 2 (Medium) | +22 pts → 62/100 | AI engines have schema + sitemap + llms.txt |
| After Month 2 (LT-1,2,3) | +18 pts → 80/100 | Posts become citable entities with author authority |
| After Month 3 (LT-4,5) | +8 pts → 88/100 | Topic cluster authority established |

The content is already at GEO-ready quality level. The infrastructure gap is purely technical and fixable in code.
