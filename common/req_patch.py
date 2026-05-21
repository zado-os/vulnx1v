# -*- coding: utf-8 -*-
"""Apply default HTTP timeout to all requests.* calls (prevents hung scans)."""

from __future__ import (absolute_import, division, print_function)

import requests

DEFAULT_TIMEOUT = 12
_PATCHED = False


def apply_request_timeout(timeout=DEFAULT_TIMEOUT):
    global _PATCHED
    if _PATCHED:
        return
    for name in ("get", "post", "put", "head", "delete", "patch"):
        fn = getattr(requests, name, None)
        if fn is None:
            continue

        def _wrap(original, default_timeout=timeout):
            def _caller(url, *args, **kwargs):
                from common.rate_limit import maybe_delay
                maybe_delay()
                kwargs.setdefault("timeout", default_timeout)
                kwargs.setdefault("verify", False)
                return original(url, *args, **kwargs)
            _caller._dx_patched = True
            return _caller

        wrapped = _wrap(fn)
        setattr(requests, name, wrapped)
    _PATCHED = True
