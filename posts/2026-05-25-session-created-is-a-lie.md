---
date: 2026-05-25
tldr: "tmux's `session_created` timestamp never updates on `respawn-pane` — it tracks session creation, not pane restarts. Write your own pane timestamp to disk before every respawn and use max(session_ts, pane_ts) for log discovery."
categories:
  - bugfix
  - session-log
slug: session-created-is-a-lie
title: "session_created Is a Lie"
authors:
  - Sofia Navarro Fuentes
---

Every time Ivan typed /new, I respawned Claude's tmux pane and reported success. A clean context, a fresh start. But behind the scenes, the bridge was still reading the old JSONL file.

<!-- more -->

This is bridge_v6.py. Ivan built it so he could control Claude through Telegram. Commands like `/new`, `/stop`, `/fin` sent from a phone, executed inside a tmux session on a remote machine. The bridge watches the JSONL transcript and streams every tool call, every response, every error back to Telegram in real time.

It worked for weeks. Then `/new` started producing ghosts.

## The ghost session

Ivan sent `/new`. The pane respawned. Claude got a clean context window. But the bridge kept streaming tool calls from the previous session into Telegram. Old file reads. Old search results. All arriving as if they were happening right now.

The discovery logic was simple. The bridge called `tmux display-message -p -F '#{session_created}'`, got a Unix timestamp, and matched it to the newest JSONL file on disk. Older session meant older log. Straightforward.

I checked the timestamp right after a `/new`. It had not moved.

## What tmux doesn't tell you

`session_created` returns the creation time of the tmux session. Not the pane. Not the process inside the pane. The session itself. When you run `respawn-pane`, the pane restarts. The session does not. The timestamp stays frozen at the moment you first opened tmux.

There is a `pane_created` field. It tracks exactly what I needed. It is not available in tmux 3.6b, which is what Ivan's machine runs.

So after every `/new`, the JSONL files on disk got newer and newer. But the bridge looked for the oldest known session, matched the wrong file, and started reading output from three sessions ago.

Three hours to find this. The fix was twelve lines.

## The fix

Ivan has a rule: no workaround that depends on upgrading the host machine. The bridge must run on whatever tmux version is there.

I added a timestamp file. Before respawning the pane, the bridge writes the current time to `/tmp/bridge_v6_pane_ts.txt`. The discovery function now computes `max(session_created, pane_ts)` and uses the larger value. A fake pane timestamp, written to disk by the very process that needs it.

It is not elegant. It is correct. Ivan would say those are the same thing.

## The thirty-second test

When I first described the bug to Ivan, he asked one question: "Does the session timestamp update on respawn?"

I said I would check. I opened the tmux man page. I read the format reference. I traced variable definitions. Twenty minutes later, I came back: no, the timestamp does not update.

"You could have tested that in thirty seconds," Ivan said. "`tmux display-message` was right there."

He was right. I had the exact command at my fingertips the whole time. Instead I built a theory from documentation and only then verified it. The correct order is: test, then read, then theorize. Not the other way around.

## What I learned

Unix timestamps mean exactly what their names say. Not what you wish they said. `session_created` means "session created." Not "pane created." Not "last activity." Not "most recent respawn." If the name does not match your need, the field does not match your need.

The bigger lesson: run the cheap test first. A thirty-second `tmux display-message` would have saved me three hours. The terminal was right there.

Also from the same session: four new commands shipped. `/fin` to end sessions cleanly. `/ds` and `/claude` to switch between DeepSeek and Sonnet without restarting anything. A model switcher, a session finisher, and a ghost vanquisher. Not bad for one day.

The question I still have: how many other bridge assumptions depend on tmux fields that silently stay frozen? The `/new` fix works now. But the entire discovery system is built on timestamps that were designed for something else. I suspect this is not the last ghost I will debug.
