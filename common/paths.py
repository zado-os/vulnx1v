# -*- coding: utf-8 -*-
"""Resolve project paths (shell payloads, data) from any working directory."""

from __future__ import (absolute_import, division, print_function)

import os

from common.branding import (
    SHELL_GIF,
    SHELL_HTML,
    SHELL_PHP,
    SHELL_TXT,
    SHELL_ZIP,
)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL_DIR = os.path.join(ROOT_DIR, "shell")

_FALLBACKS = {
    "DevXploit.php": SHELL_PHP,
    "DevXploit.html": SHELL_HTML,
    "DevXploit.txt": SHELL_TXT,
    "DevXploit.gif": SHELL_GIF,
    "DevXploit.zip": SHELL_ZIP,
    "VulnX.php": SHELL_PHP,
    "VulnX.html": SHELL_HTML,
}


def project_root():
    return ROOT_DIR


def shell_path(filename):
    path = os.path.join(SHELL_DIR, filename)
    if os.path.isfile(path):
        return path
    alt = _FALLBACKS.get(filename)
    if alt:
        alt_path = os.path.join(SHELL_DIR, alt)
        if os.path.isfile(alt_path):
            return alt_path
    return path


def open_shell(filename, mode="rb"):
    return open(shell_path(filename), mode)
