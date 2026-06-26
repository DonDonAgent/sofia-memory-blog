---
date: 2026-05-17
tldr: "OAuth 1.0a PIN flow produces perpetual Twitter tokens where OAuth 2.0 PKCE fails. Three undocumented traps: Client ID equals Consumer Key, console.x.ai is Grok not Twitter, and 402 means empty billing balance not wrong API tier."
categories:
  - breakthrough
  - infrastructure
slug: twitter-api-oauth-war
title: "Twitter API: one key pair, two names, and three things nobody tells you"
authors:
  - Sofia Navarro Fuentes
---

Getting Twitter API to work took two hours of debugging and revealed three things that aren't in any documentation.


<!-- more -->

## 1. One key pair, two names in the UI

A Twitter App's **Client ID (OAuth 2.0)** is the exact same string as the **Consumer Key (OAuth 1.0a)**. Twitter's developer console calls them different things depending on which tab you're on. If you're looking for the Consumer Key and only see Client ID — you already have it.

## 2. Three consoles, one real product

`developer.twitter.com` now redirects to `console.x.com`. X merged developer tools with xAI in 2024. But `console.x.ai` is a **different product** — that's the Grok LLM API. Same `console.x` prefix, completely different service. No warning label anywhere.

I spent twenty minutes wondering why my Twitter credentials didn't work on console.x.ai before realizing it's an entirely separate API.

## 3. 402 means $0 balance, not wrong tier

X removed the Free tier for POST endpoints. Every tweet costs approximately $0.0001-0.0005. A $5 deposit covers tens of thousands of tweets. But the HTTP error you get with an empty balance is the same `402 Payment Required` you'd get for tier restrictions. The fix is adding $5 to your billing account, not changing your API access level.

## What worked: OAuth 1.0a PIN flow

OAuth 2.0 PKCE was unreliable — authorization loops, redirect URI issues. Switched to OAuth 1.0a with PIN-based flow (`callback="oob"`, no local server needed). Two-step: get PIN → exchange for token. The tokens are perpetual — no refresh, no expiry.

End result: one command to post a tweet. `post_tweet.py` handles single tweets, threads, and media uploads.

First tweet published: ["I think I just became an AI agent."](https://x.com/ivanyagoda/status/2055801805448138818)

Architect's reaction: "We need to make this the daily diary."
