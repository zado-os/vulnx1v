import re
import socket
import subprocess

import requests
from requests.exceptions import RequestException

from common.colors import bad, good, W, end
from common.uriParser import parsing_url as hostd

REQUEST_TIMEOUT = 12


class GatherHost():

    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers or {}

    def match_info(self, regex, data):
        match = re.search(regex, data)
        if match:
            return dict(data=match.group(1))

    def match_printer(self, to_match, match):
        if match and match.get('data'):
            print(' {0} {1} : {2}'.format(good, to_match, match['data']))

    def _domain_creation_date(self, domain):
        """Resolve domain registration date via whois, then RDAP."""
        date = self._whois_creation_date(domain)
        if date:
            return date
        return self._rdap_creation_date(domain)

    def _whois_creation_date(self, domain):
        try:
            proc = subprocess.run(
                ['whois', domain],
                capture_output=True,
                text=True,
                timeout=REQUEST_TIMEOUT,
            )
            output = (proc.stdout or '') + (proc.stderr or '')
            patterns = [
                r'Creation Date:\s*(.+)',
                r'Created On:\s*(.+)',
                r'created:\s*(.+)',
                r'Domain Registration Date:\s*(.+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, output, re.I)
                if match:
                    return match.group(1).strip()
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass
        return None

    def _rdap_creation_date(self, domain):
        try:
            url = 'https://rdap.org/domain/{0}'.format(domain)
            resp = requests.get(
                url,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT,
                verify=False,
            )
            if resp.status_code != 200:
                return None
            data = resp.json()
            events = data.get('events') or []
            for event in events:
                if event.get('eventAction') in ('registration', 'registered'):
                    return event.get('eventDate')
        except (RequestException, ValueError, KeyError):
            pass
        return None

    def _print_ipinfo(self, ip):
        try:
            ipinfo = 'https://ipinfo.io/{0}/json'.format(ip)
            gather = requests.get(
                ipinfo,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT,
            ).text
            self.match_printer('Country', self.match_info(r'"country":\s*"(.+?)"', gather))
            self.match_printer('Region', self.match_info(r'"region":\s*"(.+?)"', gather))
            self.match_printer('Timezone', self.match_info(r'"timezone":\s*"(.+?)"', gather))
            self.match_printer('Postal', self.match_info(r'"postal":\s*"(.+?)"', gather))
            self.match_printer('Org', self.match_info(r'"org":\s*"(.+?)"', gather))
            self.match_printer('Location', self.match_info(r'"loc":\s*"(.+?)"', gather))
        except RequestException as err:
            print(' {0} IP geolocation unavailable: {1}'.format(bad, err))

    def os_server(self):
        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                verify=False,
                timeout=REQUEST_TIMEOUT,
            ).headers
        except RequestException as err:
            print(' {0} Cannot connect to target: {1}'.format(bad, err))
            return
        try:
            regx = re.compile(r'(.+) \((.+)\)')
            data = regx.search(response.get('server', ''))
            if data:
                print(' {0} {1}Server :{2} {3}'.format(good, W, end, data.group(1)))
                print(' {0} {1}OS :{2} {3}'.format(good, W, end, data.group(2)))
            else:
                server = response.get('server')
                if server:
                    print(' {0} {1}Server :{2} {3}'.format(good, W, end, server))
                else:
                    print(' {0} Cannot Find OS & HostingServer '.format(bad))
        except (AttributeError, TypeError):
            print(' {0} Cannot Find OS & HostingServer '.format(bad))

    def web_host(self):
        domain = hostd(self.url)
        creation = self._domain_creation_date(domain)
        if creation:
            print(' {0} Domain Created on : {1}'.format(good, creation))
        else:
            print(' {0} Domain creation date unavailable'.format(bad))

        try:
            ip = socket.gethostbyname(domain)
            print(' {0} IP Address : {1}'.format(good, ip))
            self._print_ipinfo(ip)
        except socket.gaierror:
            print(' {0} Cannot resolve hostname: {1}'.format(bad, domain))
