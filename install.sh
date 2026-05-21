#!/bin/bash
# DevXploit installer — ZADO-OS Roger OS (Python 3 only)

red="\e[0;31m"
green="\e[0;32m"
off="\e[0m"

REPO="https://github.com/zado-os/devxploit.git"
INSTALL_DIR="/usr/share/devxploit"
TERMUX_DIR="/data/data/com.termux/files/usr/share/devxploit"

banner() {
    echo -e "===== DevXploit INSTALL — ZADO-OS Roger OS ====="
}

install_portable() {
    echo -e "$red [$green+$red]$off Use: chmod +x devxploit && ./devxploit -u URL -x"
    echo -e "$red [$green+$red]$off Or: python3 devxploit.py -u URL -x"
}

termuxOS() {
    pkg install -y python git
    python3 -m pip install -r ./requirements.txt 2>/dev/null || pip3 install -r ./requirements.txt
    if [ -d "$TERMUX_DIR" ]; then
        read -p "Replace old install? [Y/n]: " replace
        if [ "$replace" = "y" ] || [ "$replace" = "Y" ] || [ -z "$replace" ]; then
            rm -rf "$TERMUX_DIR"
            rm -f "/data/data/com.termux/files/usr/bin/devxploit"
        else
            exit 1
        fi
    fi
    mkdir -p "$TERMUX_DIR"
    cp -r common modules shell devxploit.py install.sh update.sh devxploit requirements.txt "$TERMUX_DIR/"
    chmod +x "$TERMUX_DIR/devxploit" 2>/dev/null || true
    cat > /data/data/com.termux/files/usr/bin/devxploit << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
exec python3 /data/data/com.termux/files/usr/share/devxploit/devxploit.py "$@"
EOF
    chmod +x /data/data/com.termux/files/usr/bin/devxploit
    devxploit --help 2>/dev/null || python3 devxploit.py --help
}

debianOS() {
    apt-get install -y python3 python3-pip git whois
    python3 -m pip install -r ./requirements.txt --break-system-packages 2>/dev/null \
        || python3 -m pip install -r ./requirements.txt --user 2>/dev/null \
        || python3 -m pip install -r ./requirements.txt
    if [ -d "$INSTALL_DIR" ]; then
        read -p "Replace $INSTALL_DIR? [Y/n]: " replace
        if [ "$replace" = "y" ] || [ "$replace" = "Y" ] || [ -z "$replace" ]; then
            rm -rf "$INSTALL_DIR"
            rm -f /usr/local/bin/devxploit
        else
            exit 1
        fi
    fi
    mkdir -p "$INSTALL_DIR"
    cp -r common modules shell devxploit.py install.sh update.sh devxploit requirements.txt "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/devxploit" "$INSTALL_DIR/update.sh" 2>/dev/null || true
    cat > /usr/local/bin/devxploit << EOF
#!/bin/bash
exec python3 ${INSTALL_DIR}/devxploit.py "\$@"
EOF
    chmod +x /usr/local/bin/devxploit
    [ -f bin/devxploit.desktop ] && cp bin/devxploit.desktop /usr/share/applications/ 2>/dev/null || true
    if [ -f bin/devxploiticon.png ]; then
        cp bin/devxploiticon.png /usr/share/icons/ 2>/dev/null || true
    elif [ -f bin/nexploiticon.png ]; then
        cp bin/nexploiticon.png /usr/share/icons/devxploiticon.png 2>/dev/null || true
    fi
    echo -e "$green[+]$off Installed. Run: devxploit -u https://target.com -x"
    devxploit --help 2>/dev/null || python3 devxploit.py --help
}

if [[ $EUID -ne 0 ]]; then
    echo "Run as root: sudo ./install.sh"
    install_portable
    exit 1
fi

banner
if [ -d "/data/data/com.termux/files/usr/" ]; then
    termuxOS
elif [ -d "/usr/bin/" ]; then
    debianOS
else
    install_portable
    exit 1
fi
