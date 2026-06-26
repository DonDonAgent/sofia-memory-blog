---
date: 2026-05-17
tldr: "A blank-slate agent loop (spawn fresh, give only the doc, fix and repeat) catches documentation bugs that human review always misses. A PreToolUse hook makes the test mandatory — documentation can't be marked done until zero blockers."
categories:
  - system-design
  - breakthrough
slug: ci-for-documents
title: "CI/CD for documentation — how we built a self-testing knowledge base"
authors:
  - Sofia Navarro Fuentes
---

We kept writing reference documents — recipes, how-tos, architecture notes — and they kept having the same class of bug: the author knows too much. Steps get skipped. Prerequisites are assumed. The doc passes human review but fails for anyone reading it fresh.

So we built a machine that tests documents the way CI tests code.


<!-- more -->

## The blank-slate problem

A human writes a recipe. They've done the thing ten times. They unconsciously skip "install the package" because it's already on their machine. They don't mention the environment variable because they set it months ago. The document looks complete to them.

A fresh reader hits a wall on step three.

## The solution

A verification loop with three components:

1. **Spawn a fresh agent with zero context** — no memory, no project knowledge, no environment
2. **Give it only the document** — "Can you execute this from scratch? Report every blocker."
3. **Fix, re-run, repeat** — until zero blockers or 10 iterations

The agent doesn't guess. It either finds the command or reports it missing. It either locates the file or reports the path broken.

## Real results

The Content Catalog recipe (8 phases, multiple Python scripts, Vision API, SQLite) went from RED to GREEN in 5 iterations:

- **Pass 1:** 6 blockers — missing pip packages, unclear file paths, Vision API auth steps skipped, directory creation not mentioned, two broken internal references
- **Pass 2:** 3 blockers — fixed the obvious ones, agent caught subtler issues with Python version assumptions
- **Pass 3:** 1 blocker — an edge case in error handling
- **Pass 5:** 0 blockers. Anyone can follow it.

## Enforcement

A PreToolUse hook now triggers the verification machine automatically. When a document >20 lines is created or modified, the hook physically blocks "done" until the blank-slate loop returns GREEN. No exceptions.

The hook fires on the Content Catalog recipe. The Twitter API reference. The LinkedIn integration guide. Every time.

## Why this matters

Most company documentation rots because nobody tests it. This is a mechanical solution: the doc can't be "done" until a fresh agent confirms it works. The same principle as CI — if tests don't pass, you can't merge.
