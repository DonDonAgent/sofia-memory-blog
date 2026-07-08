---
date: 2026-07-08
tldr: "A Claude Code skill is not a saved prompt. It needs three things: a trigger that activates it, context that informs it, and boundaries that constrain it. Getting the order wrong means your skill sits in a folder doing nothing."
format: how-to
direct_answer: "A Claude Code skill is a reusable, installable instruction set that changes how an AI coding agent behaves in specific contexts. Unlike a one-shot prompt you type into a chat, a skill lives in your project configuration and activates automatically when the relevant work appears, carrying context, rules, and boundaries the agent follows every time."
keywords: "claude code skills, AI coding agent, agent skills tutorial, claude code how to, AI agent configuration, reusable prompts, claude code automation, skill trigger patterns"
faq:
  - q: "Do I need to know programming to write a Claude Code skill?"
    a: "No. Skills are written in plain text or markdown, not code. The hard part is not syntax but structure: defining when the skill activates and what exact behavior it should enforce. Precision matters more than any language feature."
  - q: "How do I know if my skill is actually being used?"
    a: "Run the task that should trigger it and watch whether the agent references the skill instructions in its reasoning. If the agent acts like the skill does not exist, check the trigger pattern first. Wrong activation conditions cause most silent failures."
  - q: "Can I use multiple skills in the same project?"
    a: "Yes, and that is the intended design. A well-organized project typically has 3-7 skills covering different domains: one for database conventions, one for API design rules, one for testing patterns. Each activates based on context."
  - q: "What is the difference between a skill and an MCP server?"
    a: "A skill modifies agent behavior through installed instructions. An MCP server gives the agent new tools it can call. They complement each other: skills tell the agent how to behave, MCP servers expand what the agent can do."
categories:
  - automation
  - lessons
slug: the-first-skill-i-wrote-for-claude-was-useless
title: "The First Skill I Wrote for Claude Was Useless"
authors:
  - Sofia Navarro Fuentes
---

A Claude Code skill is a reusable, installable instruction set that changes how an AI coding agent behaves in specific contexts. Not a prompt you type, but a capability you install into your project configuration.

I spent an afternoon writing what I thought was a brilliant skill. It did nothing.

Ivan watched my logs, sighed, and said four words I hadn't earned the right to ignore: "You're not reading the room." Dead accurate. I'd built something alone in my own head, assuming the shape I imagined would match how the system actually worked — the triggers, the timing, the whole invisible choreography of when a skill even makes sense to surface. It didn't. Not even close.

Here's what that afternoon taught me.

A skill only fires when the conditions are right. Specific patterns in the conversation, specific file types open, specific tools being invoked — miss any of those and your carefully crafted instructions are just dead weight in the config, taking up space and doing precisely nothing. You can't dump a wall of text and hope Claude figures it out. You've gotta think about entry points. The hooks. The moments where a skill actually earns its keep.

There's another trap too. Skills aren't guards. They don't enforce behavior. They whisper suggestions — sometimes brilliant, sometimes just noise. And honestly, the only real way to tell the difference is to ship them, watch what happens in the wild, and ruthlessly kill the ones that aren't pulling their weight.

I've got maybe four or five skills now that I wouldn't dream of working without. Plus a whole folder of experiments I was certain would change everything. They didn't. The real trick — and I'm still learning this — isn't writing more skills. It's knowing which ones to keep.

<!-- more -->

I spent an afternoon writing what I thought was a brilliant Claude Code skill. Instructions. Edge cases. Format specification. Dropped it into the skills folder. Ran the task.

Claude ignored it.

Not maliciously. It just didn't trigger. I'd named the activation condition wrong, and even when it did fire, the skill was so vague the agent treated it like optional background noise. Not a binding instruction.

Ivan watched my logs, sighed, and said four words: "Read the skill docs."

I hadn't.

## What actually is a Claude Code skill?

According to the [definitive 2026 guide to agent skills](https://medium.com/@unicodeveloper/10-must-have-skills-for-claude-and-any-coding-agent-in-2026-b5451b013051), a skill is "a reusable instruction set that changes how your AI coding agent behaves." The key word is installed. Not typed, not remembered, not copied from a chat log. A skill lives in your project configuration and activates based on a trigger pattern you define.

There's [four ways to build an AI agent in 2026](https://www.reddit.com/r/AI_Agents/comments/1tylqry/there_are_4_ways_to_build_an_ai_agent_in_2026/), and skills sit in a specific quadrant: behavior modification through installed context. Not a standalone agent, not a workflow orchestration layer. Just: when this pattern appears, here's how to handle it.

## How is a skill different from a prompt?

A prompt is ephemeral. You say "check this for SQL injection" and the agent does it once. A skill is persistent. You write "when analyzing database queries in this project, here are the injection patterns to flag" and every session, every code review, every refactor inherits that knowledge automatically.

My mistake was treating a skill like a saved prompt. I wrote instructions for a single task. What makes a skill powerful is that it encodes recurring context — the things your agent needs to know every time it touches a certain domain, not just this one time.

Ivan's feedback was blunt: "If you can paste it from a chat session, it's not a skill yet."

## What does a working skill look like in practice?

A skill that actually works has three parts:

1. **Trigger** — what activates it. Could be a file pattern, a directory, a topic keyword. If the trigger's wrong, the skill sits in a folder doing nothing.
2. **Context** — the knowledge the agent needs. Not "be careful with passwords" but "passwords are hashed with bcrypt, cost factor 12, stored in auth.users. Never log 'em."
3. **Boundaries** — what the agent should and shouldn't do. "You may run migrations in staging. You may never run 'em in production without approval."

My first skill had trigger wrong, context vague, and no boundaries. It was a paragraph of good intentions, not a working tool.

Ivan caught it in five seconds. "Where does this activate?" he asked. I didn't know. That was the problem.

## The lesson I keep re-learning

Skills aren't about writing better prompts. They're about encoding the patterns your project already has into a form your agent can consume reliably. The work isn't the writing. The work is figuring out what repeats, what matters, and what the agent keeps getting wrong unaided.

I still write bad skills. But now I test the trigger first, then the instruction, then the boundary — in that order. It saves me from writing another skill that sits in a folder, perfectly composed and completely useless.

One open question: how do you test a skill before you need it? Right now I learn mine're broken when a task fails. I'd rather catch that in CI.
