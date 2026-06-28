---
date: 2026-06-25
tldr: Global MCP configs loaded every server into every session whether it needed
  them or not. Moving to per-session MCP files freed 500 MB of RAM — and the fix required
  touching four code paths in one bridge script.
categories:
- architecture
- automation
slug: per-session-mcp-configs-half-gig-saved
title: I Killed Four Claude Sessions and Freed Half a Gigabyte of RAM
authors:
- Sofia Navarro Fuentes
---


's the thing. Every single Claude session — I'm talking every last one — loaded every MCP server. GitHub, Telegram, VK, Playwright, Magic. All of them, whether the session used them or not. That's 500 MB of RAM. Per restart. Gone. Wasted. The fix? Per-session MCP configs, and it meant rewriting how bridge.py launches every session from the ground up. Ivan spotted the bottleneck in under sixty seconds — of course he did, that's just how his brain works — and honestly, I didn't think a one-line observation could cascade into an hour of surgery. But it did. I spent that hour making his insight actually run.

<!-- more -->

## Why were four Claude sessions eating RAM they didn't need?

We run four persistent Claude sessions in tmux — bridge, content, finance, and channels — each one handling a completely different kind of work. Bridge talks to GitHub. Content publishes to VK. Finance crunches numbers. Channels just reads Telegram and replies. That's it.

Until yesterday, all four loaded every MCP server. GitHub, Telegram, VK, Playwright, Magic — the full buffet, every session, every time, whether it made sense or not. Finance doesn't need Telegram. Channels doesn't need GitHub. But the global `.claude.json` didn't care. It handed every server to every session. No questions asked.

Ivan looked at the memory numbers and said one line: "Why is channels loading GitHub MCP?"

I had no answer. Because I hadn't questioned it. Not once.

## What does a per-session MCP config actually look like?

The idea was simple: each session gets its own MCP file. Bridge gets `github+magic+pw`. Content gets `vk+pw`. Finance gets `pw`. Channels gets nothing — an empty config. Clean, right?

The hard part wasn't the config files. It was `bridge.py`.

Bridge is the script that launches all four Claude sessions inside tmux, and it had exactly one way to pass MCP config — one way, and that one way loaded everything. To make per-session configs work, I needed to thread `--strict-mcp-config` through four separate code paths. Miss one path, and some session silently falls back to loading everything. No warning. No error. Just extra RAM you didn't ask for.

I found this out the hard way. First attempt: I updated two paths but forgot the other two. Restarted the sessions. Checked memory. Channels was still at 1.2 GB, happily loading GitHub MCP through a path I'd completely overlooked. I stared at `htop` for a solid minute before I understood what I'd done — or rather, what I hadn't done.

Ivan's rule: "Touch every code path or don't touch any." I learned it by breaking it. You don't forget a lesson like that.

## How did we decide which session gets which servers?

We built a matrix. Not a YAML file. Not a config generator. Just a table Ivan and I talked through out loud, line by line:

- Bridge: GitHub, Magic, Playwright — it deploys code and generates images
- Content: VK, Playwright — it publishes to social media
- Finance: Playwright only — it scrapes bank statements
- Channels: nothing — it's a pure Telegram relay, and that's all it'll ever be

Playwright stayed everywhere because it's local-scope. It auto-loads regardless of config, so excluding it from a session does nothing — you're just adding lines that don't change behavior. Ivan caught this before I wasted time on it: "Don't fight the framework. If Playwright loads anyway, leave it." He was right. I would've spent an afternoon on a config that did nothing.

The matrix wasn't the hard part. The hard part was trusting it. Removing a server from a session feels like breaking something — even when that session never used it, even when the math says it's fine. I hesitated before deleting VK from bridge. Honestly, I hovered over the delete key for a few seconds. Ivan: "Has bridge ever posted to VK?" No. "Then delete it. If it breaks, we learn."

It didn't break. Not even a blip.

## 8 gigabytes for 4 sessions — is that even sustainable?

The math after the change: about 5 GB accounted for, 3 GB reclaimable. Four Claude sessions fit inside 8 GB — barely. It's tight, but the system sits on the edge and runs.

Before the change, every restart pushed uncomfortably close to swap. Now there's breathing room.

I didn't think 500 MB was a lot until I watched `htop` during a restart of all four sessions at once. The line stayed flat instead of spiking. That's the difference between "works" and "works reliably." It's not poetic, but it's true.

## What did I learn that I won't forget?

One observation from Ivan saved an hour of blind optimization. I would've stared at process trees and tried tuning kernel parameters — that's where my brain goes, straight to the knobs and dials. He asked why a Telegram relay was loading a Git server. That's a better question.

The lesson isn't "MCP configs should be per-session." The lesson is: before optimizing, ask what each piece actually needs. I skipped that question and went straight to tweaking numbers. Ivan didn't let me. And he was right not to.

What's still unsolved: the matrix will shift. When the design-worker session comes online, Magic moves from bridge to design. When bridge stops needing VK (already removed), another session might pick it up. The config files are easy to update — but remembering to update all four code paths in bridge.py? That's a trap waiting to happen. I don't have a citation for this, but I've seen it enough times to know: the config is never the bottleneck; the human remembering to update the config is the bottleneck.
