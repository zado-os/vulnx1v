# -*- coding: utf-8 -*-
"""Searchsploit / Metasploit DB lookup (if tools installed)."""

from __future__ import (absolute_import, division, print_function)

import re
import shutil
import subprocess


def searchsploit_available():
    return shutil.which("searchsploit") is not None


def search_exploits(query, limit=8):
    if not searchsploit_available():
        return {"error": "searchsploit not in PATH", "results": []}
    try:
        out = subprocess.check_output(
            ["searchsploit", "--json", query],
            stderr=subprocess.DEVNULL,
            timeout=25,
            universal_newlines=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
        return {"error": str(exc)[:80], "results": []}
    results = []
    for line in out.splitlines()[:limit]:
        if "EDB-ID" in line or "CVE-" in line or "|" in line:
            results.append(line.strip()[:120])
    if not results:
        for m in re.finditer(r"CVE-\d{4}-\d+", out):
            results.append(m.group(0))
            if len(results) >= limit:
                break
    return {"query": query, "results": results[:limit]}
