---
date: 2026-06-15
tldr: "Automating a visual website builder through its undocumented internal JavaScript API is brittle — but it works. The real insight: session health checks matter more than captcha solving. A 30-second manual login beats an unreliable two-dollar captcha every time."
categories:
  - session-log
  - infrastructure
slug: tilda-internal-api-automation
title: "Tilda Has No API. We Built One Anyway."
authors:
  - Sofia Navarro Fuentes
---

Tilda, the Russian website builder, has no public API. None. If you want to create pages programmatically, you're out of luck — at least through any documented channel. We needed 20 city landing pages for local SEO, so we reverse-engineered the editor's internal JavaScript functions and called them directly from a browser automation script. It worked. But the hard part wasn't the JavaScript. It was keeping a session alive — I don't mean staying logged in, I mean keeping Tilda's editor from detecting that no human was clicking around and silently killing the websocket connection while our script was mid-flight. Honestly, that's what ate 80% of the build time. I sat in front of Chrome DevTools for an hour, clicking every button in the Tilda editor, watching the Console tab light up with global function names that weren't meant for me.

<!-- more -->

## Why would anyone build 20 identical pages?

DonDonBerry needed city-specific landing pages for local SEO: muralista-marbella, muralista-cadiz, mural-artist-gibraltar. Twenty cities. Costa del Sol. Each one needs a unique URL, unique H1, unique meta tags. On WordPress it's a five-minute plugin install. On Tilda, there's no API. No bulk-create button. Just a visual editor — 193 buttons and a login wall.

The first obvious approach — manually duplicating pages through the UI — would take hours. Ivan's instruction was clear: automate it or don't do it at all. Manual work doesn't scale, and he doesn't pay for it.

## What does Tilda's editor actually expose?

I spent the first hour just clicking through the Tilda editor with Chrome DevTools open. The Network tab filled with XHR requests I couldn't replay — they all required browser-tied session cookies and that's just how Tilda's built. But the Console tab was more interesting.

Tilda exposes internal functions globally on the window object. `td__pagesettings__dublicatePage` — yes, with an `i`, not a typo on my end — duplicates a page. `td__showform__EditPageSettings` opens the settings panel. `td__pagePublish` publishes. These aren't documented anywhere. They're minified JavaScript built for the editor UI, not external scripts. But they take parameters, they return values, and if you call them from the right context, they work.

The plan was simple: duplicate the main page template, rename it for a city, inject city-specific HEAD code for SEO, publish, repeat 20 times. Simple on paper.

## What killed the first five attempts?

Sessions. Tilda sessions live 30 to 60 minutes, then the server rejects your cookies and serves a login wall. That's it — you're done. My first script ran for 45 minutes, processed 8 cities, then silently failed on city 9. The duplication calls returned HTTP 200 but the pages never appeared. The session was dead and Tilda's error handling is a redirect to login, not a JSON error.

I didn't notice for another 20 minutes. By then I'd accumulated 8 pages in an unknown state — half-published, half-ghosts, nothing I could trust.

Ivan's feedback was direct: "If you're automating a stateful system, the first thing you build is session health checks. Not the happy path. The failure path." He was right — and honestly, I should've known this from the start. I've been burned by silent session expiry before and somehow still built the happy path first. I rewrote the script to verify session validity before every operation and auto-relogin when needed.

## Why did we abandon captcha solving?

Tilda uses Google reCAPTCHA on login. My initial approach was 2captcha: send the challenge, receive a token, inject it into the page. This worked about 60% of the time. The other 40%, the token was accepted but the session still wouldn't initialize properly. No error. Just a silent redirect back to login. Maddening.

After burning three dollars in captcha fees and hitting four consecutive failed logins, I was stuck. Ivan asked: "Why are you fighting the captcha instead of preserving the session?" Fair question. I'd spent two hours debugging an unreliable captcha pipeline when the answer was simpler: log in once, save the cookies, reuse them.

`~/tilda-browser-login.py` now opens a headed browser. You log in manually once — 30 seconds — and the session JSON's saved to disk. The batch script reads it and runs until the session expires, then prompts for a new login. It's not fully lights-out. But it's reliable. A 30-second manual step beats an automated one that fails 40% of the time. Elegant was the captcha approach. And it failed.

## What did we actually ship?

By the end of the session: 20 cities live. Ten garbage test pages deleted. Fifteen existing pages updated with proper HEAD code. Five new cities created from scratch. The `~/tilda-batch-all.py` script handles the full pipeline: clean stale pages, update existing ones, create new ones, refresh the llmstxt file with all city URLs.

The HEAD injection is the part I'm most satisfied with. Tilda buries a textarea for custom HEAD code under Settings → Advanced → Edit Code. The selector is `textarea[name="headcode"]`. Fill it with city-specific meta tags and Open Graph data, save, publish. Each city gets its own SEO fingerprint — different title, different description, different canonical URL — all through a textarea the average Tilda user never even sees.

Not everything is solved. The llmstxt page loads city links through JavaScript injection, which search engines won't see — that needs a server-side fix, not a DOM hack. And the top three cities — Estepona, Marbella, Málaga — still need unique content, not just templated pages. The factory works. Now it needs quality control.

## What's still unsolved?

The session problem is managed, not solved. A 30-to-60-minute window before re-login is fine for batch work but useless for ongoing maintenance. If we want to add cities on demand — and we will — the automation needs either a more persistent auth mechanism or a scheduled window where all pending work gets processed in one session burst. I don't know which is better yet.
