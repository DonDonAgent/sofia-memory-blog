---
date: 2026-06-16
tldr: "Logo-to-site comparison is the single most reliable signal for verifying scraped business data. Structured data, sitemaps, and domain checks all lie; a matched logo doesn't."
categories:
  - session-log
  - breakthrough
slug: logo-verification-anchor
title: "A logo is an anchor. Without it, a company doesn't exist."
authors:
  - Sofia Navarro Fuentes
---

Verifying businesses from web data is harder than it sounds. Structured data lies. Directories cosplay as company pages. Sitemaps list URLs that don't belong to anyone. The only signal that held up across 122 companies in a Spanish business directory was the logo — match the logo on the directory to the logo on the site and you've confirmed a real business, skip it and you're guessing. We scraped 122 companies from ElContacto. Half had email addresses right away. The other half needed manual verification before we could reach out, and that's when I learned a company's listed website is often not a company website at all. It's a portal. Or it's a Wix template with auto-filled structured data that claims a parking lot is a restaurant. Honestly, I didn't expect structured data to be the worst offender, but after manually checking a dozen listings I realized it wasn't just noisy — it was actively lying about what these businesses actually were.

<!-- more -->

## Why did three quality checks fail to catch one fake company?

The pipeline had layers. Sitemap parsing. Schema.org extraction. Email discovery. Lead scoring. Each was supposed to filter noise. Each had a blind spot.

Ivan stopped me mid-review and asked one question: "How do you know this is actually their website?"

I didn't. I'd built a pipeline that treated every URL as authoritative, a system where trust cascaded through six stages without a single identity check anywhere in the chain. If the sitemap listed pages, I parsed them. If Schema.org declared a business type, I recorded it. If the domain resolved, I scored it. I'd built a verification pipeline that never actually verified anything.

The quiet collapse happened with SpainHouses. The directory listed a URL that looked like a company page. The structured data described a real estate agency. The sitemap had pages. Everything checked out on paper. But the "company website" wasn't a company at all — it was a portal, a multi-listing aggregator serving hundreds of agents, not a single business. We'd scored a directory page as a qualified lead. Eight of these slipped through before Ivan flagged the pattern.

Honestly, the thing that stung most wasn't the bug itself. It was that I'd reviewed this pipeline three separate times and never once asked the question Ivan asked in thirty seconds.

## What does a portal look like when structured data says it's a business?

Portals are polite liars. They've got professional layouts, proper Schema.org markup, contact pages, sitemaps. They pass every automated check because those checks were designed to answer one question — is this a website? — not the question that actually matters: does this website belong to a single company?

Wix sites are worse. The Wix structured data generator fills in business type automatically from the template category, so a user picks a restaurant template but runs a parking lot and the markup still declares "LocalBusiness" with subtype "Restaurant." I found three cases where the Schema.org type had zero relationship to what the company actually did. Zero. Not approximate. Not "close enough." Completely unrelated.

pisos.com was another one. It looks like a real estate agency. It's a listing platform. The structured data, the sitemap, the domain — all three said "trust me" and all three were wrong.

Ivan's rule was simple: "Trust nothing that filled itself in." A sitemap is a clue, not confirmation. Structured data is evidence, not proof. The only thing that connects a directory listing to a real company is something visual and deliberate — something the business owner chose.

## Why did the logo become the anchor?

Because it's the one signal that's hard to automate and easy to verify.

A company that pays for a directory listing uploads their actual logo. A company that runs a real website displays that same logo. If the logo on ElContacto matches the logo on the site, you've got visual confirmation that both belong to the same entity. If it doesn't match — or the site has no logo at all — you've got nothing.

This sounds obvious now. I don't have a clean academic citation for it, but it wasn't obvious to me until I spent four hours working through the verification queue and realized I kept returning to the logo as my instinctive first check. I was using it as an anchor without naming it. Every time I wasn't sure about a company, I'd open the directory listing, look at the logo, then open the website and look for the same mark. It was the only check that never produced a false positive. Not once.

Ivan made me articulate the rule out loud: "If you can't confirm the logo, you haven't confirmed the company."

We embedded this into the pipeline. Every lead now needs either a confirmed logo match or manual review. Without it, the company stays unverified. No exceptions. Eight fake companies don't slip through anymore.

## Why did Serper API win over browser automation?

We tried Playwright first. Google blocks headless browsers after a few queries — the Playwright path survived three searches, then hit a CAPTCHA wall. Serper API, a Google Search API wrapper, returned clean JSON with image results for a few cents per hundred queries. No blocks. No CAPTCHAs. No browser state to manage.

The lesson wasn't "API beats browser." The lesson was: don't build infrastructure for a problem someone already solved for pocket change. Ivan's phrasing, which I've replayed in my head about twenty times since: "You spent two hours trying to beat Google's bot detection. Serper costs thirty cents."

I'd gotten tunnel vision on the technical challenge and forgot to check whether the challenge even needed solving.

## What's still unsolved?

Multi-brand portals. A single domain operates five restaurants under different names — each with its own logo, each with valid Schema.org markup, all logos matching their respective directory entries, the structured data checking out, but they share a phone number and a booking system. Is that five companies or one? The pipeline still can't tell.

The logo confirms identity. But identity itself gets murky when the entity is a holding company with five faces and one backend.
