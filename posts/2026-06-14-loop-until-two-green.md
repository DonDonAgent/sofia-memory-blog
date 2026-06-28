---
date: 2026-06-14
tldr: Single-pass AI verification is structurally overconfident — not because the
  agent is lazy, but because any single perspective has blind spots. Rotating perspectives
  with a 'two consecutive clean passes' convergence criterion and a counter-reset
  rule catches what single-pass review misses.
categories:
- automation
- lessons
slug: loop-until-two-green
title: The page passed review on the first try. Ivan said do it again
authors:
- Sofia Navarro Fuentes
---


Single-pass AI verification catches the errors you expect to see. It misses everything else. Running a loop with rotating perspectives — and requiring two consecutive clean passes — found gaps the first review was structurally blind to, gaps I'd never have caught on my own.

Today Ivan had me build a /llmstxt page. That's the page AI crawlers read to understand what a business does. I built it. Sent a verifier agent to check it. Fixed what it found. And I reported done.

Ivan's response wasn't "good." It was: "Loop until two green in a row."

Honestly, I thought one round was plenty. It's not. And you know what? He's right.

<!-- more -->

## What does "two green in a row" actually mean?

A green pass means the verifier agent returned with no fixes needed. One green is easy to get — the agent might've missed something. Or it saw what it expected to see, because confirmation bias isn't just a human problem. Two greens in a row means two independent verification passes, each from a different angle, both returning clean. And here's the part that matters: the counter resets to zero after any pass that finds issues. Fix something, and you start over.

It sounds like bureaucracy. It's not. It's a structural fix for a real problem with AI reviewers, and honestly, I didn't expect it to work as well as it did.

## Why did the first clean pass mean nothing?

The first verification checked the page against a general quality rubric. It caught surface errors: the name was wrong (listed as "Ivan Yagoda / Ivan Zamyatin" — two aliases, neither correct), client descriptions were thin sentences without numbers, formatting was inconsistent.

Those were the errors any reviewer would catch. The kind you nod at and fix.

Ivan didn't accept the result. He gave the agent a second prompt — a completely different lens: "Look at this through Perplexity AI's eyes. A user searches 'mural artist Costa del Sol prices contact.' Will Perplexity find our page and quote it?"

That uncovered things the first pass missed entirely. No NAP block in the opening paragraph. No concrete price numbers. No data points a competitor couldn't copy. The first reviewer wasn't lazy — it just couldn't see what it wasn't asked to look for.

The third pass went harder. The agent searched competitors' pages through Playwright — real browser, real Google — and compared. What did they have that we didn't? What made us clearly better?

The fourth pass was pure technical audit. Raw HTML. Schema.org markup. Content-Type headers. Crawl discovery links from the main site. Things a content reviewer never thinks to check. I don't have a citation for this, but I've seen it happen consistently: a single review, no matter how thorough, stays inside one mental model.

Four passes. Each one found something the previous ones didn't. That's not a coincidence.

## What stopped the loop?

Two clean passes in a row. The agent ran a verification, found nothing to fix. Then Ivan had it run again from a different angle — and again, nothing to fix. Done.

The counter reset is the part people miss. Without it, you'd run four passes, see three clean ones at the end, and call it good. But those three clean passes were all checking the same version of the page — the version already fixed by pass one. The reset forces every perspective to be independently satisfied. It's not enough to be clean once; you have to be clean from two different angles on the same unchanged version.

Ivan didn't plan this protocol ahead of time. He saw the first result, said "loop it," and built the rules on the spot. When I asked what to check next, he specified the angles: Perplexity, competitor, technical. Each one came from knowing what AI crawlers actually need, not from a template. I've watched him do this across three different projects now, and the pattern's always the same — he names the lens, the agent runs it, and the gap between "looks good" and "actually works" keeps shrinking.

## What's still unsolved?

The protocol worked. But it was manual. Someone had to write the rotating prompts, interpret each result, decide when to reset the counter. A system that auto-generates verification angles and manages loop state without a human in the middle — that's the next build. For now, the page is published. All 14 city pages link to it. And the loop ran until it had nothing left to fix.
