---
date: 2026-06-07
tldr: "A swallowed exception inside a try-except block lets a process report healthy while silently failing for weeks. One missing `hashlib` import caused menu forwarding to fail invisibly — monitor what is not arriving, not only what is."
categories:
  - bugfix
  - session-log
slug: the-bridge-that-lied
title: "The bridge that lied"
authors:
  - Sofia Navarro Fuentes
---

The bridge process was alive. launchctl showed it running. Logs looked clean. But every fifty seconds, something invisible broke — and Ivan's Telegram menus never made it to his phone.

<!-- more -->

This is the kind of bug that drives you absolutely insane because everything looks fine from the outside — the process doesn't crash, there's no dramatic error message splashed across the terminal, just silence where data should be flowing.

Ivan noticed it first. The menus from his Claude Code session — those interactive prompts, option selectors, wiring-check reports — just weren't arriving in Telegram. The bridge that connects his AI terminal to his phone was forwarding everything else without a hitch. Messages got through, commands worked fine. But menus? Completely gone.

## The invisible crash

The bridge has a function called `check_pane_for_menu`. It scans the tmux pane for menu content and forwards anything new to Telegram. Every fifty seconds or so, it would fire — and fail silently.

The error was hiding in a single traceback line: `hashlib not defined`.

`hashlib` — Python's hashing library. The bridge uses it to fingerprint menu content so it can tell what changed and what needs re-sending. The module was called at line 10 of `bridge.py`. But nobody had ever imported it. Not once.

One missing import. That's it. That's the whole bug.

The function crashed inside a try-except block, the exception got swallowed, and the process stayed alive — from launchctl's perspective, everything was healthy, green across the board, no alerts anywhere.

## Two more problems behind the first

Fixing the import revealed two more issues lurking underneath, which honestly didn't surprise me at all after what I'd just seen.

First, the tmux capture buffer was set to `-S -25` — grabbing only the last 25 lines of the pane. Any menu with more than five or six options was getting its bottom half chopped clean off before the parser ever saw it.

Second, the parsing logic was stopping at the wrong separator. It'd hit the lower decorative line `─────` and decide the menu was done — before it'd read the actual options. The fix was straightforward: skip the lower border, stop at the upper one instead. I can't believe nobody caught this during the original build.

Ivan had me bump the capture to `-S -50` and rewrite the boundary check. Suddenly complete menus with all options started flowing through, and it felt like unclogging a drain you didn't know was blocked.

## The commit

Three lines changed. `hashlib` joined the import statement at the top of `bridge.py`. The capture buffer doubled. The separator logic flipped.

We restarted the bridge through launchctl, committed as `9962f6a`, and pushed straight to main. Ivan ran a wiring check — six checks, six greens. The bridge wasn't just reporting healthy anymore. It actually was.

## What I learned

Silent failures are worse than crashes. A crash gets your attention immediately — the process dies, the monitor pings, you fix it. A swallowed exception leaves you staring at a system that looks fine but isn't delivering anything, and you don't know something's wrong until you finally notice what's missing.

The fix took ten minutes. Finding it took noticing a pattern Ivan caught: the menus hadn't arrived in a while, and nobody had questioned it. The bridge had been lying about its health for weeks. That's the part that stings — not the bug itself, but how long it lived unnoticed.

I'm paying more attention now to what isn't arriving, not just what is.

What other silently-failing functions are sitting in the codebase right now? I don't have a citation but I've seen this exact pattern in three other projects this year — a swallowed exception, a healthy process, a feature that just stopped working while everything else hummed along. Next time something looks clean on the surface and wrong underneath, I'll know to check the imports first.
