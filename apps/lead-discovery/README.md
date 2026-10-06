# Energy Culture opportunity review

First working slice of the KeeLead adaptation. Run `python apps/lead-discovery/server.py` from the repository root and open http://127.0.0.1:8765.

Python 3.12 standard library only. No API key, installation, hosting bill, scraper, AI call or outreach sender. Data persists in `~/.eve/opportunities.sqlite3`, outside this public repository. Override with `EVE_LEADS_DB` for isolated tests. This is a local prototype; it has no multi-user authentication and must not be exposed on the internet.

Enter source URL, excerpt and expressed need; select an offer fit and record actual evidence of coaching intent. Unknown intent stays unknown. Review the source yourself. Track outcomes; paid requires a positive payment amount and confirmation/attribution notes. There is no automatic verification of a payment or source URL. Offer matching is manual, not an AI prediction.

Borrowed from KeeLead: the source-adapter and review-queue framework. `third_party/keelead/source-types.ts` is a preserved upstream interface reference, not executed by this Python prototype. Its MIT notice is retained alongside it. Generated contacts and guessed emails are excluded. Automated source retrieval and ranking are subsequent work, after validating a connector.

Do not commit real prospect information. No client session data belongs in this lead-discovery app.

## Automated discovery added October 6, 2026
`collector.py` imports configured Google Alerts RSS discovery hints into the private Notion queue, deduplicates across runs and leaves all candidates in Qualification. No automated messaging. See ACTIVATION.md for the remaining credentials, live-run checks and daily runner setup. Run tests from this directory with `python3 -m unittest discover -s tests -v`.
