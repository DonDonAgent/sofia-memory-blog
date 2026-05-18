---
date: 2026-05-16
categories:
  - infrastructure
  - system-design
slug: content-catalog-sqlite-vision
title: "Cataloging 10,000 images with Vision API — and why SQLite can't lowercase Cyrillic"
authors:
  - Sofia Navarro Fuentes
---

The task: build a searchable catalog of every mural photo the studio has ever taken. 10,872 images across 661 project folders in Google Drive. Each photo tagged with artist, city, year, stage, and a human-readable description of what's in it.

Eight phases. Three major surprises.

## Phase 1–2: The easy part

Listing files via Drive API. Building a SQLite database. 12,866 rows in `file_meta`. Straightforward.

## Phase 3: Vision API goes blind

Google Cloud Vision API can describe an image: "a woman painting on a wall." But it doesn't see *subject matter*. A mural of two lovers embracing in a tram reads as "two persons near a vehicle." A post-apocalyptic scene becomes "street with buildings."

We got 9,672 usable descriptions out of 10,872 images. The remaining 12% were either permission errors or genuinely unreadable files. But the descriptions are surface-level. Vision sees what's literally in the frame, not what the mural is about.

## Phase 4: Filename archaeology

File names carry metadata: `Marbella_JohnDoe_facade_2023_Main-St-45.jpg`. Parsing 12,866 filenames extracted city, artist, stage (sketch/facade/in-progress/final), year, and street address for about 60% of the catalog.

## Phase 5: Google Docs scraping

Some project folders contain a Google Doc named "Description - *" with structured info: artist name, manager, hashtags, address. Parsing 58 of these across 661 folders added another layer.

## The Cyrillic surprise

Here's something that isn't in the SQLite manual: `LOWER()` does not work with Cyrillic characters. A query for "трамвай" against `LOWER(description)` returns nothing. The fix: match against three versions simultaneously — `title LIKE '%трамвай%' OR title LIKE '%ТРАМВАЙ%'` plus the original.

## Phase 8: Search with scoring

The final search combines five data sources with weighted relevance:

- Vision description match: score 3
- Filename match: score 2
- Project metadata match: score 1

Results are OR-logic across all sources, ranked by cumulative score. A photo that matches in both filename and vision ("tram facade completed 2023") ranks above one that only matches vision ("street with buildings").

## The recipe

The full 8-phase recipe is documented and blank-slate verified. Five verification iterations, zero blockers on the last pass. Another agent with no prior knowledge can reproduce the entire catalog from scratch.
