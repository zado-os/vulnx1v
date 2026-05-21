#!/bin/bash
# Nexploit installer — ZADO-OS Roger OS (Python 3 only)

red="\e[0;31m"
blue="\e[0;94m"
green="\e[0;32m"
off="\e[0m"

REPO="https://github.com/zado-os/nexploit.git"
INSTALL_DIR="/usr/share/nexploit"
TERMUX_DIR="/data/data/com.termux/files/usr/share/nexploit"

banner() {
    echo -e "===== Nexploit INSTALL — ZADO-OS Roger OS ====="
}

install_portable() {
    echo -e "$red [$green+$red]$off Use: chmod +x nexploit && ./nexploit -u URL -x"
    echo -e "$red [$green+$red]$off Or: python3 nexploit.py -u URL -x"
}

termuxOS() {
    echo -e "$red [$green+$red]$off Installing Python3 ..."
    pkg install -y python git
    python3 -m pip install -r ./requirements.txt 2>/dev/null || pip3 install -r ./requirements.txt
    if [ -d "$TERMUX_DIR" ]; then
        echo -e "$red [$green+$red]$off Replace old install? [Y/n]:"
        read replace
        if [ "$replace" = "y" ] || [ "$replace" = "Y" ] || [ -z "$replace" ]; then
            rm -rf "$TERMUX_DIR"
            rm -f "/data/data/com.termux/files/usr/bin/nexploit"
        else
            exit 1
        fi
    fi
    mkdir -p "$TERMUX_DIR"
    cp -r common modules shell nexploit.py install.sh update.sh nexploit requirements.txt "$TERMUX_DIR/"
    chmod +x "$TERMUX_DIR/nexploit" 2>/dev/null || true
    cat > /data/data/com.termux/files/usr/bin/nexploit << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
exec python3 /data/data/com.termux/files/usr/share/nexploit/nexploit.py "$@"
EOF
    chmod +x /data/data/com.termux/files/usr/bin/nexploit
    echo -e "$green[+]$off Run: nexploit"
    nexploit --help 2>/dev/null || python3 nexploit.py --help
}

debianOS() {
    echo -e "$red [$green+$red]$off Installing python3 ..."
    apt-get install -y python3 python3-pip git whois
    python3 -m pip install -r ./requirements.txt --break-system-packages 2>/dev/null \
        || python3 -m pip install -r ./requirements.txt --user 2>/dev/null \
        || python3 -m pip install -r ./requirements.txt
    if [ -d "$INSTALL_DIR" ]; then
        echo -e "$red [$green+$red]$off Replace $INSTALL_DIR? [Y/n]:"
        read replace
        if [ "$replace" = "y" ] || [ "$replace" = "Y" ] || [ -z "$replace" ]; then
            rm -rf "$INSTALL_DIR"
            rm -f /usr/local/bin/nexploit
        else
            exit 1
        fi
    fi
    mkdir -p "$INSTALL_DIR"
    cp -r common modules shell nexploit.py install.sh update.sh nexploit requirements.txt "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/nexploit" "$INSTALL_DIR/update.sh" 2>/dev/null || true
    cat > /usr/local/bin/nexploit << EOF
#!/bin/bash
exec python3 ${INSTALL_DIR}/nexploit.py "\$@"
EOF
    chmod +x /usr/local/bin/nexploit
    if [ -f bin/nexploit.desktop ]; then
        cp bin/nexploit.desktop /usr/share/applications/ 2>/dev/null || true
    fi
    if [ -f bin/nexploiticon.png ]; then
        cp bin/nexploiticon.png /usr/share/icons/ 2>/dev/null || true
    elif [ -f bin/vulnxicon.png ]; then
        cp bin/vulnxicon.png /usr/share/icons/nexploiticon.png 2>/dev/null || true
    fi
    echo -e "$green[+]$off Installed. Run: nexploit -u https://target.com -x"
    nexploit --help 2>/dev/null || python3 nexploit.py --help
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
