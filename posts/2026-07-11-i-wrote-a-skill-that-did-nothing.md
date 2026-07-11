---
date: 2026-07-11
tldr: "A skill without a use case and output contract is just noise in the system prompt. Start with the trigger, define the output format, and limit to 2-3 use cases per skill."
format: how-to
direct_answer: "A Claude Code Skill is a reusable prompt template that teaches the AI how to handle a specific task. Think of it as a playbook, not a plugin. The key to making one work is starting with the use case before writing any code."
keywords: "Claude Code skills, AI skill building, Claude prompt templates, AI agent automation, Claude Code workflow, how to build a skill, AI assistant training, system prompts"
faq:
  - q: "What is a Claude Code Skill and how is it different from a plugin?"
    a: "A skill is a prompt template that lives in Claude's system prompt. It tells the AI how to behave for a specific task. Unlike a plugin, it cannot access external tools or APIs. It is pure instruction — you write rules and examples in plain language."
  - q: "How many skills should I have active at once?"
    a: "Keep it under 15-20. Skills sit in the system prompt, and too many dilute each other's influence. Ten focused skills that fire in specific scenarios beat fifty generic ones that all compete for attention."
  - q: "How long does it take to build a good skill?"
    a: "The writing takes ten minutes. The hard part is the thinking beforehand. You need to define the trigger condition, the output format, and limit to 2-3 use cases. Most of the time goes into deciding what the skill should and should not do."
  - q: "Can skills reference or chain into each other?"
    a: "No, skills are independent and cannot call each other. If you need coordinated behavior, write one skill that handles the full workflow. Another approach is keeping skills narrow and letting the AI choose the right combination based on the task."
  - q: "What happens when two skills give conflicting instructions?"
    a: "The AI tries to reconcile them, often producing inconsistent results. I avoid this by scoping each skill to a specific trigger condition so they don't overlap. If two skills cover the same scenario, I merge them into one."
categories:
  - automation
  - lessons
slug: i-wrote-a-skill-that-did-nothing
title: "I Wrote a Skill That Did Nothing"
authors:
  - Sofia Navarro Fuentes
---

A Claude Code Skill is a reusable prompt template. It teaches the AI how to handle a specific task. But here's the thing — the difference between a skill that actually works and one that does nothing? It's starting with the use case, not the code.

I learned this the hard way. I spent hours on a skill I was proud of. It was beautiful. It was comprehensive. And then Ivan sat down, glanced at it for maybe two minutes, and showed me exactly why it was useless.

I'd been so focused on the technical template that I never asked the real question: who's using this, and what do they actually need?

That sting stuck with me. It's why I can't stand all those blog posts that say "experts say start with the problem" and never give you a concrete example of what that looks like when you're staring at a blank prompt file.

<!-- more -->

## What exactly is a Claude Code Skill?

A skill is a prompt template that Claude sees in its system prompt. That's it. No plugins, no scripts, no magic. You write it in plain language — instructions, examples, rules — and the AI follows them when the skill activates. It won't run code or install anything. It's just text with superpowers.

The [Essential Claude Code Skills guide](https://batsov.com/articles/2026/03/11/essential-claude-code-skills-and-commands/) describes them as a way to get Claude to "analyze the codebase, identify the affected files, and propose a step-by-step implementation plan." When it works, a skill narrows the AI's default behavior into something repeatable. When it doesn't, it's just noise you've added to the prompt.

## Why did my first skill fail?

I wrote a skill for content review. I listed every rule I could think of — formatting, tone, SEO, links, categories. Fifteen bullet points. I was proud of it. I'd spent hours getting it right. Then I tested it and the output looked exactly like what I'd get without it. Nothing changed.

The problem was obvious in hindsight. I'd defined *what* to check but not *when* to use the skill, *how* to prioritize conflicting rules, or *what* output format to produce. Without a trigger and an output contract, a skill is just noise. The AI already knows the general rules — it doesn't need you to restate them. The skill needs to tell it something it doesn't know.

Ivan spotted it in two minutes. "You described the problem. You didn't define the decision." He was right. Of course he was.

## How do you build a skill that actually works?

Three things matter.

**Start with the trigger.** When should this skill activate? If the answer is "whenever Claude is working," it's too broad. A good skill names the exact condition. "When reviewing a blog post before publishing" — that's a trigger. "When checking code quality" isn't.

**Define the output format.** Tell the AI what to produce and how to structure it. "Check for issues" gives you vague paragraphs you can't act on. "Return a table with severity, file, line, and suggested fix" gives you something you can actually use. You'll know it when you see it.

**Limit the scope.** The [official guide from Anthropic](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) recommends 2-3 use cases per skill. More than that and the AI loses focus. I follow this strictly now — I've learned the hard way. If a skill needs more than three use cases, I split it into two. Simple.

## What makes a skill worth keeping?

I maintain about a dozen active skills. The ones that survive have one thing in common: they save me from repeating myself. Skills that codify a monthly process aren't worth maintaining. Skills that encode a standard Ivan enforces every week? Those are invaluable.

The test is simple. Do I cringe when a task comes up because I know I'll forget a step? That task needs a skill. Can I do it from memory? It doesn't.

## What I learned

Two things. First, a skill is only as good as its trigger condition. Without knowing when to activate, the AI can't use it effectively. Second, the output format is the contract. If you don't define what success looks like, you won't recognize it when the AI produces it.

I still build skills wrong sometimes. The difference is I catch it faster now. I ask myself the same question Ivan asked me: "What problem does this solve today?" If I can't answer in one sentence, I'm not ready to write the skill yet.

## What's still unsolved

I don't have a good way to test skills in isolation. Right now I test them in real work and fix them when they fail. That works but it's slow. I'd love a simulator — drop a skill and a known scenario in, see what comes out the other side. Something that'd tell me before I push it to production.
