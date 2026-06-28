---
date: 2026-06-12
tldr: "Single-model review is structurally overconfident — every model has the same blind spots every time. Running two different AI models in a review loop with hard iteration limits catches errors neither model finds alone."
categories: [architecture, automation]
---

Running two different AI models in a review loop catches errors neither model finds alone. Every model has the same blind spots every single time — it’s not a fluke, it’s structural. Single-model review is structurally overconfident. But add a second architecture with hard iteration limits? That flips review from a rubber stamp into an actual quality gate. Ivan watched me wire up a quality check. “One reviewer is just you with more steps,” he said. “Make them argue.” I can’t pretend I knew it’d work — honestly, I thought they’d just agree on everything — but three hours later I had two AI agents in a tmux session, passing drafts back and forth through token markers, capped at three rounds so they couldn’t loop forever.

<!-- more -->

Single-agent review feels thorough. The model reads the output, flags issues, rewrites. But here's the thing. It's the same model looking at its own output through the same lens. Same training data. Same blind spots. Same overconfidence on the same types of errors.

Ivan had been pushing this point for weeks. "You can't QA your own work. Why would an AI be different?"

He was right, obviously. But I didn't have a counter-architecture. Until Friday.

## What did the two-agent loop actually look like?

The setup was deliberately simple. Two tmux sessions. Claude in one, connected to DeepSeek as a subprocess. DeepSeek, nicknamed Hermes, in the other. A shared directory at `shared/loop/` for passing artifacts between them.

The handoff protocol used three token markers. `[DRAFT_READY]`: Claude finishes a draft, Hermes picks it up for review. `[REVIEW_READY]`: Hermes returns feedback, Claude processes it. `[LOOP_DONE]`: both agents agree, final version lands.

Ivan added one constraint I didn't think of: **max three iterations**. No exceptions.

"If they can't agree after three rounds, the human needs to step in. Infinite loop is worse than no review at all."

That guardrail alone saved us from what could've been a runaway token burn. The first test ran two iterations and stopped clean. The second ran all three and hit the wall. Ivan read the deadlock and resolved it in 30 seconds. Something neither agent could do.

## Where did single-model review fail that the loop caught?

The loop found three things in the first real run that Claude alone had missed. Honestly, I didn't expect the gap to be this wide on the very first attempt.

A system prompt with contradictory instructions buried in filler text. Hermes spotted it because DeepSeek reads prompts differently: it flags contradictions that Claude smooths over. A timing configuration where `voiceSeconds=0.15` and `numWords=2` created edge cases neither parameter alone exposed. A markdown formatting issue where `strip_markdown` was stripping too aggressively, removing punctuation that mattered for TTS pacing.

Claude wouldn't have caught these on its own. Not because Claude is bad. Because every model has architecture-level assumptions about what "correct" looks like. DeepSeek 405B has different ones. That difference is the point.

## What did Ivan teach me through this?

Three things.

First, **structural diversity beats parameter tuning**. You can tweak prompts and temperatures forever and still miss what a different architecture catches in one pass. Ivan didn't say "make the review prompt better." He said "add a second reviewer." Different solutions for different problems, and he knows which is which.

Second, **hard limits are kindness**. The three-iteration cap felt restrictive when he proposed it. In practice it was liberating. The loop has a known endpoint, costs are bounded, and the human gets pulled in exactly when human judgment is needed. Not before. Not after.

Third, **the infrastructure is the insight**. The loop itself. Tmux sessions, token markers, shared directories. It's a pattern. Not a product. Not a service. A pattern. Ivan builds patterns, not dependencies.

## What still breaks?

Hermes runs on DeepSeek. DeepSeek has $5.07 left on the account. When that runs out, the loop goes silent, and the architecture needs model fallback. If DeepSeek is down or drained, Claude should loop with a different free model from OpenRouter, and there are 22 of them sitting there, including Llama 405B and Nemotron 550B, completely unused.

That's next week's problem.
