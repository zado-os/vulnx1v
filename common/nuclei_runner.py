# -*- coding: utf-8 -*-
"""Run Nuclei if installed (external binary)."""

from __future__ import (absolute_import, division, print_function)

import json
import shutil
import subprocess


def nuclei_available():
    return shutil.which("nuclei") is not None


def run_nuclei(url, tags="cve,wordpress", timeout=120):
    if not nuclei_available():
        return {"error": "nuclei not in PATH", "findings": []}
    cmd = [
        "nuclei", "-u", url, "-silent", "-jsonl",
        "-tags", tags, "-timeout", "10", "-rate-limit", "30",
    ]
    try:
        out = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, timeout=timeout, universal_newlines=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
        return {"error": str(exc)[:80], "findings": []}
    findings = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            findings.append(json.loads(line))
        except ValueError:
            pass
    return {"findings": findings}
