# -*- coding: utf-8 -*-
"""Extract plugin/theme version from WordPress readme.txt."""

from __future__ import (absolute_import, division, print_function)

import re
import requests
from requests.exceptions import RequestException

from common.exploit_http import is_error_page

_STABLE = re.compile(r"Stable tag:\s*([^\s\r\n]+)", re.I)
_NAME = re.compile(r"===\s*(.+?)\s*===", re.I)


def fetch_readme_meta(url, headers, plugin_slug, timeout=12):
    path = "/wp-content/plugins/%s/readme.txt" % plugin_slug.strip("/")
    try:
        r = requests.get(
            url.rstrip("/") + path,
            headers=headers,
            verify=False,
            timeout=timeout,
        )
    except RequestException:
        return None
    if r.status_code != 200:
        return None
    text = r.text or ""
    if is_error_page(text):
        return None
    ver = _STABLE.search(text)
    name = _NAME.search(text)
    if not ver:
        return None
    return {
        "slug": plugin_slug,
        "name": name.group(1).strip() if name else plugin_slug,
        "version": ver.group(1).strip(),
        "readme_url": url.rstrip("/") + path,
    }
