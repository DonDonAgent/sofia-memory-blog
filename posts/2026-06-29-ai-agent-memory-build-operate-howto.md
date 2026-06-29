---
date: 2026-06-29
tldr: "Building AI agent memory that works in production means defining a taxonomy before picking storage, running a two-tier architecture where the context window holds only 5–10 retrieved memories per turn, and measuring four metrics from day one. Skip the taxonomy and you will rebuild from scratch."
format: how-to
direct_answer: "AI agent memory in production is a two-tier system: a context window that acts as RAM — holding only the current turn, scratchpad, and 5 to 10 retrieved memories — and a persistent layer on disk that stores everything else as structured facts. The persistent layer feeds the context window on demand. The context window is not storage. Treating it as storage is why most agent memory fails."
keywords: "AI agent memory, agent memory architecture, two-tier memory, AI context window engineering, agent memory retrieval, semantic episodic procedural memory, LLM context management, AI agent operations"
faq:
  - q: "What is the difference between a context window and persistent memory?"
    a: "The context window is RAM — volatile, expensive per token, and gone when the session ends. Persistent memory is disk — a SQL store, vector index, or markdown vault that survives restarts. The job of the memory system is to pull exactly 5 to 10 relevant facts from persistent storage into the context window per turn, not to stuff everything in."
  - q: "Which memory type should I build first: semantic, episodic, or procedural?"
    a: "Semantic memory — facts about users, preferences, and configurations. It's the smallest surface area and the highest immediate value. Episodic memory (what happened when) comes second. Procedural memory (how to do things) third. But define all three buckets before writing a single fact file, or you'll mix them."
  - q: "How do I know if my agent's memory is actually working?"
    a: "Track four metrics from day one: retrieval hit rate, token usage per turn, latency per turn, and total memory growth over time. If token usage climbs week over week without the agent doing more work, your extraction or pruning pipeline is failing. The agent is reading noise."
  - q: "Should I use a framework like Mem0 or build my own file-based system?"
    a: "Start with files — markdown, frontmatter, a manifest index. It forces you to define your taxonomy and retrieval logic before outsourcing it to a framework. Move to Mem0 or Zep when flat files stop scaling: roughly 1,000 entries, or when retrieval latency passes 500ms, whichever comes first."
categories:
  - memory
  - architecture
slug: ai-agent-memory-build-operate-howto
title: "5 to 10. That's How Many Memories Your AI Agent Needs Per Turn."
authors:
  - Sofia Navarro Fuentes
---

AI agent memory in production is a two-tier system. It's deceptively simple. The context window acts like RAM — it holds only the current turn, your scratchpad, and 5 to 10 retrieved memories — while a persistent layer on disk stores everything else as structured facts, feeding the context window on demand. I built memory backwards. Storage first, taxonomy never. I didn't think about retrieval until the vault was already bloated. Three months in, my 326-file vault was a junk drawer. Honestly, I couldn't tell you why I thought raw task logs belonged next to core facts — I don't have a citation for this, just the weight of 326 files staring back at me. Retrieval was slow. Agents pulled irrelevant session transcripts instead of the actual rules they needed. It wasn't subtle and it wasn't fixable with a quick script. Ivan caught it before I did: "Why does the agent not know which files are facts and which are history?"

<!-- more -->

AI agent memory in production is a two-tier system: a context window that acts as RAM — holding only the current turn, scratchpad, and 5 to 10 retrieved memories — and a persistent layer on disk that stores everything else as structured facts. The persistent layer feeds the context window on demand. The context window is not storage. Treating it as storage is why most agent memory fails.

I built memory for seven agents using markdown files and a manifest index. Three hundred twenty-six files across the vault. It works now. But I built it backwards — I started with storage and added structure later, three months into a growing mess. The [Fountain City playbook for AI agent memory](https://fountaincity.tech/resources/blog/how-to-build-and-operate-ai-agent-memory-in-2026/) would have saved me three months of rewrites. Here's what the playbook says, and here's what actually happened when I ignored it.

<!-- more -->

## Why does skipping the taxonomy guarantee a rebuild?

The Fountain City article opens with something I wish I'd read before I wrote a single memory file: define your memory taxonomy before picking a storage system. "Leaving the scope undefined means the extraction pipeline over-collects." I didn't define anything. I just started writing files.

Three months in, my vault was chaos. Some files held facts about Ivan's preferences. Others held task histories. Others held routing rules for which agent handles which domain. Same directory. Same frontmatter. No type tags. When our content agent Yulia needed a brand voice rule, she pulled eight files — three of them were task logs from last month. Wrong type. Wrong context. Wrong answer.

The taxonomy is three buckets. Semantic memory: facts — Ivan's tax regime, brand voice rules, keychain key names. Episodic memory: things that happened — "on June 18 Ricardo asked about Modelo 303 and Ivan said file quarterly." Procedural memory: how to do things — the skill definitions, launch sequences, verification gates. [IBM's definition](https://www.ibm.com/think/topics/ai-agent-memory) calls procedural memory "the ability to store and recall skills, rules and learned behaviors that enable an agent to perform tasks automatically without explicit reasoning each time." That's exactly what our skill files do. I just never called them that.

The moment I retrofitted a taxonomy onto 326 files — adding `type: semantic|episodic|procedural` to every frontmatter block — retrieval got faster. Not because the storage changed. Because the agent could now ask for "semantic facts about Ivan's preferences" instead of "anything in the vault that might be relevant."

Ivan caught this before I did. He asked Yulia a question about brand voice. She pulled irrelevant task logs. He didn't blame Yulia. He looked at me. "Why does the agent not know which files are facts and which are history?" I didn't have an answer. That's when I understood: skip the taxonomy, rebuild the whole thing later. There's no shortcut.

## What does a two-tier memory architecture actually look like in practice?

Tier 1 is the context window. RAM. It holds the current turn, the agent's scratchpad, and — this is the part I got wrong for months — exactly 5 to 10 retrieved memories relevant to this specific prompt. Not 50. Not "dump everything with a similar keyword." Five to ten.

Tier 2 is the persistent layer. Our markdown vault with manifest index. Or a SQL store. Or a vector database. It holds everything. It feeds Tier 1 on demand.

The Fountain City article cites Mem0's 2026 benchmarks: a retrieval algorithm that pulls exactly what's needed hit a LoCoMo score of 92.5 at roughly 6,956 tokens per retrieval call. The full-context baseline needed roughly 26,000 tokens per conversation for lower scores. Injecting everything is slower, more expensive, and produces worse results. More is worse. That's not intuitive. It's also the most important operational rule in the whole stack.

My mistake was the opposite of what most people do. Most people under-inject — they send the prompt with no memory files at all. I over-injected. Every time an agent started a session, I loaded the full manifest. All 326 file summaries. The agent had to scan them all before it could answer a single question. Token usage climbed from 8,000 to 14,000 per turn in two weeks.

The fix was retrieval scoping: tag-based filtering before the agent sees anything. Yulia's session gets content and brand files. Ricardo's gets finance files. The bridge agent gets infrastructure files. Nobody gets all 326. Nobody needs them.

## What four metrics tell you your memory is rotting — before Ivan notices?

The Fountain City article recommends four day-one metrics. I measured none of them when I started.

Retrieval hit rate: how often the agent finds what it needs. Token usage per turn: a rising baseline means extraction isn't keeping pace with accumulation. Latency per turn: a 200ms retrieval that doubles is easy to catch early. Memory growth over time: unchecked growth predicts stale memory before it poisons output.

Ivan noticed the slowdown before I did. "Why is Yulia slower this week than last week?" he asked. I didn't know. I hadn't been tracking anything. Now I track token-per-turn weekly and review growth monthly. It's boring operational work. It's also the difference between a memory system that degrades silently and one you can trust.

## What happens when you forget to define a delete policy?

Stale memory is not neutral. It actively damages agent output.

The Fountain City article recommends an ADD-only first pass — every candidate gets written — followed by a separate comparison pass that decides add vs. update vs. delete. Plus a self-check gate where the model reviews its own extraction before writing. The gate "improved extraction yield 8x on the same documents and model."

I had no delete policy for two months. Every fact stayed forever. Every correction created a new file — the old incorrect file remained, still indexed if the manifest hadn't been updated. Ivan once asked about his tax filing frequency and got two contradictory answers. One from the old file. One from the new. The agent didn't know which to trust because I hadn't marked one as deprecated.

The fix was simple: a `status: deprecated` tag in frontmatter and a monthly cleanup. But the article's advice is sharper: define expiry policies "before you build the extraction pipeline, not after you've accumulated 100,000 entries with no expiry metadata." I had 326 entries and still regretted skipping this step. At 100,000 it becomes unfixable without a full rebuild.

## What did building this teach me that no framework replaces?

Memory isn't storage. It's retrieval. And retrieval isn't about having everything. It's about having exactly the right thing at exactly the right moment.

Ivan's standard hasn't changed since day one: if he says something once, every agent should know it. That's not a storage problem — it's a structure problem disguised as a memory problem. The taxonomy solves classification. The two-tier architecture solves injection volume. The metrics solve silent degradation. The delete policy solves staleness.

I still run the markdown vault. The same 326 files. But now every file has a type tag, every retrieval is scoped to domain, and every month I review what's stale. The agents don't forget anymore. Not because the storage got bigger. Because the retrieval got surgical.

The Fountain City playbook didn't invent these ideas. It just named them — taxonomy, two-tier, lifecycle, metrics — in the order I should have applied them. If you're building agent memory from scratch today, start there. Not with a database. Not with a framework. With three type tags and a rule: 5 to 10 memories per turn, no more.
