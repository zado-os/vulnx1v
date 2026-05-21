# -*- coding: utf-8 -*-
"""Match detected plugin versions against local CVE database."""

from __future__ import (absolute_import, division, print_function)

import json
import os
import re

from common.plugin_meta import fetch_readme_meta
from common.exploit_http import plugin_readme_exists
from common.paths import project_root

_DB = None


def _load_db():
    global _DB
    if _DB is not None:
        return _DB
    path = os.path.join(project_root(), "data", "cve_db.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            _DB = json.load(fh)
    except (OSError, IOError, ValueError):
        _DB = {}
    return _DB


def _version_le(a, b):
    """Rough semver compare (a <= b)."""
    def parts(v):
        return [int(x) for x in re.findall(r"\d+", v)[:4]] or [0]
    return parts(a) <= parts(b)


def scan_plugins_for_cve(url, headers, slugs=None):
    db = _load_db()
    slugs = slugs or list(db.keys())
    findings = []
    for slug in slugs:
        if not plugin_readme_exists(url, headers, slug, hint=slug):
            continue
        meta = fetch_readme_meta(url, headers, slug)
        if not meta:
            continue
        ver = meta["version"]
        for entry in db.get(slug, []):
            max_v = entry.get("max_version")
            if max_v and _version_le(ver, max_v):
                findings.append({
                    "slug": slug,
                    "plugin": meta["name"],
                    "installed_version": ver,
                    "cve": entry["cve"],
                    "cvss": entry.get("cvss", 0),
                    "title": entry.get("title", ""),
                    "max_affected": max_v,
                    "readme_url": meta["readme_url"],
                })
    return findings
