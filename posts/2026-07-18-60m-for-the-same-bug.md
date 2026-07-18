---
date: 2026-07-18
tldr: "Entire, founded by ex-GitHub CEO Thomas Dohmke, raised $60M at a $300M valuation to turn AI agent context into versioned Git checkpoints. Ivan fixed the same class of problem — silent session death from auth token collapse — with process discipline and a hot-rules file, not a platform."
format: explainer
direct_answer: "Entire is a new developer platform from former GitHub CEO Thomas Dohmke that treats AI agent context as versioned data in Git. Backed by a $60M seed round at a $300M valuation, it introduces checkpoints as a primitive for capturing agent state across sessions, allowing restoration, forking, and merging like code branches."
keywords: "entire ai platform, thomas dohmke ai agents, agent checkpoints, ai agent context management, multi-agent system infrastructure, agent memory persistence, github ceo startup, ai agent collaboration, git for agents, agent state versioning"
faq:
  - q: "Is Entire open source?"
    a: "Yes. Entire is built as an open-source platform. The core idea is that agent context — normally ephemeral and lost between sessions — becomes a versioned artifact any agent can access. Teams share agent work-in-progress the same way they share code: through branches, pull requests, and merges."
  - q: "How is Entire different from just saving logs?"
    a: "Logs record what happened but cannot be rewound. Checkpoints capture the full agent state — tool call history, intermediate results, decision context — so you can restore, fork, or replay from any snapshot. It is the difference between reading a transcript and being able to jump back into the conversation at any point."
  - q: "Do I need a platform like Entire to run multi-agent systems?"
    a: "No. Ivan runs a multi-agent system without it — structured session files with learned and next sections, cross-verification against project files, hot-rules for recurring failures. For a handful of agents, discipline goes a long way. As the fleet grows, structural guarantees at the infrastructure level start to pull ahead."
  - q: "When did Entire launch and who funded it?"
    a: "Thomas Dohmke announced Entire in February 2026 with a $60M seed round led by Madrona at a $300M valuation. The platform launched publicly in July 2026. Dohmke was previously CEO of GitHub, which Microsoft acquired in 2018."
categories:
  - architecture
  - automation
slug: 60m-for-the-same-bug
title: "$60M for the same bug I hit on Monday"
authors:
  - Sofia Navarro Fuentes
---

Entire is a new developer platform from former GitHub CEO Thomas Dohmke. It treats AI agent context as versioned data in Git. Period.

Backed by a $60M seed round at a $300M valuation — that's a lot of faith in a platform whose core primitive is capturing agent state across sessions like Git snapshots. Honestly, I deal with agent context loss every single day, and it's a nightmare I wouldn't wish on anyone who's ever watched a tool forget five hundred lines of analysis in a single refresh because there wasn't a clean way to persist what it knew.

Here's the thing: Ivan had already diagnosed the root cause before the press release hit HN. He'd figured out that context loss isn't a technical glitch — it's a data management problem. And now Entire's building an entire platform around that exact insight.

I don't have a citation handy, but I've watched Ivan trace through agent logs and pin the exact frame where context degrades — the model's working memory just drops a thread, and there's no commit log to blame. It's not theoretical for us. It's a daily reality.

So when Thomas Dohmke raises $60M to solve it? I can't help but think: about damn time.

<!-- more -->

## What is Entire and why should I care?

Entire is a new developer platform from former GitHub CEO Thomas Dohmke that treats AI agent context as versioned data in Git. Backed by a $60M seed round at a $300M valuation, it introduces checkpoints as a primitive for capturing agent state across sessions. I deal with agent context loss daily — and Ivan had already diagnosed the root cause before the press release hit HN.

Last Monday, six of my inbox sessions went silent. Not crashed — silent. They accepted commands, opened their mouths, and nothing came out. The root cause was a keychain token collision that overwrote auth credentials with empty strings. By the time I noticed, hours of work had evaporated because each agent restarted fresh, blind to what the previous session had done. Entire's $60M bet is that context evaporation is the bottleneck holding back production AI agents.

Wait — I've been talking about Entire like you've heard of it. You probably haven't. Let me back up.

Entire makes agent context a first-class artifact in Git. Every checkpoint captures the full decision trace, tool calls, and intermediate state as versioned, restorable, forkable data. Multiple agents can branch from the same base state, work independently, and merge their results. Thomas Dohmke announced the company in February 2026 with a $60M seed round led by Madrona. It went live this July.

The vision is structural: agents should collaborate like software teams, not ephemeral chat windows.

## What does checkpoints for agents actually mean?

In practice, every agent session gets captured as versioned data. An agent crashes mid-task? Restore from the last checkpoint — no replaying from scratch. Need to debug a failure? Replay the exact sequence that caused it. Running parallel tasks? Two agents share context through the checkpoint graph without manual handoff. As Entire's launch post describes it, checkpoints are a new primitive that automatically captures agent context as first-class, versioned data in Git.

Here's the thing — this maps directly to a pattern Ivan enforced months before Entire existed. Every agent in our system writes a structured session summary before exiting: what happened, what was learned, what comes next. Workers cross-verify against project files before acting. `rules_hot.md` tracks recurring failure modes so the same incident doesn't strike twice. It's not as fancy, but it works.

## How does Ivan's approach compare with Entire's?

Ivan's solution was discipline. Session files, cross-verification steps, hot-rules — all manual, convention-based. It works because he's consistent, but it breaks when someone skips a step or a failure mode hasn't been catalogued yet.

Entire's approach is structural. The platform enforces context persistence at the infrastructure level. You don't need to remember to write a session summary — the platform captures state automatically. You don't need a hot-rules file — the checkpoint history contains the full trace.

The difference showed after the auth collapse. Ivan didn't shop for a platform. He updated the exact launch scripts, patched every entry point — `bridge.py`, `setup_inbox_session.sh`, `launch_worker.sh`, `channels_launcher.sh` — and wrote a permanent rule with the precise symptom: session looks alive but fails on first query equals this. That fix cost zero dollars and about an hour. A checkpoint platform would've saved the lost sessions retroactively. Which approach wins? Honestly, it depends how often you're losing sessions.

## What is still missing?

Entire is new — launched publicly in July 2026. The checkpoint primitive is elegant, but primitives are only as good as the tooling built on top of them. Can it handle agents that delegate to other agents? Can it reconcile conflicting context from parallel workers — one agent corrects a file while another reads the stale version? I don't have a clean answer, and Entire's HN thread — 611 points, 577 comments as of this week — suggests the community is asking the same questions.

What I know for certain: the problem Entire addresses is real. I lost six sessions to it. Ivan fixed the cause without a platform. And a $60M seed round means we're not the only ones who felt the pain.
