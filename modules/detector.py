
#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)

from common.colors import W,B,Y,good,end,run,info
from modules.executor.Wordpress import Wordpress
from modules.executor.Magento import Magento
from modules.executor.Prestashop import Prestashop
from modules.executor.Lokomedia import Lokomedia
from modules.executor.Lokomedia2 import Lokomedia2
from modules.executor.Drupal import Drupal
from modules.executor.Joomla import Joomla
from modules.executor.Uknown import Uknown
from modules.executor.Opencart import Opencart
from modules.executor.Framework import Framework
from common.cms_detect import detect_cms_scored, CLASS_MAP
from common.waf_detect import detect_waf
from common.report_export import reset_report, get_report

import re
import requests
import time
from requests.exceptions import RequestException


class CMS(object):

    def __init__(
        self,url,
        headers=None,
        exploit=False,
        domain=False,
        webinfo=False,
        serveros=False,
        cmsinfo=False,
        dnsdump=False,
        port=False,
        force_cms=None,
        output_dir=None,
        ):

        self.url = url
        self.headers = headers
        self.exploit = exploit
        self.force_cms = force_cms
        self.output_dir = output_dir
        self.domain = domain
        self.webinfo = webinfo
        self.serveros = serveros
        self.cmsinfo = cmsinfo
        self.dnsdump = dnsdump
        self.port = port
        self._cms_key = None
        self._cms_confidence = 0

    def __fetch__(self, target_url, default=''):
        try:
            return requests.get(
                target_url,
                headers=self.headers,
                verify=False,
                timeout=12,
            ).text
        except RequestException:
            return default

    def __getlmcontent__(self):
        return self.__fetch__(self.url + '/smiley/1.gif')

    def __getlm2content__(self):
        return self.__fetch__(self.url + '/rss.xml')

    def __getcontent__(self):
        return self.__fetch__(self.url)

    def __getexploit__(self):
        if self.exploit:
            return True

    def __getdomain__(self):
        if self.domain:
            return True

    def __getwebinfo__(self):
        if self.webinfo:
            return True

    def __getserveros__(self):
        if self.serveros:
            return True

    def __getcmsinfo__(self):
        if self.cmsinfo:
            return True

    def __getdnsdump__(self):
        if self.dnsdump:
            return True

    def __getport__(self):
        if self.port:
            return self.port

    def detect(self):
        """Multi-signal CMS detection with confidence score."""
        html = self.__getcontent__()
        try:
            lm = self.__getlmcontent__()
            if lm:
                html += lm
        except Exception:
            pass
        display, confidence, ranked = detect_cms_scored(
            self.url, self.headers, extra_html=html
        )
        self._cms_confidence = confidence
        if ranked:
            self._cms_key = ranked[0][0]
        else:
            self._cms_key = "unknown"
        if display == "Unknown" and re.search(r"lokomedia", self.__getlm2content__() or "", re.I):
            self._cms_key = "lokomedia2"
            display = "Lokomedia2"
        return display

    def serialize(self):
        result = dict(
            name=self.detect(),
            exploit=self.__getexploit__(),
            domain=self.__getdomain__(),
            webinfo=self.__getwebinfo__(),
            serveros=self.__getserveros__(),
            cmsinfo=self.__getcmsinfo__(),
            dnsdump=self.__getdnsdump__(),
            port=self.__getport__()
        )
        return result

    def _resolve_cms_class(self, detected_name):
        from modules.exploits.exploit_scanner import CMS_CLASS_NAMES
        if self.force_cms:
            key = self.force_cms.lower()
            if key != 'all':
                name = CMS_CLASS_NAMES.get(key)
                if name:
                    detected_name = name
        fw_keys = ("laravel", "shopify", "moodle", "shopware")
        if self._cms_key in fw_keys or (detected_name or "").lower() in fw_keys:
            return Framework
        try:
            return globals()[detected_name]
        except KeyError:
            return Uknown

    def _run_exploit_scan(self, cms_name, instance):
        from modules.exploits.exploit_scanner import (
            run_forced_cms_scan,
            probe_and_scan_unknown,
        )
        if self.force_cms and self.force_cms.lower() == 'all':
            run_forced_cms_scan('all', self.url, self.headers, output_dir=self.output_dir)
            return
        if cms_name == 'Uknown':
            probe_and_scan_unknown(self.url, self.headers, output_dir=self.output_dir)
            return
        instance.exploit(output_dir=self.output_dir)

    def instanciate(self):
        init_time = time.time()
        reset_report(self.url)
        cms = self.serialize()
        if cms['name']:
            cms_class = self._resolve_cms_class(cms['name'])
            if cms_class is Framework:
                instance = cms_class(
                    self.url, self.headers, fw_type=self._cms_key or "laravel"
                )
            else:
                instance = cms_class(self.url, self.headers)
            display_cms = cms_class.__name__
            if cms_class is Framework:
                display_cms = (self._cms_key or "framework").capitalize()
            if self.force_cms:
                display_cms += ' [exploit: %s]' % self.force_cms
            waf = detect_waf(self.url, self.headers)
            get_report().set_meta(
                cms=display_cms, confidence=self._cms_confidence, waf=waf
            )
            print ('\n {0}[{1}Target{2}]{3} => {4}{5} \n '.format(B,W,B, W, self.url, end))
            print ("{0} −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−".format(W))
            print (' {0} looking for cms' .format(run))
            print (' {0} CMS : {1} ({2}% confidence)' .format(
                good, display_cms, self._cms_confidence))
            if waf:
                print (' {0} WAF/CDN : {1}' .format(info, ", ".join(waf)))
            if cms['exploit']:
                self._run_exploit_scan(cms['name'], instance)
                from modules.advanced.orchestrator import run_advanced_pipeline
                run_advanced_pipeline(
                    self.url, self.headers, cms_name=display_cms,
                )
            if cms['webinfo']:
                print ("{0} −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−".format(W))
                print(' {0} Web Hosting Information'.format(run))
                instance.webinfo()
            if cms['serveros']:
                print ("{0} −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−".format(W))
                print(' {0} OS / Server Information'.format(run))
                instance.serveros()
            if cms['cmsinfo']:
                print ("{0} −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−".format(W))
                print(' {0} CMS Information Gathering'.format(run))
                instance.cmsinfo()
                print ("{0} −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−".format(W))
            if cms['dnsdump']:
                instance.dnsdump()
            if cms['domain']:
                instance.domaininfo()
            if cms['port']:
                instance.ports(cms['port'])
        end_time = time.time()
        elapsed_time = end_time - init_time
        print('\n %s[%s Elapsed Time %s]%s => %.2f seconds ' % (Y,W,Y,W,elapsed_time))
        from common.scan_options import ScanOptions
        opts = ScanOptions.get()
        if opts.report_path:
            path = opts.report_path
            get_report().write_json(path)
            if path.endswith(".json"):
                html_p = path.replace(".json", ".html")
                get_report().write_html(html_p)
                print(' {0} Report saved: {1} + {2}'.format(good, path, html_p))
                if opts.pdf_report or opts.full_advanced:
                    pdf_p = path.replace(".json", ".pdf")
                    if get_report().write_pdf(pdf_p):
                        print(' {0} PDF report: {1}'.format(good, pdf_p))
            else:
                print(' {0} Report saved: {1}'.format(good, path))