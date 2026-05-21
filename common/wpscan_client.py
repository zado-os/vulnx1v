# -*- coding: utf-8 -*-
"""WPScan API integration (optional — set WPSCAN_API_TOKEN)."""

from __future__ import (absolute_import, division, print_function)

import os
import re

import requests
from requests.exceptions import RequestException


def wpscan_available():
    return bool(os.environ.get("WPSCAN_API_TOKEN", "").strip())


def run_wpscan(url, timeout=30):
    token = os.environ.get("WPSCAN_API_TOKEN", "").strip()
    if not token:
        return {"error": "WPSCAN_API_TOKEN not set", "vulnerabilities": []}
    host = re.sub(r"^https?://", "", url.rstrip("/")).split("/")[0]
    api = "https://wpscan.com/api/v3/wordpresses/%s" % host
    try:
        r = requests.get(
            api,
            headers={"Authorization": "Token token=%s" % token},
            timeout=timeout,
        )
        if r.status_code == 404:
            return {"error": "not in WPScan DB", "vulnerabilities": []}
        r.raise_for_status()
        data = r.json()
    except RequestException as exc:
        return {"error": str(exc)[:80], "vulnerabilities": []}
    vulns = []
    for v in data.get("vulnerabilities", []) or []:
        vulns.append({
            "title": v.get("title", ""),
            "cve": ", ".join(v.get("cve", []) or []),
            "cvss": v.get("cvss", {}).get("score") if isinstance(v.get("cvss"), dict) else v.get("cvss"),
            "fixed_in": v.get("fixed_in"),
        })
    return {"host": host, "vulnerabilities": vulns}
