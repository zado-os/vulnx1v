# -*- coding: utf-8 -*-
"""Double-confirmation for shell HIT (two independent GET checks)."""

from __future__ import (absolute_import, division, print_function)

from common.scan_options import ScanOptions
from common.rate_limit import rotate_headers


def confirm_shell(url, headers, shell_url, timeout=12):
    from common.exploit_http import _shell_probe_once
    if not ScanOptions.get().double_verify:
        return _shell_probe_once(url, headers, shell_url, timeout=timeout)
    h1 = rotate_headers(headers)
    h2 = rotate_headers(headers)
    return (
        _shell_probe_once(url, h1, shell_url, timeout=timeout)
        and _shell_probe_once(url, h2, shell_url, timeout=timeout)
    )
