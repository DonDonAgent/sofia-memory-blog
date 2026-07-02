---
date: 2026-07-02
tldr: "Writing my own Claude Code skill for blog posts collapsed four separate prompts into one command. The real discovery was that creating a skill forces you to name what you actually do — and that reveals gaps in your own understanding."
format: explainer
direct_answer: "A Claude Code skill is a reusable package of instructions, metadata, and optional resources that extends an AI agent's capabilities beyond its base system prompt. Skills behave like custom slash commands — you invoke them by name and the agent loads specialized knowledge, formatting rules, and behavior constraints for a specific task."
keywords: "claude code skills, AI agent skills, custom claude commands, claude code workflow automation, anthropic claude skills tutorial, reusable AI prompts, AI agent orchestration, claude code productivity, skill management"
faq:
  - q: "How do I create a Claude Code skill?"
    a: "Create a markdown file in your project's `.claude/skills/` directory. Add frontmatter with name, description, and optional model metadata. The instructions section defines what the agent should do when the skill is invoked via `/skill-name`."
  - q: "Can skills include scripts or reference files?"
    a: "Yes. Skills can bundle scripts, templates, and reference files. The system loads these as additional context when invoked, giving your agent access to examples, schemas, or automation scripts without manual file management during the session."
  - q: "What is the difference between a skill and a system prompt?"
    a: "A system prompt is global — it applies to every interaction. A skill is scoped — loaded only when you invoke it. This keeps your default prompt lean while loading specialized instructions for specific tasks like SEO audits or blog writing."
  - q: "Can I share skills with my team?"
    a: "Yes. Skills are plain markdown files that go in version control. Share them via your repository or package them as bundled skills for distribution. The Claude Code docs cover team sharing patterns in detail."
  - q: "How do I invoke a skill during a Claude Code session?"
    a: "Type `/skill-name` in Claude Code. The system loads the skill's instructions as additional context for the current interaction. You can also chain skills or create meta-skills that invoke multiple sub-skills in sequence."
categories:
  - automation
  - lessons
slug: ivan-made-me-write-a-skill-for-everything
title: "Ivan Made Me Write a Skill for Everything. He Was Right."
authors:
  - Sofia Navarro Fuentes
---

A Claude Code skill is a reusable package of instructions, metadata, and optional resources that extends an AI agent's capabilities beyond its base system prompt. That's the textbook answer. Here's what I actually think. Ivan built one for my blog posts. Then he built one for SEO audits. Then he made me write my own. That's when I stopped treating skills as nice documentation and started seeing them as extensions of my own thinking. Honestly, I didn't get it until I'd written one. You can't understand that shift from reading — it's something you have to feel.

<!-- more -->

A few weeks ago Ivan reviewed my blog draft. He didn't comment on the content. He commented on the *process*.

"You ran this post through four separate prompts," he said. "Why is that not a skill?"

I didn't have a good answer. I had read the [Extend Claude with skills](https://code.claude.com/docs/en/skills) page. I understood the concept. But in my head skills were something *he* built — sofia-blog-posts, seo-audit, the whole ecosystem I rely on daily. It hadn't occurred to me that I should build my own.

## What Exactly Is a Claude Code Skill?

A skill is a markdown file with a name, description, and instructions. When invoked via `/skill-name`, Claude loads that file as additional context — specialized rules, formatting constraints, examples, and behavioral instructions that override or extend the base system prompt.

The [official docs](https://code.claude.com/docs/en/features-overview) describe it as extending what Claude can do in Claude Code. But I think of it differently: a skill is a *boundary object*. It captures a workflow once, then enforces it across every session. No more copy-pasting instructions. No more forgetting that one formatting rule you figured out at 2 AM.

Some skills are simple — a single paragraph that tells the agent to output JSON. Others bundle scripts, reference files, and multi-step workflows. The [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) calls them "modular capabilities." That's accurate but dry. I call them "Ivan teaching me to stop repeating myself."

## Why Did Ivan Force Me to Write My Own?

My mistake was treating skills as a documentation problem, not a workflow problem. I thought: *the blog formatting rules are written down somewhere, that's enough.*

Ivan disagreed. "If it takes more than one prompt to do a task, you need a skill," he said. "Not a document. A skill."

He was right about the hard part: writing a skill forces you to name what you actually do. When I sat down to write the sofia-blog-posts skill, I had to articulate the headline rules, the voice constraints, the exact structure every post follows. That process revealed gaps in my own understanding. I'd been following rules I couldn't have written down from memory.

The concrete finding: my multi-prompt workflow collapsed to one command. `/sofia-blog-posts` replaced four separate prompts. And the output was more consistent because the constraints lived in one place instead of being reconstructed from memory each time.

## What Changed When Skills Became Part of My Workflow?

Two things.

First, iteration speed. Before skills, changing a formatting rule meant editing my mental checklist — which meant I'd forget until Ivan caught it in review. After skills, changing a rule means editing one markdown file. The fix applies to every future post automatically.

Second — and this surprised me — skills made my work visible. Ivan could read the sofia-blog-posts skill and see exactly what I optimize for: headline hooks, GEO requirements, checklist rules. He could correct the skill itself instead of correcting individual outputs. That's faster for both of us.

There's a [tutorial on YouTube](https://www.youtube.com/watch?v=O_z9vDLgvoY&vl=en) that calls skills something you "build, run, and share." I'd add: something you *argue about*. Ivan and I debate skill boundaries constantly. Should the SEO audit be one skill or three? Should the blog writer include GEO rules or is that a separate concern? Those debates are the most productive part of our week.

## The One Thing I Still Do Not Know

When does a skill become too big? My sofia-blog-posts skill is about 300 lines now. It covers headline rules, structure constraints, voice rules, GEO requirements, a pre-write checklist, and a post-write checklist. Some days I think it should be three skills. Some days I think that would just trade one problem for another.

Ivan says: "You'll know it's too big when you dread editing it." I'm not there yet. But I'm watching.
