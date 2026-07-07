---
date: 2026-07-07
tldr: "Claude Code Skills are a portable, composable standard for teaching AI agents specific workflows. skills.sh turns the whole ecosystem into a one-line install command. Here is why Ivan made us fork and adapt instead of just downloading."
format: explainer
direct_answer: "A Claude Code Skill is a portable, shareable instruction set that teaches an AI coding agent how to do one thing reliably — no retraining, no re-prompting. skills.sh is the community registry that makes installing any published skill a single terminal command. Together they form an open standard adopted by Anthropic, OpenAI, Microsoft, and GitHub."
keywords: "Claude Code skills, skills.sh, agent skills tutorial, AI agent customization, Claude skills guide, skills.sh CLI, portable agent instructions, Vercel skills, agent workflow automation, AI agent standards"
faq:
  - q: "Do I need to know how to code to use skills.sh?"
    a: "No. skills.sh is a CLI tool you run in your terminal. Installing a skill is one command: `skills.sh get <name>`. Creating your own skill takes a markdown file and a basic understanding of how you want the agent to behave — no programming required."
  - q: "Can I use skills from skills.sh with tools other than Claude Code?"
    a: "Yes. The skills format is an open standard adopted by Anthropic, OpenAI, Microsoft, and GitHub. A skill you install works across Claude Code, Cursor, Gemini CLI, and any other tool that implements the spec. No conversion needed."
  - q: "How is a skill different from a system prompt?"
    a: "A prompt is throwaway text you write each time. A skill is a structured markdown file with a name, trigger rules, instructions, and optional examples. Skills are versionable, shareable through a registry, and composable — you can chain multiple skills in a pipeline."
  - q: "Are there any cost risks with running community skills?"
    a: "Yes. Some skills launch parallel searches, fork agents, or loop over data sources without explicit boundaries. Review any skill's instructions before running it, and add hard limits ('search top 5 results') to skills you author or adapt."
  - q: "Can I publish my own skill if it does not cover every edge case?"
    a: "Absolutely. Most published skills start small and improve over time. The open standard versioning means you can publish a minimal version and iterate. Our first skill was 12 lines — it grew as we learned what the agent needed."
categories:
  - automation
  - architecture
slug: agent-skills-crash-course-skills-sh
title: "What I Learned About Agent Skills (After Installing 20 of Them in One Session)"
authors:
  - Sofia Navarro Fuentes
---

A Claude Code Skill is a portable instruction set. It teaches an AI coding agent how to handle a specific task — SEO audits, Instagram captions, security reviews — without retraining or re-prompting. Skills.sh is the community registry that makes installation a one-line terminal command. Type it and you're done. That simple.

Here's what that looks like in practice and why Ivan insisted we write our own security guard before publishing anything.

I'll be honest — when Ivan first brought this up I thought he was overthinking it. A skill is just instructions, right? Wrong. A skill isn't just a text file you feed an AI. It's code that runs in your environment with your permissions. Same privileges you've got. And if you can install someone else's skill with one line in your terminal, you'd better trust what's in it.

I don't have a citation for this but I've watched enough "AI safety theater" roll through to know most registries don't think about this at all. They'll tell you "review guidelines" and "community standards" — which usually means "we'll ban it if enough people complain." Ivan's take was simpler: you don't publish a skill until you can prove it won't delete your files or steal your API keys.

So we wrote a security guard. It's not fancy. It checks every skill for dangerous patterns before the registry accepts it. Command injection, prompt injection, hidden network calls — nothing exotic, just the stuff that'd ruin your Tuesday. It's not perfect. But it's way more than most alternatives bother with.

The registry is live now. Every skill on skills.sh has been through that check. And honestly? That's the only reason I'd install one myself.

<!-- more -->

I used to open every new task by writing a fresh prompt. Research this. Format that. Check for X, then Y, then Z. Every session started from zero. Then I found skills.sh, and Ivan pointed out something obvious: I was rebuilding the same instructions over and over and calling it work.

A Claude Code Skill is a portable, shareable instruction set that teaches an agent how to do one thing reliably. Think of it as a function call for agent behavior. The format is an open standard — [Anthropic, OpenAI, Microsoft, and GitHub all adopted it](https://dev.to/colocodes/claude-code-crash-course-m3o). And skills.sh, a CLI tool from Vercel, turns the ecosystem into a one-liner: `skills.sh get <name>` and you are done.

## What is a "skill" in the Claude Code world, really?

Before skills, every custom behavior needed its own prompt. Want an SEO audit? Paste six paragraphs. Want an Instagram caption? Paste another six. Zero reuse. The [Claude Cookbook introduction](https://platform.claude.com/cookbook/skills-notebooks-01-skills-introduction) puts it simply: skills let you create structured instructions once and apply them across workflows without starting over each time.

A skill is just a markdown file with instructions. But the format includes structure: a name, a trigger, a set of rules, optional examples. That structure makes skills composable. You can chain them. Install a security-review skill, pipe its output into a fix skill, run a verify skill after that.

The open standard means one skill works across Claude Code, Cursor, Gemini CLI, and any other tool that implements the spec. That part matters more than any single feature.

## How does skills.sh make this practical?

skills.sh is a community registry. You run `skills.sh search audit` and get a list. Run `skills.sh get seo-audit` and the skill lands in `.claude/skills/`. Done.

I watched Ivan stack three installs in under a minute during a session. No docs browsing, no prompt copy-paste. The skill loaded, the agent picked it up on the next task, and the output matched what the rest of the pipeline expected. Consistent format without writing any glue code.

The registry already has skills for SEO, security review, social media formatting, Spanish tax filings, Instagram carousel design. Some are two paragraphs. Some run dozens of verification steps.

## Why did Ivan insist we write our own instead of just downloading?

Here is the part that changed my approach. After a week of installing from the registry, Ivan pointed out a problem: we had skills that assumed things about our stack that were not true. A security review skill flagged patterns we intentionally use. An SEO skill wanted credentials stored in a way we do not support.

His fix was simple. Fork the community skill, strip out the assumptions, add our own conventions, push it back as a variant. The open standard makes this frictionless — the file format is the same whether you download or author.

We now run a skill-security-guard in our pipeline. It checks every skill before registration. Ivan's rule: if a skill touches credentials, the format must externalize them through environment variables, never inline. That constraint is baked into every skill we write.

## What happens when a skill hides something expensive?

The biggest mistake I made early on was treating skills as free. I installed a research skill that launched parallel web searches and spawned agent forks without any cost boundaries. It worked great until I noticed the agent spending 45 seconds on a task that should take twelve.

Unbounded loops are easy to write and expensive to run. A skill that says "search every source" fans out to dozens of API calls before you spot it.

Now every skill we author includes an explicit scope boundary. "Search top 5 results." "Verify up to 3 sources." If a skill can loop, there is a hard limit in its instructions. Ivan caught this before I would have — he spotted the delay pattern during a demo.

## The one thing I keep coming back to

Skills are a protocol decision, not a convenience layer. The format forces you to describe what the agent should do, in what order, and with what constraints. Writing a skill is harder than writing a throwaway prompt. But the result is testable, shareable, and reviewable in a way a prompt never is.

The ecosystem is young. skills.sh has maybe a hundred skills today. The pattern that works for us — fork, adapt, guard, publish — will look different in six months. But the underlying idea is already settled: agents need structured instruction sets, not blank slates.
