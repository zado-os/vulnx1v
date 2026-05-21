# -*- coding: utf-8 -*-
"""Run optional advanced scan pipeline after CMS exploit scan."""

from __future__ import (absolute_import, division, print_function)

from common.colors import W, run, good, bad, info
from common.scan_options import ScanOptions
from common.report_export import get_report


def run_advanced_pipeline(url, headers, cms_name=None):
    opts = ScanOptions.get()
    if not opts.advanced_enabled():
        return

    print("{0} −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−".format(W))
    print(" {0} Advanced pipeline [ZADO-OS]".format(run))

    if opts.cve_match or opts.full_advanced:
        _run_cve_match(url, headers)

    if opts.sqli_xss or opts.full_advanced:
        from modules.advanced.sqli_xss import run_sqli_xss_probes
        hits = run_sqli_xss_probes(url, headers)
        for h in hits:
            get_report().add_finding(
                "advanced", h["detail"], h["type"], url, True,
            )

    if opts.wpscan or opts.full_advanced:
        _run_wpscan(url)

    if opts.nuclei or opts.full_advanced:
        _run_nuclei(url)

    if opts.msf_search or opts.full_advanced:
        _run_msf(url, cms_name)


def _run_cve_match(url, headers):
    from common.cve_match import scan_plugins_for_cve
    from common.colors import good, que

    print(" {0} CVE version matching (local DB)".format(run))
    hits = scan_plugins_for_cve(url, headers)
    if not hits:
        print(" {0} No version-matched CVE in local DB".format(que))
        return
    for h in hits:
        line = "%s %s v%s (CVSS %.1f) — %s" % (
            h["cve"], h["plugin"], h["installed_version"],
            h.get("cvss", 0), h.get("title", ""),
        )
        print(" {0} {1}".format(good, line))
        get_report().add_cve_finding(h)


def _run_wpscan(url):
    from common.wpscan_client import run_wpscan, wpscan_available
    from common.colors import good, bad, que

    if not wpscan_available():
        print(" {0} WPScan skipped — export WPSCAN_API_TOKEN".format(que))
        return
    print(" {0} WPScan API lookup".format(run))
    data = run_wpscan(url)
    if data.get("error"):
        print(" {0} WPScan: {1}".format(bad, data["error"]))
        return
    for v in data.get("vulnerabilities", [])[:15]:
        print(" {0} {1} {2}".format(good, v.get("cve") or "?", v.get("title", "")[:60]))
        get_report().add_finding(
            "wpscan", v.get("title", "wpscan"), "info", url, True,
        )


def _run_nuclei(url):
    from common.nuclei_runner import run_nuclei, nuclei_available
    from common.colors import good, que, run

    if not nuclei_available():
        print(" {0} Nuclei skipped — install: go install nuclei@latest".format(que))
        return
    print(" {0} Nuclei scan (wordpress,cve tags)".format(run))
    data = run_nuclei(url)
    if data.get("error"):
        print(" {0} Nuclei: {1}".format(que, data["error"][:60]))
        return
    for item in data.get("findings", [])[:20]:
        tid = item.get("template-id") or item.get("info", {}).get("name", "?")
        print(" {0} {1}".format(good, tid))
        get_report().add_finding("nuclei", str(tid), "info", url, True)


def _run_msf(url, cms_name):
    from common.msf_search import search_exploits, searchsploit_available
    from common.colors import good, que, run

    if not searchsploit_available():
        print(" {0} searchsploit skipped — apt install exploitdb".format(que))
        return
    q = (cms_name or "wordpress").lower()
    print(" {0} searchsploit: {1}".format(run, q))
    data = search_exploits(q)
    for line in data.get("results", [])[:6]:
        print(" {0} {1}".format(good, line))
