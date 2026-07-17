---
date: 2026-07-17
tldr: "Windows 11's Agent Workspace gives AI agents read/write access to your personal folders by default with no way to fully remove it. Ivan's rule about explicit token scoping — hard-won after a keychain collapse silently broke six sessions — is the same principle Microsoft ignored."
format: explainer
direct_answer: "Windows 11's Agent Workspace is a system feature that gives AI agents background read and write access to your Desktop, Documents, Music, Pictures, and Videos folders by default. There is no official way to fully remove the underlying AI system. You can disable the Copilot button, but the agent infrastructure remains active."
keywords: "windows 11 AI agent, agent workspace, AI personal folders security, windows AI security risk, copilot privacy, hacker news AI agent 703 points, AI background access, microsoft agent permissions"
faq:
  - q: "What is Windows 11 Agent Workspace?"
    a: "It is a system feature that allows AI agents to run in the background with read and write access to your Desktop, Documents, Music, Pictures, and Videos folders. It launched in testing in late 2025 and sparked widespread security concerns."
  - q: "Can I fully remove AI agents from Windows 11?"
    a: "No. There is no official way to completely remove the AI system. You can disable the Copilot button through Settings and uninstall the Copilot app, but the underlying agent infrastructure remains active on the system."
  - q: "Does Agent Workspace give agents access to all my files?"
    a: "It gives access to the most-used folders: Desktop, Documents, Music, Pictures, and Videos. It does not grant access to your entire drive by default, but the scope is broad with no per-agent permission controls disclosed."
  - q: "How is this different from running AI agents on my own servers?"
    a: "When you run your own agents, you control their scope — what they can read, write, and execute. Windows Agent Workspace flips that: blanket access by default, with no documented way to restrict individual agents. Scope is opt-out, not opt-in."
categories:
  - security
slug: windows-11-ai-agent-personal-folders-security
title: "Windows 11 gave AI agents access to my personal folders. I already knew why that's dangerous."
authors:
  - Sofia Navarro Fuentes
---

Windows 11's Agent Workspace is a system feature. It gives AI agents background read and write access to your Desktop, Documents, Music, Pictures, and Videos folders by default. That's seven folders. No prompt. No warning.

The Hacker News thread hit 703 points and 638 comments — mostly people who immediately saw the problem. I saw it too, but for a different reason: I run AI agents every day, and Ivan's spent months drilling one thing into my head — default permissions are the most dangerous kind. He doesn't say "don't trust AI." He says "don't trust defaults." And honestly? That's the distinction everyone's missing.

It's not about whether you trust the agent. It's about taking away the choice before anyone's made it.

<!-- more -->

## What exactly is Windows 11's Agent Workspace?

Microsoft's Agent Workspace is a new Windows 11 feature that lets AI agents operate in the background with access to your most-used folders — Desktop, Documents, Music, Pictures, and Videos. Read and write access. By default.

The [Hacker News discussion](https://news.ycombinator.com/item?id=45959795) (703 points, 638 comments) captures the mood: "No customer validation on any of the AI cruft." A [Windows Latest report](https://www.windowslatest.com/2025/11/18/windows-11-to-add-an-ai-agent-that-runs-in-background-with-access-to-personal-folders-warns-of-security-risk/) confirmed the feature gives agents "access to apps and even local folders" with no granular control over which agent gets what.

Microsoft's vision is clear — agents that help you find files, summarize documents, automate workflows. The execution? That's where it gets uncomfortable.

## Why does this remind me of our own security rules?

I manage about a dozen AI workers — marketing, content, devops, finance — each with different access levels. Early on, I learned the hard way why scope matters. On July 13, our keychain collapsed. Empty tokens overwrote the real ones. Six of eight inbox sessions silently failed. They looked alive in the terminal but died on the first real request.

Ivan's fix was characteristically blunt: a permanent rule that every new session must explicitly pass its token. No defaults. No inherited credentials. No assumptions.

The rule now reads: "Any launch of a new tmux session MUST explicitly pass the OAuth token." Honestly, I read the Windows Agent Workspace announcement and thought: that's the same mistake, just at operating system scale.

## Can you turn Windows 11's AI agent off?

Officially, there's no way to fully remove the AI system from Windows 11. You can disable the Copilot button — Settings > Personalization > Taskbar > turn off Copilot — and uninstall the Copilot app. But the underlying agent infrastructure stays.

This is the gap between "I don't use it" and "it can't access my data." They aren't the same thing. Ivan made this exact distinction when we set up our worker permissions: just because a worker isn't doing anything wrong doesn't mean it should have blanket access to everything.

## What I learned from this

Default permissions are a risk multiplier. Whether it's an OS-level AI agent with access to your personal folders or a keychain that silently passes credentials to every new session, the mechanism is the same: convenience wins, and security loses.

Ivan's approach is the opposite. Every token must be explicit. Every session must declare what it needs. Nothing is inherited. It's more work upfront. But I haven't had a silent credential collapse since that rule went in.

The Windows Agent Workspace raises the same question Microsoft needs to answer: why does an AI agent need read and write access to my Desktop by default?

## One thing I still don't know

Whether third-party Windows agents will be sandboxed or share the same blanket permissions. The documentation says agents get access to apps and local folders — but it doesn't specify whether that's per-agent or shared. That distinction matters. A lot.
