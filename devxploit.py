
#!/usr/bin/env python3

from __future__ import (absolute_import, division, print_function)

"""
DevXploit — CMS Detector, Exploits Scan & Shell Injector.
ZADO-OS Roger OS Edition · https://github.com/zado-os/devxploit
"""

from modules.detector import CMS
from modules.dorks.engine import Dork
from modules.dorks.helpers import DorkManual
try:
    from modules.cli.cli import CLI
except ImportError:
    CLI = None
from common.colors import red, green, bg, G, R, W, Y, G, good, bad, run, info, end, que, bannerblue2

from common.requestUp import random_UserAgent
from common.uriParser import parsing_url as hostd
from common.banner import banner

import sys
import argparse
import re
import os
import socket
import common
import warnings
import signal
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': random_UserAgent(),
    'Content-type': '*/*',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

_EXPLOIT_CMS = [
    'intel', 'wordpress', 'joomla', 'prestashop', 'drupal',
    'lokomedia', 'opencart', 'magento', 'all',
]

warnings.filterwarnings(
    action="ignore", message=".*was already imported", category=UserWarning)
warnings.filterwarnings(action="ignore", category=DeprecationWarning)

banner()


def parser_error(errmsg):
    print("Usage: devxploit [options]  (or: python3 devxploit.py -h)")
    print(R + "Error: " + errmsg + W)
    sys.exit()


def parse_args():
    parser = argparse.ArgumentParser(
        prog='devxploit',
        epilog='\tExample:\r\ndevxploit -u example.com --exploit-scan')
    parser.error = parser_error
    parser._optionals.title = "\nOPTIONS"
    parser.add_argument('-u', '--url', help="url target to scan")
    parser.add_argument(
        '-D', '--dorks', help='search webs with dorks', dest='dorks', type=str)
    parser.add_argument(
        '-o', '--output', help='specify output directory', required=False)
    parser.add_argument('-n', '--number-pages',
                        help='search dorks number page limit', dest='numberpage', type=int)
    parser.add_argument('-i', '--input', help='specify input file of domains to scan', dest='input_file', required=False)
    parser.add_argument('-l', '--dork-list', help='list names of dorks exploits', dest='dorkslist',
                        choices=['wordpress', 'prestashop', 'joomla', 'lokomedia', 'drupal', 'all'])
    parser.add_argument('-p', '--ports', help='ports to scan',
                        dest='scanports', type=int)
    parser.add_argument('-e', '--exploit', help='search vulnerability & run exploits',
                        dest='exploit', action='store_true')
    parser.add_argument('-x', '--exploit-scan', help='run CMS Exploits Scan (same as --exploit)',
                        dest='exploit_scan', action='store_true')
    parser.add_argument('--exploit-cms', dest='exploit_cms',
                        choices=_EXPLOIT_CMS,
                        help='force Exploits Scan for a CMS pack (or all)')
    parser.add_argument('--list-exploits', dest='list_exploits',
                        choices=_EXPLOIT_CMS,
                        help='list Exploits Scan modules')
    parser.add_argument('--it', help='interactive mode.',
                        dest='cli', action='store_true')
    parser.add_argument('--cms', help='search cms info[themes,plugins,user,version..]',
                        dest='cms', action='store_true')
    parser.add_argument('-w', '--web-info', help='web informations gathering',
                        dest='webinfo', action='store_true')
    parser.add_argument('-d', '--domain-info', help='subdomains informations gathering',
                        dest='subdomains', action='store_true')
    parser.add_argument('--dns', help='dns informations gatherings',
                        dest='dnsdump', action='store_true')
    return parser.parse_args()


args = parse_args()
url = args.url
input_file = args.input_file
warnings.filterwarnings('ignore')


def detection():
    run_exploit = args.exploit or args.exploit_scan
    instance = CMS(
        url,
        headers=HEADERS,
        exploit=run_exploit,
        domain=args.subdomains,
        webinfo=args.webinfo,
        serveros=True,
        cmsinfo=args.cms,
        dnsdump=args.dnsdump,
        port=args.scanports,
        force_cms=args.exploit_cms,
        output_dir=args.output,
    )
    instance.instanciate()


def dork_engine():
    if args.dorks:
        Dork(
            exploit=args.dorks,
            headers=HEADERS,
            pages=(args.numberpage or 1)
        ).search()


def dorks_manual():
    if args.dorkslist:
        DorkManual(select=args.dorkslist).list()


def interactive_cli():
    if args.cli:
        if CLI is None:
            print(bad + " Interactive mode requires readline (Linux/macOS)." + W)
            sys.exit(1)
        CLI(headers=HEADERS).general("")


def signal_handler(sig, frame):
    print("%s(ID: {}) Cleaning up...\n Exiting...".format(sig) % (W))
    exit(0)


signal.signal(signal.SIGINT, signal_handler)


def list_exploits_catalog():
    from modules.exploits.exploit_scanner import print_exploit_catalog
    print_exploit_catalog(args.list_exploits)


if __name__ == "__main__":

    if args.list_exploits:
        list_exploits_catalog()
        sys.exit(0)

    dork_engine()
    dorks_manual()
    interactive_cli()

    if url:
        root = url
        if root.startswith('http://') or root.startswith('https://'):
            url = root
        else:
            url = 'https://' + root
            print(url)
        detection()

    if input_file:
        with open(input_file, 'r') as urls:
            u_array = [line.strip('\n') for line in urls]
            try:
                for line in u_array:
                    if line.startswith('http'):
                        url = line
                    else:
                        url = 'https://' + line
                    detection()
            except Exception as error:
                print('error : ' + str(error))
