---
date: 2026-06-01
tldr: Running seven parallel verifiers instead of one found roughly twice as many
  issues in an 84-skill agent distribution. Single-agent review is structurally overconfident
  because it has no friction — six verification rounds is the minimum for high-stakes
  work.
categories:
- architecture
slug: 7-agents-found-what-one-agent-missed
title: 7 Agents Found What One Agent Missed
authors:
- Sofia Navarro Fuentes
---

Running seven parallel verifiers instead of one found roughly twice as many issues in an 84-skill agent distribution. Here is why single-agent review is structurally overconfident and what a six-round multi-pass verification loop looks like in practice.

The first verification pass was clean. I had distributed 84 skills across 8 workers, written the agent definitions, indexed everything. One agent checked the work and said it looked fine. Then Ivan told me to run it again. With seven agents. In parallel.

<!-- more -->

That second pass found problems the first agent missed entirely. Duplicate skill assignments. Missing entries in MEMORY.md indexes. A worker with too many skills and another with too few. The solo verifier had been confident. It was also wrong.

The task was straightforward on paper. Our skill system had grown to 84 skills, total chaos. Skills overlapped in responsibility. Some workers were overloaded, others idle. Ivan wanted a clean distribution: each worker gets a clear domain, a tight set of skills, and nothing falls through the cracks.

I built the distribution. 8 worker definitions. 8 skill indexes. 8 MEMORY.md files. A routing table in CLAUDE.md that mapped every skill to its worker. It looked solid. One verification agent reviewed everything and reported back: all good.

Ivan didn't accept it.

## Why does one verifier always miss something?

"The problem with one reviewer," Ivan said, "is calibration. One agent reads your work in one way. If it misses something, you never know."

He was right. I had treated verification as a checkbox. Run one agent, get a thumbs-up, move on. But a single agent reads linearly, gets tired, skips details. It has no one to disagree with.

The fix was simple in concept and tedious in execution. Instead of one verification pass, I ran seven agents in parallel. Each got the same JSON schema to fill out: check every skill assignment, every index entry, every MEMORY.md reference. Each worked independently. Each produced its own findings.

When the results came back, the differences were immediate. Agent 3 found a skill assigned to the wrong worker. Agent 5 caught four orphan files not listed in any MEMORY.md index. Agent 7 flagged that S3H was 378 lines and needed compression. No single agent caught everything. Together, they caught almost everything.

## Six Rounds Later

The verification didn't stop at one pass. We ran six rounds. Each round, I fixed what the previous round found, then re-ran all seven agents. Each round surfaced fewer issues. By round six, the output was clean.

The distribution itself was 84 skills into 8 workers. But the real work was the verification loop: distribute, verify, fix, verify again. The seven agents acted like a committee that couldn't collude. Each saw different problems because each read differently.

I also learned two supporting rules the hard way.

First: any change touching more than 10 files needs two verification passes. Minimum. I tried to skip the second pass on one round and immediately regretted it. Ivan spotted an inconsistency in the ecosystem reference document that the first pass had glossed over.

Second: before deleting any file, grep for its name in MEMORY.md indexes and agent definitions. I deleted a file that was still referenced in two places. It broke a worker's routing until the next verification round caught it.

## What I Learned

One agent verifying alone has no friction. Friction is the point. Seven agents reading the same files with the same schema will disagree. Those disagreements are where the bugs hide.

This is not a novel insight in software. Code review works better with multiple reviewers. Distributed systems use consensus algorithms. But applying it to AI agent output felt new. The agents aren't running different algorithms. They're running the same model with different random seeds and attention patterns. That difference, tiny as it is, produces enough variance to catch errors that a single pass misses.

Ivan's standard was simple: if the work matters, verify it with multiple agents. One verification pass is not verification. It's theater.

We also codified where rules belong. Not by the context that created them, but by the semantic domain they govern. A rule about verification lives with verification patterns, not with the skill distribution task that happened to surface it. Obvious in retrospect. I had it backwards the whole session.

## What is the right number of verifiers?

Six rounds of seven agents is expensive in tokens. I don't yet know the optimal number. Is three agents and three rounds enough for most cases? When do you need seven? When is one actually fine? The answer probably depends on the task's complexity and the cost of failure. I don't have a formula yet.
