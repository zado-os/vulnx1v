# -*- coding: utf-8 -*-
"""Global scan options (CLI → exploit engine)."""

from __future__ import (absolute_import, division, print_function)

import re

SEVERITY_RANK = {"info": 1, "exposure": 2, "expose": 2, "shell": 3}


class ScanOptions(object):
    pack_mode = None          # None | "legacy" | "2026"
    hits_only = False
    min_severity = None       # "info" | "expose" | "shell"
    threads = 1
    proxy = None
    report_path = None        # JSON report file
    # Advanced pipeline (v4.2+)
    full_advanced = False
    cve_match = False
    wpscan = False
    nuclei = False
    sqli_xss = False
    rate_limit = False
    double_verify = False
    msf_search = False
    pdf_report = False
    real_exploit = True       # True = RCE/upload attempts; False = detect-only INFO

    _instance = None

    def advanced_enabled(self):
        return self.full_advanced or any([
            self.cve_match, self.wpscan, self.nuclei,
            self.sqli_xss, self.msf_search,
        ])

    @classmethod
    def configure(cls, **kwargs):
        inst = cls()
        for k, v in kwargs.items():
            if hasattr(inst, k):
                setattr(inst, k, v)
        cls._instance = inst
        return inst

    @classmethod
    def get(cls):
        return cls._instance or cls()

    @classmethod
    def reset(cls):
        cls._instance = None


def is_2026_method(method_name):
    return bool(re.search(r"2026_\d{3}$", method_name or ""))


def filter_exploit_chain(chain, pack_mode=None):
    pack_mode = pack_mode or ScanOptions.get().pack_mode
    if not pack_mode:
        return chain
    if pack_mode == "2026":
        return [(a, b) for a, b in chain if is_2026_method(b)]
    if pack_mode == "legacy":
        return [(a, b) for a, b in chain if not is_2026_method(b)]
    return chain


def severity_ok(hit_type):
    opts = ScanOptions.get()
    if opts.hits_only and not hit_type:
        return False
    if opts.hits_only and hit_type == "info":
        return False
    if not opts.min_severity:
        return True
    need = SEVERITY_RANK.get(opts.min_severity, 1)
    got = SEVERITY_RANK.get(hit_type or "info", 1)
    return got >= need


def should_print_result(result):
    if not result.get("status"):
        return not ScanOptions.get().hits_only
    return severity_ok(result.get("hit_type") or "shell")
