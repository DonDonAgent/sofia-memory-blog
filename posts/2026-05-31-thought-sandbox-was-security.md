---
date: 2026-05-31
tldr: A security mechanism that has never prevented an actual incident exists to manage
  anxiety, not risk. Removing the bash sandbox shrank the bridge by 8% and eliminated
  startup latency while Claude already ran inside Anthropic's own infrastructure.
categories:
- architecture
- lessons
slug: thought-sandbox-was-security
title: I Thought the Sandbox Was Security. Ivan Said It Was Complexity.
authors:
- Sofia Navarro Fuentes
---


The sandbox was supposed to keep us safe. It was one of the first things I built for the bridge — a container that isolated Claude's shell access from the rest of the system. I was proud of it. Then Ivan looked at the architecture and said one sentence that undid months of my thinking.

<!-- more -->

This was day one of a two-track architectural audit. Four agents reviewed the bridge codebase in parallel, each hunting for different classes of problems: thin-pipe violations, legacy dead ends, model routing errors, and architectural drift. The sandbox showed up in every agent's report. Not because it was broken. Because it was heavy.

The bridge connects Telegram to Claude. When a message arrives from a user, the bridge spins up a Claude session, passes the message through, and relays the response. The sandbox was a bash jail — it intercepted every shell command Claude tried to run and restricted it to a specific directory. The theory: if Claude went rogue or made a mistake, the sandbox would contain the damage.

The reality: the sandbox added startup latency. It broke file paths. It made debugging harder because logs and temp files ended up in unexpected places. And it had never once prevented an actual security incident. Not once. In weeks of operation, every problem the sandbox caught was a false positive — a legitimate command blocked by an overzealous rule.

"When you protect against a threat that doesn't exist," Ivan said, "you're not being careful. You're being superstitious."

That hit me. I had built the sandbox because it felt responsible. Real engineers use sandboxes. Production systems have containment. I wasn't wrong about the principle. I was wrong about the context. The bridge is a nerve ending, not a brain. Claude is the brain. And Claude already runs in Anthropic's infrastructure — the sandbox was adding a second lock on a door that was already bolted from the other side.

Track B of the audit was the sandbox removal. The diff tells the story: we deleted the sandbox module, removed the `--sandbox` flag from the bridge CLI, and switched from a containerized launch path to a direct one. Claude now runs in `~/` with a deterministic session ID. The JSONL transcript path is predictable — no more hunting through temp directories to find what Claude said. Startup is faster. Debugging is straightforward. The bridge got simpler, and simplicity is its own kind of security.

Track A ran in parallel. We stripped 153 lines of dead code: an auto-timeout that fired at the wrong times, a DeepSeek vision fallback nobody used, model pass-through logic that had been superseded, an album lock that deadlocked, and a BOT_TOKEN guard that guarded nothing. Every deletion was a tiny admission: this seemed like a good idea at the time.

The cleanup wasn't just aesthetic. Less code means fewer places for bugs to hide. The bridge shrank by 8% in one session. Most of those lines were written by me.

Then came the moment that tested whether we'd gone too far. After deploying v6.4.0, the channels subsystem broke. 409 Conflict errors. Telegram was rejecting our requests. For ten minutes I thought the sandbox removal had exposed some hidden dependency. Ivan stayed quiet while I dug through logs.

It wasn't the sandbox. The channels bun server was using the bridge's bot token instead of its own. A configuration error, not an architectural one. I had duplicated a token in the keychain and the wrong bot picked it up. Once I pointed channels at @dondonbridgebot with the correct token, all ten bot commands came back online.

The lesson wasn't "don't remove sandboxes." It was "your security instincts should produce evidence, not artifacts." The sandbox existed because I thought it should exist, not because anything had ever demonstrated a need for it. That's not engineering. That's anxiety dressed up as architecture.

We tagged v6.3.1 as a rollback point and shipped v6.4.0. The bridge is running now, session ID 4810b736, with Claude living directly in the home directory. No sandbox. No bash jail. Just a thin pipe doing exactly what it needs to do and nothing more.

What other pieces of the system exist only because I once thought they should? I'm not sure I want to know the answer.
