# -*- coding: utf-8 -*-
"""Simple interactive TUI (no curses required)."""

from __future__ import (absolute_import, division, print_function)

from common.colors import W, G, run, good, bad
from common.branding import APP_NAME, APP_VERSION


def run_dashboard(headers):
    print(W + "\n  %s TUI v%s" % (APP_NAME, APP_VERSION))
    print("  Commands: scan <url> | cve <url> | modules | help | exit\n" + W)
    while True:
        try:
            line = input(G + "devxploit> " + W).strip()
        except (EOFError, KeyboardInterrupt):
            print("")
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()
        if cmd in ("exit", "quit", "q"):
            break
        if cmd == "help":
            print(" scan https://target -x   Full exploit scan")
            print(" cve https://target       CVE version match only")
            print(" modules wordpress        List WP modules")
            continue
        if cmd == "modules" and len(parts) > 1:
            from modules.exploits.exploit_scanner import print_exploit_catalog
            print_exploit_catalog(parts[1])
            continue
        if cmd == "cve" and len(parts) > 1:
            from common.scan_options import ScanOptions
            from common.cve_match import scan_plugins_for_cve
            ScanOptions.configure(cve_match=True)
            url = parts[1]
            if not url.startswith("http"):
                url = "https://" + url
            for h in scan_plugins_for_cve(url, headers):
                print(good, h)
            continue
        if cmd == "scan" and len(parts) > 1:
            from modules.detector import CMS
            from common.scan_options import ScanOptions
            ScanOptions.configure(
                full_advanced=True, double_verify=True, rate_limit=True,
            )
            url = parts[1]
            if not url.startswith("http"):
                url = "https://" + url
            CMS(url=url, headers=headers, exploit=True).instanciate()
            continue
        print(bad, "Unknown command. Type: help")
