
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
from common.req_patch import apply_request_timeout
from common.colors import red, green, G, R, W, good, bad, run
from common.requestUp import random_UserAgent
from common.banner import banner
from common.scan_options import ScanOptions

apply_request_timeout()

import sys
import argparse
import warnings
import signal
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_EXPLOIT_CMS = [
    'intel', 'wordpress', 'joomla', 'prestashop', 'drupal',
    'lokomedia', 'opencart', 'magento', 'laravel', 'shopify', 'moodle', 'shopware', 'all',
]

warnings.filterwarnings(action="ignore", category=DeprecationWarning)


def build_headers(proxy=None):
    h = {
        'User-Agent': random_UserAgent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }
    if proxy:
        h['proxy'] = proxy
    return h


def parser_error(errmsg):
    print("Usage: devxploit [options]  (or: python3 devxploit.py -h)")
    print(R + "Error: " + errmsg + W)
    sys.exit()


def parse_args():
    parser = argparse.ArgumentParser(
        prog='devxploit',
        epilog='\tExample:\r\ndevxploit -u https://target.com -x --hits-only -o ./logs/report.json')
    parser.error = parser_error
    parser._optionals.title = "\nOPTIONS"
    parser.add_argument('-u', '--url', help="Target URL")
    parser.add_argument('-D', '--dorks', help='Search with dorks', dest='dorks', type=str)
    parser.add_argument('-o', '--output', help='Output directory or report.json path')
    parser.add_argument('-n', '--number-pages', dest='numberpage', type=int)
    parser.add_argument('-i', '--input', help='File with URLs (batch scan)', dest='input_file')
    parser.add_argument('-l', '--dork-list', dest='dorkslist',
                        choices=['wordpress', 'prestashop', 'joomla', 'lokomedia', 'drupal', 'all'])
    parser.add_argument('-p', '--ports', dest='scanports', type=int)
    parser.add_argument('-e', '--exploit', dest='exploit', action='store_true')
    parser.add_argument('-x', '--exploit-scan', dest='exploit_scan', action='store_true')
    parser.add_argument('--exploit-cms', dest='exploit_cms', choices=_EXPLOIT_CMS)
    parser.add_argument('--list-exploits', dest='list_exploits', choices=_EXPLOIT_CMS)
    parser.add_argument('--legacy-only', dest='legacy_only', action='store_true',
                        help='Run only classic exploit modules')
    parser.add_argument('--2026-only', dest='pack_2026', action='store_true',
                        help='Run only 2026 CVE/advisory pack')
    parser.add_argument('--hits-only', dest='hits_only', action='store_true',
                        help='Show only HIT/EXPOSE (hide MISS and most INFO)')
    parser.add_argument('--min-severity', dest='min_severity',
                        choices=['info', 'expose', 'shell'],
                        help='Minimum finding level to report')
    parser.add_argument('--threads', dest='threads', type=int, default=1,
                        help='Parallel threads for -i batch mode')
    parser.add_argument('--proxy', dest='proxy', help='HTTP proxy http://host:port')
    parser.add_argument('--report', dest='report',
                        help='JSON report path (default: output/report.json if -o set)')
    parser.add_argument('--it', dest='cli', action='store_true')
    parser.add_argument('--tui', dest='tui', action='store_true',
                        help='Interactive TUI dashboard')
    parser.add_argument('--full', dest='full', action='store_true',
                        help='Enable all advanced features (CVE, Nuclei, WPScan, SQLi/XSS, MSF, PDF)')
    parser.add_argument('--cve-match', dest='cve_match', action='store_true',
                        help='Match plugin versions vs local CVE DB')
    parser.add_argument('--wpscan', dest='wpscan', action='store_true',
                        help='WPScan API (needs WPSCAN_API_TOKEN)')
    parser.add_argument('--nuclei', dest='nuclei', action='store_true',
                        help='Run Nuclei templates if installed')
    parser.add_argument('--sqli-xss', dest='sqli_xss', action='store_true',
                        help='SQLi/XSS reflection probes')
    parser.add_argument('--rate-limit', dest='rate_limit', action='store_true',
                        help='Random delay + UA rotation (WAF friendly)')
    parser.add_argument('--double-verify', dest='double_verify', action='store_true',
                        help='Require two shell confirmations for HIT')
    parser.add_argument('--msf-search', dest='msf_search', action='store_true',
                        help='searchsploit lookup for detected CMS')
    parser.add_argument('--pdf-report', dest='pdf_report', action='store_true',
                        help='Also write PDF next to JSON report')
    parser.add_argument('--detect-only', dest='detect_only', action='store_true',
                        help='Detection only (INFO paths) — no real RCE/upload attempts')
    parser.add_argument('--real-exploit', dest='real_exploit', action='store_true',
                        help='Force real exploitation (default with -x)')
    parser.add_argument('--cms', dest='cms', action='store_true')
    parser.add_argument('-w', '--web-info', dest='webinfo', action='store_true')
    parser.add_argument('-d', '--domain-info', dest='subdomains', action='store_true')
    parser.add_argument('--dns', dest='dnsdump', action='store_true')
    return parser.parse_args()


def scan_kwargs_from_args(args):
    return dict(
        exploit=args.exploit or args.exploit_scan,
        domain=args.subdomains,
        webinfo=args.webinfo,
        serveros=True,
        cmsinfo=args.cms,
        dnsdump=args.dnsdump,
        port=args.scanports,
        force_cms=args.exploit_cms,
        output_dir=args.output if args.output and not args.output.endswith('.json') else None,
    )


def main():
    args = parse_args()
    pack_mode = None
    if args.legacy_only:
        pack_mode = 'legacy'
    if args.pack_2026:
        pack_mode = '2026'
    report_path = args.report
    if not report_path and args.output and str(args.output).endswith('.json'):
        report_path = args.output
    elif not report_path and args.output:
        import os
        report_path = os.path.join(args.output, 'devxploit_report.json')

    exploit_on = args.exploit or args.exploit_scan
    full = args.full
    ScanOptions.configure(
        pack_mode=pack_mode,
        hits_only=args.hits_only,
        min_severity=args.min_severity,
        threads=args.threads or 1,
        proxy=args.proxy,
        report_path=report_path,
        full_advanced=full,
        cve_match=full or args.cve_match or exploit_on,
        wpscan=full or args.wpscan,
        nuclei=full or args.nuclei,
        sqli_xss=full or args.sqli_xss or exploit_on,
        rate_limit=full or args.rate_limit or exploit_on,
        double_verify=full or args.double_verify or exploit_on,
        msf_search=full or args.msf_search,
        pdf_report=full or args.pdf_report,
        real_exploit=(exploit_on or args.real_exploit) and not args.detect_only,
    )

    HEADERS = build_headers(args.proxy)
    if args.proxy:
        import os
        os.environ['HTTP_PROXY'] = args.proxy
        os.environ['HTTPS_PROXY'] = args.proxy

    banner()

    if args.list_exploits:
        from modules.exploits.exploit_scanner import print_exploit_catalog
        print_exploit_catalog(args.list_exploits)
        return

    if args.dorks:
        Dork(exploit=args.dorks, headers=HEADERS, pages=(args.numberpage or 1)).search()
        return

    if args.dorkslist:
        DorkManual(select=args.dorkslist).list()
        return

    if args.tui:
        from modules.tui.dashboard import run_dashboard
        run_dashboard(HEADERS)
        return

    if args.cli:
        if CLI is None:
            print(bad + " Interactive mode requires readline (Linux/macOS)." + W)
            sys.exit(1)
        CLI(headers=HEADERS).general("")
        return

    skw = scan_kwargs_from_args(args)

    if args.input_file:
        from modules.batch_scan import run_batch
        with open(args.input_file, 'r') as fh:
            lines = fh.readlines()
        run_batch(lines, HEADERS, threads=args.threads or 3, **skw)
        return

    if args.url:
        url = args.url
        if not url.startswith('http'):
            url = 'https://' + url
            print(url)
        CMS(url=url, headers=HEADERS, **skw).instanciate()
        return

    parser.print_help()


def signal_handler(sig, frame):
    print("%s Cleaning up...\n" % W)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    main()
