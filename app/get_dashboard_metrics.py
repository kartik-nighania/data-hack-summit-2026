"""Metrics-API access (Module 8): the resilient query helper the dashboards,
health checks and monitoring jobs share.

Notebook 04 teaches it inline; notebook 05's baseline/health-check job imports it.
Budget note: the Metrics API allows 100 requests/DAY on the free tier.
"""
import json
import os
import time

import requests

from app.config import load_env


def metrics_query(q):
    """Resilient Metrics-API call: retries transient errors; explains 429 (100 req/day free tier)."""
    load_env()
    auth = (os.environ["LANGFUSE_PUBLIC_KEY"], os.environ["LANGFUSE_SECRET_KEY"])
    host = os.environ["LANGFUSE_HOST"]
    for attempt in (1, 2):
        r = requests.get(f"{host}/api/public/v2/metrics", auth=auth,
                         params={"query": json.dumps(q)}, timeout=30)
        if r.status_code == 429:
            print("⚠️ Metrics API daily budget exhausted (100 requests/day on the free tier) - "
                  "charts will be empty; they refill tomorrow. This is why monitor jobs batch queries!")
            return []
        if r.status_code >= 500 and attempt == 1:
            time.sleep(2); continue
        r.raise_for_status()
        return r.json().get("data", [])
    return []
