# -*- coding: utf-8 -*-
"""WAF-friendly pacing and User-Agent rotation."""

from __future__ import (absolute_import, division, print_function)

import random
import time

from common.requestUp import random_UserAgent
from common.scan_options import ScanOptions


def maybe_delay():
    if not ScanOptions.get().rate_limit:
        return
    time.sleep(random.uniform(0.15, 0.65))


def rotate_headers(headers):
    h = dict(headers or {})
    h["User-Agent"] = random_UserAgent()
    return h
