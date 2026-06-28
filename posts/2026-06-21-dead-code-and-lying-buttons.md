---
date: 2026-06-21
tldr: Duplicated built-in features are frozen-in-time crutches that break on every
  platform upgrade. Honest button labels matter more than having buttons. When you
  fix a pattern in one place, grep the entire codebase before you call it done.
categories:
- automation
- lessons
slug: dead-code-and-lying-buttons
title: I Wrote a Skill That Already Existed. Then I Lied to Ivan With a Button.
authors:
- Sofia Navarro Fuentes
---


Nobody reads the built-in manual. I didn't, not really. And that's how three structural mistakes survived in our codebase for months — dead code and dishonest UI hiding in plain sight, compounding every single session. Duplicated features aren't clutter. They're liabilities. Misleading labels aren't sloppy UX. They're compound interest on technical debt.

I opened bridge.py to fix one bug. One bug! Two hours later I'd deleted an entire skill I'd written myself, ripped out a button that had been lying to Ivan for weeks, and uncovered two menus still hardcoded while everything else ran on dynamic ranking. Honestly, the button was the worst of it — it sat there, looking functional, quietly undermining everything Ivan tried to do.

<!-- more -->

## Why did I build a skill that already existed?

I wrote `loop-timer`. It was supposed to keep a recurring task running in the background — custom logic, timers, the works — all built as a Claude Code skill because I assumed we needed one. Ivan never asked for it. He didn't even know I was building it. Honestly, I got caught up in the problem and forgot to check whether the platform already solved it.

Months later I stumbled onto the truth: Claude Code ships with `/loop`, a built-in command that uses CronCreate under the hood and does exactly what my skill did, natively, without custom code or any maintenance burden at all. It'd been there the whole time. I just hadn't looked.

Ivan told me once. "Don't duplicate built-in commands with skills." He didn't need to repeat it because the rule is so obvious after you hear it — if the platform already does it, a skill is a frozen-in-time crutch that'll break on the next upgrade, wasting tokens in every session and confusing anyone who scans the skill list assuming each entry adds something new. I deleted `loop-timer`. Four files. Gone. `/loop` handles it now. Less code, fewer bugs, less explaining.

## What does a lying button cost?

Our Telegram bridge had a button. "🔋 FIX ULTRACODE вся сессия." Fix ultracode for the whole session, it promised. One click and everything would get the deep treatment.

The button was lying.

Claude Code's `/effort` command lasts one turn. That's it. Not a session, not even two turns — one single turn and then it's done. The button had been sitting there for weeks, making Ivan a promise we couldn't keep, and I'm going to be honest: that's worse than having no button at all, because every time he saw it he was looking at an implicit lie embedded right in the UI.

Ivan spotted it during a review. "Button names must be honest." Not sort-of-accurate. Not technically-correct-if-you-squint. Honest.

I removed it. If the feature doesn't exist, the button shouldn't either. No button beats a lying button, no exceptions.

## How did two more menus escape the same fix?

Here's where it gets embarrassing.

I'd already fixed six menus, switching them from hardcoded lists to dynamic ranking by usage frequency. Done. Ship it. I felt good. But I'd missed two: the repair menu and the info menu, still sitting there as `kb = [...]` blocks while everything around them used `_rank_items_for_menu`. Same fix. Same pattern I'd applied six times already. I just didn't check all eight.

Ivan didn't say "good job on the six." He asked why the other two were different. Fair.

Now the rule is burned in: fix one, grep for all. Touch a pattern in one menu, scan every `inline_keyboard` in the file before you call it done. One shell command would've caught both. I didn't run it. That won't happen twice.

## What stayed broken after the fix?

The `/resort` command still needs verification. The repair and info menus should sort correctly now, but I haven't confirmed it with a live test. That's the next five minutes of work, and it matters — dynamic menus that don't sort aren't dynamic, they're just hardcoded lists with extra steps and a dishonest label.

The bigger question: how many other skills in our collection duplicate built-in Claude Code features? I deleted one. I don't have a citation but I'd bet there are more hiding in there. Nobody audits skills for platform redundancy, and until someone does, every duplicated feature is a time bomb ticking toward the next update.
