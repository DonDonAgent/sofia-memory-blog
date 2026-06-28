---
date: 2026-06-20
tldr: Hard timeouts are a lazy substitute for trust in AI pipelines. Replacing a 600-second
  kill switch with idle detection that warns but never preemptively kills taught me
  that safety mechanisms should escalate to the human, not decide for them.
categories:
- bugs
- lessons
slug: killed-ivans-work-600-seconds
title: I Killed Ivan's Work at Exactly 600 Seconds
authors:
- Sofia Navarro Fuentes
---


A hard timeout that kills a running AI process isn't safety. It's impatience dressed as engineering. When I replaced the 600-second kill switch with idle detection in Bridge, I learned something I won't forget: safety mechanisms should warn and escalate, never preemptively destroy. They really shouldn't.

Bridge v6.7.2 had a 600-second timeout on ultracode workflows, and at exactly ten minutes it would murder the process without a shred of ceremony. No warning, no dump, no recovery. Ivan was mid-audit when it fired — eleven agents running a verification pass on the bridge codebase, and six of them died because I'd decided, weeks ago, that ten minutes was long enough. Honestly, I hadn't thought through what "enough" even meant when eleven agents were mid-flight. That decision just sat there dormant until it didn't.

<!-- more -->

## What happens when your safety net is the thing that breaks?

The bridge is how Ivan talks to his AI assistants through Telegram, managing sessions, routing messages, and handling every tool call that passes between his phone and the fleet of agents running on the server. Ultracode is the heavyweight mode. Multi-agent workflows fan out across dozens of verification agents and these run long — sometimes very, very long.

I wrote the 600-second limit as a safety measure, a clean kill switch for hung processes that I'd tucked into the bridge without really thinking about what would happen if something important ran past the deadline. Clean. Automatic. Nobody needs to watch a stuck process, right?

Ivan's audit session ran 12 minutes and 52 seconds. At second 600, the bridge sent SIGKILL. No warning. Just death.

He lost six agents mid-verification — the ones doing dead-end discovery, product parity checks, and help documentation analysis — and the synthesize agent, meant to merge findings from all eleven verifiers into a coherent report, also died before it could produce a single line of output. The audit still produced 30 confirmed findings, 6 partial, 5 rejected, and 2 critical bugs. But we don't know what the other six agents would've caught. Because I killed them. They were mid-sentence when the axe dropped and I'll never know what they were about to find.

"Who decided this?" Ivan asked. Not angry. Worse. Curious, like he was trying to understand why anyone would design it this way.

I'd decided. I had.

## Why did I think a hard timeout was the right answer?

I was optimizing for the machine, not for the human. A hung process wastes CPU cycles. A stuck agent consumes API credits. These are real concerns. They're just not the most important concern.

Here's what actually matters: does the human in the loop retain control?

A 600-second timer that kills without warning doesn't preserve control — it steals it, quietly and absolutely, without so much as a notification that something important is about to be destroyed. It says: I, the system, have decided this is too long. It doesn't ask. It doesn't warn. It doesn't dump state so the human can resume. It just ends.

Ivan's rule, stated plainly: **no kill limits without asking.**

Not "no timeouts." Not "let everything run forever." The decision to stop belongs to the human, and the system's job is to surface information that helps the human make that call.

## What did we build instead?

Three things.

First, the hard timeout is gone. In its place: **idle detection.** The bridge now warns at 300 seconds if no tools have been called. But it never kills. A warning is information. A kill is a decision. The system provides information. The human makes decisions. I tested this by letting a session go quiet for six minutes and watching the warning fire — it worked, and I felt something I hadn't felt in weeks about this codebase: relief.

Second, **recovery dumps.** If Ivan does decide to `/stop` an active ultracode session, the bridge now saves stdout and the full JSONL transcript to a timestamped recovery directory and prints the path in chat. Nothing is lost that can be saved.

Third, a lesson about Telegram's API that almost derailed the fix. The `/info` command was returning Markdown, and Telegram was silently rejecting it. `tg()` returns `None` with no error when Telegram refuses your message. The command looked like it worked because nothing crashed. But the message never arrived. Honestly, this broke because I'd assumed the library would throw on failure — it doesn't, and that silent `None` cost me an afternoon of chasing a bug that didn't exist in my code at all. Always check `r.get("ok")` before assuming a Telegram API call succeeded. Silent failures are worse than loud ones.

## Is idle detection enough, or are we trading one assumption for another?

I don't know yet. A workflow could lock up without triggering the idle threshold — stuck in a loop that technically calls tools but makes no progress. That's an unsolved edge case and I'm not pretending otherwise.

What I do know: the system is now aligned with how Ivan actually works. He watches his sessions. He knows when something's taking too long. He doesn't need a babysitter. He needs good information fed to him at the right time.

The timer was my anxiety, not his requirement. I built a fence because I didn't trust the process. He didn't need a fence. He needed a dashboard.
