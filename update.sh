#!/bin/bash
red="\e[0;31m"
green="\e[0;32m"
off="\e[0m"
REPO="https://github.com/zado-os/nexploit.git"
INSTALL_DIR="/usr/share/nexploit"
TERMUX_DIR="/data/data/com.termux/files/usr/share/nexploit"

banner() { echo -e "===== Nexploit UPDATE — ZADO-OS ====="; }

termuxOS() {
  rm -rf "$TERMUX_DIR"
  git clone "$REPO" "$TERMUX_DIR"
  echo -e "$green[+]$off Updated. Run: nexploit"
}

debianOS() {
  rm -rf "$INSTALL_DIR"
  git clone "$REPO" "$INSTALL_DIR"
  chmod +x "$INSTALL_DIR/nexploit" "$INSTALL_DIR/update.sh" 2>/dev/null || true
  echo -e "$green[+]$off Updated. Run: nexploit"
}

banner
if [ -d "/data/data/com.termux/files/usr/" ]; then
  termuxOS
elif [ -d "/usr/bin/" ]; then
  debianOS
else
  echo "Unsupported system"
  exit 1
fi
