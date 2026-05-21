# -*- coding: utf-8 -*-
"""Lightweight SQLi / XSS reflection probes on common parameters."""

from __future__ import (absolute_import, division, print_function)

import re
import requests
from requests.exceptions import RequestException

from common.colors import que, good, run, W
from common.http_session import fresh_headers
from common.exploit_http import is_error_page

_SQLI_MARKERS = re.compile(
    r"sql syntax|mysql_fetch|mysqli_|ORA-\d{5}|PostgreSQL.*ERROR|"
    r"SQLite3::|unclosed quotation|Warning.*mysql",
    re.I,
)
_XSS_PROBE = "<dxXSS9/>"
_XSS_REFLECT = re.compile(r"<dxXSS9\s*/>", re.I)

_PARAMS = ["id", "page", "s", "cat", "p", "q", "search", "redirect", "url"]


def _test_url(base, headers, param, payload):
    sep = "&" if "?" in base else "?"
    test = base + sep + param + "=" + payload
    try:
        return requests.get(
            test, headers=fresh_headers(headers), verify=False, timeout=12,
        )
    except RequestException:
        return None


def run_sqli_xss_probes(url, headers):
    base = url.rstrip("/") + "/"
    findings = []
    print(" {0} SQLi / XSS probes on common parameters".format(run))
    for param in _PARAMS:
        r = _test_url(base, headers, param, "'")
        if r and r.text and _SQLI_MARKERS.search(r.text):
            msg = "SQLi error reflected — param %s" % param
            findings.append({"type": "sqli", "param": param, "detail": msg})
            print(" {0} {1}".format(good, msg))
        r2 = _test_url(base, headers, param, _XSS_PROBE)
        if r2 and r2.text and _XSS_REFLECT.search(r2.text) and not is_error_page(r2.text):
            msg = "XSS reflection — param %s" % param
            findings.append({"type": "xss", "param": param, "detail": msg})
            print(" {0} {1}".format(good, msg))
    if not findings:
        print(" {0} No SQLi/XSS reflections on sampled params".format(que))
    return findings
