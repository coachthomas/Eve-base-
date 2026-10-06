# Energy Culture lead discovery — first revenue milestone

Status: implementation scope; not a deployed or tested application.
Owner: Thomas J. Brady / Energy Culture LLC.
Goal: help Thomas find relevant coaching conversations and track the first attributable paid booking through EnergyCulture.org.

## Upstream review
Candidate: https://github.com/Atum246/keelead
Reviewed upstream tree: a846e2b6c19f781d44073f2e651c1ac8de52cf4a.
LICENSE is MIT, copyright (c) 2024 KeeLead. Preserve its copyright and permission notice in copied code. Dependency licenses and data-provider terms require separate review.
HANDOFF.md acknowledges placeholder source implementations.
lib/sources/social/facebook.ts generates random names, phone numbers and fabricated email addresses; it is not a working Facebook prospect connector.
lib/sources/social/reddit.ts implements HTTP retrieval but has not been live-tested here. It drops post body text and deduplicates authors, which needs adjustment for evidence-based coaching opportunity review.
lib/sources/search/duckduckgo.ts uses Instant Answer results rather than a general web search feed.

## Smallest useful workflow
1. Enter a genuine public post URL and a short excerpt manually; add automated retrieval only after validating a source.
2. Record what the person explicitly asks for, publication date when known, retrieval date, and source.
3. Label fit to personal growth, life transitions, or spiritual exploration. A topic mention alone is not buying intent.
4. Prioritize explicit requests for a coach or paid guidance, recency, service fit, and whether a response is appropriate.
5. Thomas reviews the original post and chooses whether to respond.
6. Save a suggested response for Thomas to review. Sending is a separate, explicitly authorized action.
7. Track reviewed, contacted, replied, booked and paid outcomes, with actual payment amount and attribution.

## First interface
A browser-based opportunity table with source link, excerpt, expressed need, fit reason, explicit purchase-intent evidence (or unknown), proposed next step and outcome.
No inferred ability-to-pay or diagnosis. Do not score distress as sales priority.
No private prospect records in the public GitHub repository.
No invented identities or contacts. Keep demonstration data visibly separate from real records.

## Acceptance checks
- Every real opportunity has a resolvable original source link and supporting excerpt.
- Missing dates, contact details and purchase intent remain unknown.
- The same URL is not counted twice.
- A fabricated connector result cannot enter the real opportunity queue.
- Drafting a response never sends it.
- A booking is not a paid sale until payment is confirmed.
- Record the first confirmed paid booking and actual costs; do not guarantee revenue.

## Execution order
Implement source-linked intake and outcome tracking first, then validate one retrieval connector and add coaching-specific ranking.
Use the existing Energy Culture booking offer; its final price and booking URL must be verified before inserting them into outreach.
Do not incur hosting or API charges without an agreed budget.
Current execution environment is unavailable, so no installation, build or runtime tests have been performed.
