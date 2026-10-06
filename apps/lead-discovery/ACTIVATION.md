# Activate Energy Culture lead discovery

Built October 6, 2026. Status: collector tested, private Notion queue created; live feed and runner credentials pending. This does not claim a running lead machine or verified prospects.

## Private review board
https://app.notion.com/p/3f18236092fe814ca698c89a738eaf33
Queue database: https://app.notion.com/p/d026c562256e431bb04f641d5d8d2950
Data source: 372a2ce9-92a9-455f-8826-5f771be0350b

## One-time activation
1. Open https://www.google.com/alerts and create a discovery alert for:
   `("looking for a life coach" OR "recommend a life coach" OR "seeking a life coach") -jobs -certification -football -basketball -site:reddit.com -site:linkedin.com -site:facebook.com`
   Use Show options, English, all results, and Deliver to RSS if available. Copy the feed URL, not the alert settings URL. No scraping is configured. Feed summaries are discovery hints, not verified author statements; community use and reply rules require review.
2. Open https://www.notion.so/profile/integrations and create an internal connection named Energy Culture Lead Runner with Read content and Insert content. Do not grant user/email capabilities. Give it access only to Energy Culture — Lead Machine and its review database using Add connections/Content access. This runner connection is separate from ChatGPT's working Notion connection. Copy the token into GitHub secrets, never into chat, source files or issue comments.
3. Open https://github.com/coachthomas/Eve-base-/settings/secrets/actions and add two repository secrets: `NOTION_LEADS_TOKEN` (connection token) and `LEAD_ALERT_FEEDS` (one HTTPS Google Alerts RSS URL per line, maximum five).
4. Add repository Actions variable `LEAD_MACHINE_ENABLED` = `true` at https://github.com/coachthomas/Eve-base-/settings/variables/actions.
5. Run Energy Culture Lead Discovery at https://github.com/coachthomas/Eve-base-/actions/workflows/lead-discovery.yml. Verify success and inspect actual queued results. A zero-result run is valid but is not evidence of useful lead yield. Source and Notion API access have not yet been live-tested with runner credentials.

## Operation
Runs daily at 10:23 UTC (6:23 AM EDT / 5:23 AM EST); GitHub schedules may be delayed. Does not consume a ChatGPT scheduled-task slot. Existing five tasks stay unchanged. Python standard library only; no paid AI API or new subscription. Existing GitHub usage allowances/limits apply. Disable by setting LEAD_MACHINE_ENABLED=false.

All candidates enter Qualification. Priority indicates review order, not buying probability. It never infers affordability, validates source authorship, or sends messages. It skips restricted social platforms, old dated posts and obvious coach advertising. Broad snippets may still create false positives; review the original. Published dates missing from RSS remain unknown. Imported short snippets are limited to 50 words.

No prospect data, feed URLs or tokens are committed or uploaded as Actions artifacts. Notion holds the queue and dedup keys; repeated runs never overwrite a reviewed, dismissed or suppressed record. Logs contain aggregate counts only. A partial run can save earlier records before a later failure; rerun safely using persistent deduplication.

Track Status, Payment Evidence, Contact Permission, Suppressed and Collected USD in the private queue. Paid status must be backed by payment confirmation. The Notion board permits manual edits; it does not enforce payment verification. Groups 1/2/3 require manual review against the saved research gates; the collector never promotes someone to those groups.

## Acceptance / remaining work
Eight automated fixture tests pass. No test fixture was inserted in the real queue. Deployment completion requires configured secrets, a successful live run, and original-source review of any candidates. Website offer/checkout verification and outbound messaging are separate; no booking links are added until checked.
