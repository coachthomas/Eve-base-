"""Supervised local intake for ChatGPT's search and Notion connectors.
No credentials required. Input is a JSON list on stdin; output is Notion-ready
properties for deduplication and insertion through the connected Notion tools.
This mode does not run unattended or call connectors from Python.
"""
import json
import sys
from datetime import datetime, timezone
from collector import qualify

def prepare(entries):
    result, seen = [], set()
    counts = {"examined": len(entries), "rejected": 0, "duplicates": 0, "prepared": 0}
    for entry in entries:
        # The supervising agent must inspect source intent before this gate.
        if entry.get("source_review") != "individual_request":
            counts["rejected"] += 1
            continue
        item = qualify({k: entry.get(k) for k in ("url", "title", "excerpt", "published")})
        if not item:
            counts["rejected"] += 1
            continue
        if item["key"] in seen:
            counts["duplicates"] += 1
            continue
        seen.add(item["key"])
        properties = {
            "Name": item["title"][:180] or "Coaching request — review",
            "Source Link": item["url"],
            "Evidence": "Search discovery excerpt (unverified): " + " ".join(item["excerpt"].split()[:50]),
            "Source": "Connected web search; supervised local intake",
            "Key": item["key"],
            "date:Observed:start": datetime.now(timezone.utc).isoformat(),
            "date:Observed:is_datetime": 1,
            "Offer": item["offer"], "Queue": "Qualification", "Status": "New",
            "Priority": item["priority"],
            "Reason": "Individual request identified during source review. Verify date, adult eligibility, payment evidence, source-use permission and contact route before promoting.",
            "Payment Evidence": "Unknown",
            "Contact Permission": "Unknown — review original source and community rules",
            "Suppressed": "__NO__",
        }
        if item["published"]:
            properties["date:Published:start"] = item["published"]
            properties["date:Published:is_datetime"] = 1
        result.append(properties)
    counts["prepared"] = len(result)
    return {"mode": "supervised_local", "counts": counts, "pages": result}

if __name__ == "__main__":
    print(json.dumps(prepare(json.load(sys.stdin))))
