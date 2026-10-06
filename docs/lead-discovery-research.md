# Energy Culture lead discovery: research and build specification

Research date: October 6, 2026. Scope: find relevant prospects for Thomas to review and contact, plus qualify inbound inquiries. This is a build specification, not a deployed collector or a purchased dataset. Vendor descriptions are claims, not independently tested accuracy. Access rules and free allowances must be rechecked when a connector is enabled.

## Recommended direction

Build a small, evidence-based version of the workflow used by established sales platforms: discover → preserve evidence → verify → match an offer → qualify payment → rank → human review → record outcomes. Start with existing first-party inquiries and free web alerts. Add public/community connectors individually after checking their terms and actual yield.

The important limitation: most leading platforms sell B2B account intelligence. A company researching leadership does not establish that its employee wants personal coaching or can pay $150/$400. Our useful unit is a person's explicit coaching request, with a suitable contact route and a separate payment signal.

Do not buy a giant contact list to compensate for weak intent. No free source identified here reliably supplies all three of coaching need, individual affordability, and permission to contact. Public discovery will commonly produce candidates who still need qualification.

## 1. Free and limited-free source inventory

| Source | What it supplies / access | Cost status | Best use and limits | Build decision |
|---|---|---|---|---|
| Energy Culture's existing inquiry and booking records | Client-submitted goal, chosen offer, stated budget, requested reply channel; authorized export/API once mapped | No new data purchase; existing Wix costs/allowances remain | Highest direct relevance; an inquiry is not automatic marketing permission. Never import coaching transcripts into prospecting | First connector; use minimum inquiry fields |
| Referrals submitted with permission | Self-described need and introduction from a client/partner | No data purchase | A referral name alone is not permission or affordability evidence | Manual intake first |
| Google Alerts | Email links when new matching Search results appear | Free alert workflow | Discovery pointers, incomplete indexing, no guaranteed real-time coverage or blanket right to copy destination content | First external discovery lane; import delivered links, review originals |
| Talkwalker Alerts | Keyword/Boolean alerts; email and RSS; advertised web/blog/forum/X coverage | Free alerts, distinct from paid listening suite | Provider coverage claims require pilot testing; RSS access does not grant unrestricted reuse of underlying posts | Preferred feed candidate; verify account/feed and terms before activating |
| Bluesky public AppView API | Public post/feed endpoints; official reference documents public GET access | No paid key identified for public read endpoints | Search endpoint docs redirected during this check; exact search behavior/rate limits need runtime verification. Content remains user-owned; no blanket commercial content license | Pilot candidate, not approved wholesale reuse |
| Individual permissioned forums/RSS, including Discourse sites | Topic/post links and text through site-specific feeds/API | Often no fee; site dependent | Discourse software API docs do not authorize collection from every forum. Each operator's rules, content license, auth and deletion handling matter | Enable only approved named communities |
| YouTube Data API | Search/video/comment metadata through official API | Quota limited; project/API setup required | Current docs list 100 search calls/day and 10,000 units/day for other endpoints. Observe API policies. Comments are usually weak buying evidence | Later audience/content research; low priority for individual sales leads |
| Hunter Free | Business contact discovery and email verification | Official help currently lists 50 credits/month | Business email verification is not buying intent, consent, or personal affordability; avoid guessed addresses | Optional referral/partner lane after prospect identified |
| Apollo Free | Limited B2B contact/search and one intent topic advertised | Free account, plan-dependent allowances | Company buying signals, not personal coaching demand; API/export permissions require separate checking | Optional business partnership/employer-funded lane |
| Clay Free | Research/enrichment tables and multi-provider waterfalls | Current page: 500 actions/month, 100 data credits/month, 200 rows/table; no phone enrichment | Provider credits, own API keys and data rights remain separate; unsuitable as unlimited free collection | Workflow benchmark / small experiment, not dependency |
| Census/ACS API | Public aggregate demographics and market characteristics | Free API/key | Useful for market sizing and comparing areas; area income cannot establish a person's budget | Planning only; never individual paid-tier qualification |
| OpenStreetMap data | Locations/business categories for possible partners | Open data under its applicable license; hosted services have separate limits | Public Nominatim is not a bulk prospect search service. Data license and endpoint policy both apply | Optional partner mapping using suitable licensed extracts/service; not consumer lead qualification |

Google Alerts: https://support.google.com/websearch/answer/4815696

Talkwalker: https://www.talkwalker.com/alerts

Bluesky: https://docs.bsky.app/docs/api/app-bsky-feed-get-author-feed and https://bsky.social/about/support/tos

Discourse: https://docs.discourse.org/

YouTube: https://developers.google.com/youtube/v3/getting-started and https://developers.google.com/youtube/v3/docs/search/list

Hunter: https://help.hunter.io/en/articles/11060999-what-s-included-in-hunter-s-free-plan

Apollo: https://www.apollo.io/product/buying-intent

Clay: https://www.clay.com/pricing

Census: https://www.census.gov/data/developers.html

OSM endpoint policy: https://operations.osmfoundation.org/policies/nominatim/

### Keep these candidates, but do not activate unrestricted collection

Reddit: very relevant expressed-need discussions, but current Data API Terms require a separate agreement for commercial use and express written approval to derive revenue. KeeLead's working Reddit search code does not supply that permission. Keep Reddit as a possible licensed integration and a place to learn general demand patterns; do not turn it into an automated free commercial lead feed. https://redditinc.com/policies/data-api-terms

LinkedIn: useful professional context and partnerships, but LinkedIn prohibits scraping tools and automated activity. Use permitted native features or a specifically authorized integration. A job title remains a fit/context signal, not proof of personal affordability. https://www.linkedin.com/help/linkedin/answer/a1341387/prohibition-of-scraping-software

Private groups, purchased consumer records, hidden contact details and anonymous visitor identification: not initial connectors. Prefer explicit inquiries, public requests with appropriate community reply rules, and permissioned introductions.

## 2. Paid-platform benchmark: what they supply and why buyers value them

G2's current category identifies established names including Apollo, ZoomInfo, LinkedIn Sales Navigator and Cognism. This is a review-based shortlist, not a universal ranking or proof of results for coaching. Clay/Common Room/Bombora/6sense add particularly useful workflow comparisons.

| Platform | How it gets results / what it supplies | Useful structure to independently implement | Limit for Energy Culture |
|---|---|---|---|
| Apollo | B2B contact/company search, intent from partners and multiple sources, filters, refreshed signals, outreach and CRM workflow | Offer-specific filters, source evidence, refresh dates, review queue, outcome tracking | Company intent is not an individual coaching/payment signal |
| ZoomInfo | Broad B2B intelligence; public information, contributed data, partner sources and research processes documented in its filings; enrichment and sales workflows | Record source reliability, recency and conflicts; integrate review with pipeline status | Proprietary dataset cannot be copied. Direct current data-source page was inaccessible in this research; filing evidence is historical |
| LinkedIn Sales Navigator | Professional network, targeted lead/account search, saved recommendations and buyer-intent features | Multiple audience profiles, saved filters, new-signal alerts, relationship context | Native access rules; role/income assumptions do not qualify coaching purchases |
| Clay | Ordered multi-provider enrichment waterfalls, AI research, tables, signal-driven workflows | Cheapest permitted source first; query the next source only for missing information; stop on sufficient evidence | Credits/data rights/costs remain; do not reproduce proprietary code or prompts wholesale |
| Common Room | Combines first-party and external signals, person/account profiles, identity resolution, scoring and plays | Evidence timeline, multiple independent signals, trigger-based review cards | Use explicit identities/authorized records; don't copy covert visitor identification |
| Bombora | Licensed B2B publisher cooperative; contextual content consumption and company research activity | Distinguish weak attention from explicit intent; compare recency and signal changes | Its proprietary cooperative is not obtainable by copying an algorithm |
| Cognism | Business contact intelligence and additional phone verification for its Diamond data | Store verification method, date and status; report unknown instead of inventing verified contacts | Verified phone ≠ consent ≠ coaching interest ≠ ability to pay |
| 6sense | Historical CRM plus first/third-party signals for predictive buying-stage/account scoring | Close the feedback loop; compare predicted fit with real paid outcomes | Small coaching dataset cannot justify calibrated probabilities; start with transparent rules |

Sources: https://www.g2.com/categories/sales-intelligence ; https://www.apollo.io/product/buying-intent ; https://www.sec.gov/Archives/edgar/data/1794515/000162828020007502/zoominfo-s1a1.htm ; https://www.linkedin.com/help/sales-navigator/answer/a507435 ; https://university.clay.com/docs/building-a-data-waterfall ; https://www.commonroom.io/product/signals/ ; https://bombora.com/what-is-intent-data/ ; https://www.cognism.com/diamond-data ; https://6sense.com/platform/predictive-analytics/

### Cross-check against actual users

Anil P., a software founder reviewing Apollo on G2 in August 2026, describes reduced fragmentation between finding contacts, verifying them, outreach and CRM sync. He also reports stale contact details and lower-tier credit limitations. Borrow the integrated workflow and verification step; do not assume the vendor's accuracy claim transfers to us.

https://www.g2.com/products/apollo-io/reviews/apollo-io-review-13344982

Matthew W., sales administration support, reviewing Sales Navigator in May 2026, values company/role targeting and multiple personas. He notes cost and the need to use the workflow consistently. This supports multiple saved audience definitions rather than one narrow perfect-client filter. His review was incentivized, as disclosed by G2.

https://www.g2.com/products/linkedin-sales-navigator/reviews/linkedin-sales-navigator-review-12783346

Common Room's vendor-published Semgrep case describes combining product use, web visits and GitHub activity for warmer outbound. Its reported 74% pipeline increase is a selected customer claim, not independent causal evidence or a coaching forecast. Borrow signal combination and timing, not the claimed lift.

https://www.commonroom.io/customers/semgrep-warm-outbound-grow-pipeline/

Recurring value: precision, fresher evidence, fewer manual steps, signals delivered where the seller works. Recurring weakness: inaccurate/stale records, expense, limits and complexity. Our prototype should stay small and explain every ranking.

## 3. Build parameters

### Offer catalog

| Offer | Price | Matching evidence |
|---|---:|---|
| Becoming Your Most Genuine Self | $150 | Person explicitly seeks authenticity, values clarity, direction or guided self-reflection; coaching rather than a request for clinical treatment |
| Energy Culture — Fits Like a Glove | $400 | Person wants a personalized coaching path; two approximately one-hour sessions and relevant format/timing accepted |

These are sales-matching definitions, not diagnosis categories. Verify that the relevant offer/booking link is publicly usable before including it in any outreach brief. This research does not establish publication status.

### Mandatory gates, separate from fit score

1. Source use is approved for this purpose and evidence is traceable.
2. Person expresses a relevant goal/need; generalized audience engagement is insufficient.
3. Payment evidence relates to the selected offer: explicit available budget at/above its price, or explicit acceptance of that price. Label this a stated payment signal, never guaranteed affordability.
4. A permitted and appropriate reply/contact route exists; no suppression/do-not-contact flag.
5. Thomas reviews the record before any contact. Initial service design assumes adult clients; uncertain age/eligibility requires review, not visual inference.

Willingness to buy coaching with no price, past spending on related services, and employer funding not yet confirmed are weaker indicators. Preserve them as possible payment signals in the qualification queue; they do not meet the initial price-specific gate. A $200 budget can qualify the $150 offer, not the $400 offer. Unknown budget does not mean unable to pay.

### Three paid fit groups, plus separate queues

Use five explicit fit parameters: relevant stated goal; appropriate coaching service; desired course structure; compatible session format; compatible timing. Mark each met / not met / unknown with evidence.

| Queue | Rule |
|---|---|
| Group 1 — strongest fit | All five fit parameters met; every mandatory gate passed |
| Group 2 — strong fit | Three or four met including goal and coaching suitability; every mandatory gate passed; remaining unknowns clearly shown |
| Group 3 — broader fit | Goal and coaching suitability met, but fewer other parameters confirmed; every mandatory gate passed; no confirmed hard incompatibility |
| Qualification | Relevant interest but payment, contact route, eligibility or other required evidence unresolved |
| Community assistance — later | Person explicitly seeks free/donated support; separate future workflow, not inferred from appearance or missing budget |
| Excluded / suppressed | Confirmed incompatible service, prohibited source use, contact opt-out, or clearly unsuitable approach |

Track optional self-disclosed geography/time zone and communication preferences for delivery. Do not infer income from job, neighborhood, photographs, likes or follower count. Do not infer health conditions or rank personal distress for sales.

Initial freshness assumption: prioritize requests from the last 30 days; older records need renewed evidence before promotion. This is a configurable pilot hypothesis, not a researched optimum. Published date and collection date remain separate.

## 4. Function contracts

| Function | Inputs → output / responsibility |
|---|---|
| `register_source` | Provider, terms URL, permitted purpose, license, access method, quota, review date → source approval record |
| `can_collect` | Source approval + requested operation → allow / block / manual review; no silent permission assumptions |
| `build_queries` | Offer goals + explicit seeking language + exclusions → provider-specific queries |
| `fetch_candidates` | Approved source + query + quota budget → real records, cursor, retrieval time, errors; no demo fallback |
| `normalize_evidence` | Raw permitted result → canonical URL, source ID, exact short excerpt, author ID if supplied, published/observed dates |
| `deduplicate` | Canonical URL + provider IDs → merge duplicate evidence without guessing cross-platform identity |
| `extract_signals` | Evidence → goal/intent/payment/contact assertions with exact supporting spans; unsupported fields remain unknown |
| `match_offers` | Supported goal + format + offer catalog → candidate offers and reasons |
| `qualify_payment` | Price-specific evidence + offer price → stated-qualified / possible / unknown / incompatible |
| `assign_tier` | Gate results + five fit parameters → group/queue plus rule version and explanation |
| `review_contact_route` | Submitted channel/community rules/suppression → permitted channel or hold |
| `build_review_brief` | Approved evidence → concise why-this-person/why-this-offer card, payment evidence and source link |
| `record_outcome` | Thomas action → contacted/replied/booked/paid/dismissed; payment amount confirmed separately |
| `evaluate_rules` | Outcomes by source, query, offer and tier → conversion counts, denominators, time cost, suggested rule changes |
| `refresh_or_expire` | Evidence age/removals → recheck, downgrade, remove or suppress as needed |

AI extraction, if used, must be evidence-bound. Rules assign tiers; generated prose cannot invent identity, phone, email, budget, intent or source verification. No automated sending in the first build.

### Minimum record schema

`lead_id`, `source_id`, `provider_record_id`, `canonical_url`, `excerpt`, `published_at`, `observed_at`, `person_id_if_known`, `stated_goal`, `intent_evidence`, `offer_matches`, `fit_parameters`, `payment_signal_type`, `payment_excerpt`, `budget_amount_if_explicit`, `currency`, `contact_route`, `contact_permission_basis`, `tier`, `rule_version`, `reviewer`, `status`, `outcomes`, `suppression`, `expires_at`.

Each extracted signal stores its evidence pointer and confidence category: direct statement / proxy / unknown. Do not publish identifiable prospect records to a public repository. Coaching recordings and session content remain outside this discovery system.

### Starter query families

- Direct request: "looking for a life coach", "recommend a life coach", "seeking a coach".
- Authenticity request: seeking/looking/recommend + authenticity, values, purpose, personal direction.
- Personalized request: seeking/looking + personalized coaching, individual coaching plan.
- Price context: coaching request + budget, paid, price, cost, investment. These words help discovery; they do not themselves satisfy the payment gate.
- Partner lane: workshop hosts, community education providers, HR/wellness decision-makers requesting speakers/coaches. Track separately from individual coaching prospects.

Tune Boolean syntax per source. Exclude coach job advertisements, coach-to-coach marketing, sports coaching and unrelated training. Avoid searching vulnerable-person support spaces for sales opportunities.

## 5. Turn it into measurable science

For each source/query/tier/offer record: candidates found, human-confirmed relevant requests, qualified payment signals, permitted contact routes, contacts attempted, replies, bookings, paid clients, collected revenue and minutes spent. Report both conversion rates and sample counts. Compute revenue and net contribution per research hour; revenue alone is not profit.

Keep Groups 2 and 3 in the pilot so weaker-fit opportunities are observed. An initial review-time allocation of 60%/25%/15% across Groups 1/2/3 is a testable proposal, not an optimum. Rotate a small random sample within each group to reduce cherry-picking. Compare similar time windows and contact approaches; log offer availability and outreach changes.

Do not call a rule score a purchase probability. Only consider predictive models after enough genuine outcomes accumulate; assess calibration and held-out performance. Small samples warrant counts and uncertainty, not confident percentage promises.

## 6. Reuse and licensing decisions

KeeLead's MIT license permits reuse subject to its conditions and notice preservation. The current prototype already preserves its copied source interface and MIT notice. Keep its modular source-adapter idea, but the audited synthetic/demo results must never enter the real prospect queue.

https://github.com/Atum246/keelead/blob/main/LICENSE

Strictly licensed candidates stay in the comparison. Decide component by component: use under its license, buy an appropriate license if later justified, independently implement a public functional idea, or leave a connector disabled. n8n is an example of source-available software with use-case restrictions; its internal-client-instance guidance may fit internal workflows, but it should not be treated as unrestricted software for resale.

https://support.n8n.io/article/can-i-use-your-license-for-my-use-case

Copyright protects expression, including software, but generally not facts, ideas, systems or methods. This supports implementing general workflow concepts with original code. It does not authorize copying proprietary code, creative copy, assets or databases, bypassing terms, or using patented methods. Changing copied code slightly is not a reliable legal remedy. Patent analysis concerns claims; this research is not a patent clearance search.

https://www.copyright.gov/help/faq/faq-general.html

https://www.uspto.gov/patents/basics/manage

For every dependency/connector keep: origin/version, software license, copied files, required notices, data-use terms, storage/redistribution restrictions, attribution, deletion process, rate/cost limits and approved purpose. Software permission and data permission are separate checks.

## 7. Concrete next build sequence

1. Extend the existing local review prototype with evidence fields, source registry, price-specific payment gates and the three fit groups plus qualification queue.
2. Add a source-approved alert-feed importer with deduplication and dates. Configure accounts/feeds only when available; never label unconfigured feeds as live.
3. Add authorized first-party inquiry import and separate marketing/contact permission fields. Do not import session data.
4. Pilot queries; review each real result and measure yield. Only then add a Bluesky or named forum adapter where access/use checks pass.
5. Add outcome reports and revise rules based on confirmed bookings/payments. Keep outreach human-controlled.

Acceptance examples: duplicate posts merge; fake/demo contacts rejected; unknown budget goes to qualification; $200 supports $150 only; all paid groups require price-specific payment evidence; opt-outs suppress contact; stale requests downgrade; unpaid booking never counts as collected revenue; review card explains every group assignment.

No subscriptions were purchased, automated collectors activated, prospects contacted or publication changes made for this research. Existing code remains a local prototype; these functions are specified, not claimed implemented.
