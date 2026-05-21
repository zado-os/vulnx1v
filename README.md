<p align="center">
  <a href="https://github.com/zado-os/devxploit"><img src="https://i.ibb.co/ZxxFqxQ/vxv2.png" alt="DevXploit"></a>
  <br>
  <strong>DevXploit v4.2.1</strong> — ZADO-OS Roger OS Edition
  <br>
  <sub>588 modules · CVE match · Nuclei · WPScan · SQLi/XSS · PDF reports</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/version-4.2.1-red?style=flat-square" alt="version">
  <img src="https://img.shields.io/badge/Modules-588+-red?style=flat-square" alt="modules">
  <img src="https://img.shields.io/badge/License-GPL--3.0-green?style=flat-square" alt="license">
  <a href="https://github.com/zado-os/devxploit">
    <img src="https://img.shields.io/github/stars/zado-os/devxploit?style=flat-square" alt="stars">
  </a>
</p>

<p align="center">
  <a href="https://github.com/zado-os/devxploit/archive/refs/heads/main.zip">Download ZIP</a> •
  <a href="https://github.com/zado-os/devxploit">Repository</a> •
  <a href="https://github.com/zado-os/devxploit/issues">Issues</a>
</p>

---

## Maintainer

| | |
|--|--|
| **Author** | Hussain Al-zadjali — **[@zado-os](https://github.com/zado-os)** |
| **Project** | ZADO-OS Roger OS Edition |
| **Upstream** | [anouarbensaad/vulnx](https://github.com/anouarbensaad/vulnx) |

---

## Overview

**DevXploit** fingerprints CMS targets, runs **588** exploit modules (legacy + 2026 packs + frameworks), validates shells with strict rules, and optionally runs an **advanced pipeline**: CVE version matching, SQLi/XSS probes, WPScan API, Nuclei, searchsploit, JSON/HTML/PDF reports.

```bash
git clone https://github.com/zado-os/devxploit.git
cd devxploit
python3 -m pip install -r requirements.txt --break-system-packages
chmod +x devxploit install.sh
./devxploit -u https://target.example -x --full --report ./logs/report.json
```

---

## Features (v4.2)

| Feature | Flag / default | Description |
|---------|----------------|-------------|
| Exploit scan | `-x` | 588 modules, `[n/t]` progress |
| **Full power** | `--full` | CVE + SQLi/XSS + WPScan + Nuclei + MSF + PDF + rate-limit + double-verify |
| CVE auto-match | `-x` or `--cve-match` | Plugin `readme.txt` version vs `data/cve_db.json` + CVSS |
| Double shell verify | `-x` or `--double-verify` | Two GET checks before **HIT** |
| Rate-limit / WAF | `-x` or `--rate-limit` | Delay + User-Agent rotation |
| SQLi / XSS | `-x` or `--sqli-xss` | Reflection probes on common params |
| WPScan API | `--wpscan` / `--full` | Needs `export WPSCAN_API_TOKEN=...` |
| Nuclei | `--nuclei` / `--full` | External `nuclei` binary |
| searchsploit | `--msf-search` / `--full` | Exploit-DB lookup for CMS |
| Reports | `--report file.json` | JSON + HTML; PDF with `--pdf-report` or `--full` |
| Batch | `-i urls.txt --threads 5` | Parallel targets |
| TUI | `--tui` | `scan`, `cve`, `modules` commands |
| Filters | `--hits-only`, `--2026-only`, `--legacy-only` | Noise control |

### Result types

| Tag | Meaning |
|-----|---------|
| **HIT** | Confirmed shell (`php_uname` / upload form, double-checked if enabled) |
| **EXPOSE** | Backup, `.env`, installer leak |
| **INFO** | Plugin/path/CVE indicator — verify manually |
| **CVE** | Version matched against local CVE DB (CVSS in report) |
| **MISS** | Not vulnerable |

---

## Quick start (Kali Linux)

```bash
sudo apt update
sudo apt install python3 python3-pip git exploitdb -y   # exploitdb → searchsploit
git clone https://github.com/zado-os/devxploit.git
cd devxploit
git pull
python3 -m pip install -r requirements.txt --break-system-packages
sudo ./install.sh

# Recommended full scan
devxploit -u https://target.com -x --full --report /root/scan.json -o /root/logs

# Shell hits only (no false plugin HIT)
devxploit -u https://target.com -x --hits-only --double-verify

# Optional WPScan (free token at wpscan.com)
export WPSCAN_API_TOKEN="your_token"
devxploit -u https://target.com -x --full

# Optional Nuclei
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
devxploit -u https://target.com --nuclei
```

---

## CLI reference

```
devxploit -u URL -x [options]

Core
  -u, --url URL              Target
  -x, --exploit-scan         Exploit scan (enables CVE, SQLi/XSS, rate-limit, double-verify)
  --full                     All advanced tools (WPScan, Nuclei, MSF, PDF, …)
  --exploit-cms PACK         intel|wordpress|joomla|…|all
  --list-exploits PACK       Module catalog
  --hits-only                Hide MISS / INFO
  --min-severity LEVEL       info | expose | shell
  --legacy-only / --2026-only
  -i FILE --threads N        Batch scan
  --proxy URL
  --report FILE.json         JSON + HTML (+ PDF if --full / --pdf-report)
  -o DIR                     Log directory

Advanced (v4.2)
  --cve-match                Local CVE DB version match
  --wpscan                   WPScan API (WPSCAN_API_TOKEN)
  --nuclei                   Nuclei templates
  --sqli-xss                 SQLi/XSS reflection probes
  --rate-limit               WAF-friendly pacing
  --double-verify            Two-step shell confirmation
  --msf-search               searchsploit for CMS
  --pdf-report               PDF next to JSON report
  --tui                      Interactive dashboard
  --it                       Legacy interactive CLI
```

### Examples

```bash
devxploit -u https://site.tld -x --full --report scan.json
devxploit -u https://site.tld -x --hits-only
devxploit -u https://site.tld --exploit-cms wordpress --2026-only
devxploit -i targets.txt --threads 5 -x --full -o ./batch
devxploit --tui
devxploit --list-exploits all
```

---

## Module counts

| Pack | Legacy | 2026 | Total |
|------|--------|------|-------|
| Intel | 14 | — | 14 |
| WordPress | 32 | 50 | 82 |
| Joomla | 19 | 50 | 69 |
| PrestaShop | 28 | 50 | 78 |
| Drupal | 8 | 50 | 58 |
| OpenCart | 6 | 50 | 56 |
| Lokomedia | 6 | 50 | 56 |
| Magento | 5 | 50 | 55 |
| Laravel / Shopify / Moodle / Shopware | — | 30 each | 30 |
| **Total** | | | **588** |

---

## Project layout

```
devxploit.py                 Entry point
common/
  exploit_http.py            Shell / plugin verification
  cve_match.py               CVE + CVSS from data/cve_db.json
  wpscan_client.py           WPScan API
  nuclei_runner.py           Nuclei integration
  msf_search.py              searchsploit
  report_export.py           JSON / HTML / PDF
  rate_limit.py              WAF pacing
  double_verify.py           Two-step HIT
modules/
  exploits/                  588 module chains
  advanced/orchestrator.py   Post-scan pipeline
  tui/dashboard.py           --tui mode
  detector.py                CMS routing
data/cve_db.json             Local CVE ↔ plugin versions
docker-compose.yml           Official container
```

---

## Docker

```bash
docker compose build
docker compose run --rm devxploit -u https://example.com -x --full --report /devxploit/logs/report.json
```

Or:

```bash
docker build -t devxploit:4.2 -f docker/Dockerfile .
docker run -it --rm -v "$PWD/logs:/devxploit/logs" devxploit:4.2 -u http://target -x
```

---

## GitHub & updates

```bash
git pull
sudo ./update.sh
```

Repository: **https://github.com/zado-os/devxploit**

---

## Legal

Use only on systems you are authorized to test. Unauthorized access is illegal.

---

## License

[GPL-3.0](LICENSE) — maintained by **Hussain Al-zadjali (@zado-os)**.
