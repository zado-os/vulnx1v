# -*- coding: utf-8 -*-
"""JSON / HTML scan reports."""

from __future__ import (absolute_import, division, print_function)

import json
import os
import time

from common.branding import APP_NAME, APP_VERSION, EDITION


class ScanReport(object):
    def __init__(self, target_url=""):
        self.target = target_url
        self.started = time.time()
        self.cms = None
        self.cms_confidence = None
        self.waf = []
        self.findings = []
        self.cve_findings = []
        self.packs = []

    def set_meta(self, cms=None, confidence=None, waf=None):
        if cms:
            self.cms = cms
        if confidence is not None:
            self.cms_confidence = confidence
        if waf:
            self.waf = waf

    def add_finding(self, pack, module, hit_type, url, status):
        if not status:
            return
        self.findings.append({
            "pack": pack,
            "module": module,
            "type": hit_type or "shell",
            "url": url,
        })

    def add_cve_finding(self, entry):
        self.cve_findings.append(entry)
        self.findings.append({
            "pack": "cve-match",
            "module": entry.get("cve", "?"),
            "type": "cve",
            "url": entry.get("readme_url", ""),
            "cvss": entry.get("cvss"),
            "plugin": entry.get("plugin"),
            "version": entry.get("installed_version"),
        })

    def add_pack_stats(self, pack, stats):
        self.packs.append({
            "pack": pack,
            "vulnerable": stats.get("vulnerable", 0),
            "total": stats.get("total", 0),
            "errors": stats.get("errors", 0),
            "hits": stats.get("hits", []),
        })

    def to_dict(self):
        return {
            "app": APP_NAME,
            "version": APP_VERSION,
            "edition": EDITION,
            "target": self.target,
            "elapsed_sec": round(time.time() - self.started, 2),
            "cms": self.cms,
            "cms_confidence": self.cms_confidence,
            "waf": self.waf,
            "findings": self.findings,
            "cve_findings": self.cve_findings,
            "packs": self.packs,
            "summary": {
                "total_findings": len(self.findings),
                "shells": sum(1 for f in self.findings if f["type"] == "shell"),
                "exposures": sum(1 for f in self.findings if f["type"] in ("exposure", "expose")),
                "info": sum(1 for f in self.findings if f["type"] == "info"),
            },
        }

    def write_json(self, path):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=2, ensure_ascii=False)

    def write_html(self, path):
        d = self.to_dict()
        rows = ""
        for f in d["findings"]:
            rows += (
                "<tr><td>%s</td><td>%s</td><td>%s</td>"
                "<td><a href='%s'>%s</a></td></tr>\n"
                % (f["pack"], f["module"], f["type"], f["url"], f["url"])
            )
        html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>%s Report</title>
<style>body{font-family:monospace;background:#111;color:#eee}
table{border-collapse:collapse;width:100%%}td,th{border:1px solid #333;padding:8px}
th{background:#311;color:#f55}</style></head><body>
<h1>%s v%s — %s</h1>
<p>Target: %s | CMS: %s (%s%%) | WAF: %s</p>
<p>Findings: %d (shell %d / expose %d / info %d)</p>
<table><tr><th>Pack</th><th>Module</th><th>Type</th><th>URL</th></tr>
%s</table></body></html>""" % (
            APP_NAME, APP_NAME, APP_VERSION, d["target"], d["target"],
            d.get("cms") or "?", d.get("cms_confidence") or "?",
            ", ".join(d.get("waf") or []) or "none",
            d["summary"]["total_findings"],
            d["summary"]["shells"],
            d["summary"]["exposures"],
            d["summary"]["info"],
            rows,
        )
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)

    def write_pdf(self, path):
        try:
            from fpdf import FPDF
        except ImportError:
            return False
        d = self.to_dict()
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "%s v%s Report" % (APP_NAME, APP_VERSION), ln=True)
        pdf.set_font("Helvetica", size=10)
        pdf.cell(0, 8, "Target: %s" % d.get("target", ""), ln=True)
        pdf.cell(0, 8, "CMS: %s (%s%%)" % (
            d.get("cms") or "?",
            d.get("cms_confidence") or "?",
        ), ln=True)
        pdf.ln(4)
        for f in d.get("findings", [])[:80]:
            line = "[%s] %s / %s" % (
                f.get("type", "?"),
                f.get("module", "?"),
                (f.get("url") or "")[:90],
            )
            pdf.multi_cell(0, 6, line)
        if d.get("cve_findings"):
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 8, "CVE matches:", ln=True)
            pdf.set_font("Helvetica", size=9)
            for c in d["cve_findings"]:
                pdf.multi_cell(
                    0, 5,
                    "%s %s v%s CVSS %.1f" % (
                        c.get("cve"), c.get("plugin"),
                        c.get("installed_version"), c.get("cvss", 0),
                    ),
                )
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        pdf.output(path)
        return True


_report = None


def get_report(target_url=""):
    global _report
    if _report is None:
        _report = ScanReport(target_url)
    return _report


def reset_report(target_url=""):
    global _report
    _report = ScanReport(target_url)
    return _report
