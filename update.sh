#!/bin/bash
# DevXploit updater — ZADO-OS Roger OS

INSTALL_DIR="/usr/share/devxploit"
REPO="https://github.com/zado-os/devxploit.git"

if [ ! -d "$INSTALL_DIR/.git" ]; then
    echo "[-] DevXploit not installed in $INSTALL_DIR"
    exit 1
fi

cd "$INSTALL_DIR" || exit 1
git pull origin main
python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null \
    || python3 -m pip install -r requirements.txt --user
echo "[+] DevXploit updated. Run: devxploit -u URL -x"
