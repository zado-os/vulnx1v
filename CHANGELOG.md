#### v3.2.0 — 2026 exploit pack (50 per CMS)
- **350 new probes** (50 × WordPress, Joomla, PrestaShop, Drupal, OpenCart, Lokomedia, Magento)
- Engine: `modules/exploits/probes_2026/` (catalog + `probe_engine.py`)
- Total modules: **468** (legacy + 2026)

#### v3.1-devxploit (DevXploit — ZADO-OS Roger OS)
- Rebrand: **DevXploit** (`devxploit` / `devxploit.py`) — MSF-inspired console, `HIT`/`MISS` markers
- Shell payloads: `DevXploit.php` + `?DevXploit=1` (legacy `VulnX.*` mapped in `paths.py`)
- **119 modules:** Intel pack (14), WordPress extras (+10), Joomla multipart header fix
- Repo: https://github.com/zado-os/devxploit

#### v3.0-nexploit-only (Nexploit — drop vulnx)
- Removed `vulnx.py` — single entry: `nexploit.py` + `./nexploit`
- Install/update/Docker/CLI rebranded to Nexploit only
- Repo: https://github.com/zado-os/nexploit

#### v2.3-nexploit (Nexploit — ZADO-OS Roger OS)
- Rebrand: **Nexploit** (CLI `nexploit`) — repo [zado-os/nexploit](https://github.com/zado-os/nexploit)
- Launcher: `nexploit.py` · install path `/usr/share/nexploit`

#### v2.2-vulnnader
- 95 Exploits Scan modules (+ WP modern, Drupal, Magento, Joomla index)
- `common/branding.py`, `common/exploit_http.py`

#### v2.1-zado (ZADO-OS Roger OS Edition)
- Developer / maintainer: **ZADO-OS (Roger OS)**
- Unified Exploits Scan: 78+ modules (WP 17, Joomla 18, PS 27, Drupal 5, Lokomedia 6, OpenCart 5)
- New packs: `drupal_exploits.py`, `lokomedia_exploits.py`, `opencart_exploits.py`
- PrestaShop: megamenu, soopamobile, blocktestimonial, psmodthemeoptionpanel, homepageadvertise2
- Joomla: com_jdownloads, com_jdownloads2 enabled
- Fixes: PS shell `.text` check, WP blaze/catpro regex, Revslider shell URLs, PS `self.url` init
- Export hits to `-o` log files; `--list-exploits` / `--exploit-cms` extended

#### v2.0
- Add Module to get the operating system of target and web server name & version.
#### v1.9
- Add Vulnx−Mode `interactive mode`
- Add Command Line Interface Class `cli`
- Add Dork Functionnality to Vulnx−Mode
- Fix DNSDUMP Functionnality

#### v1.8
- Remove pip & rename conf to config to excute update without problem.
- Fix port arg to give port to scan.
- CI : Change pip package. 
- Docker : change pip package.
- Remove the ENV Variable.

#### v1.7
- add documentation vulnx for windows.
- add minor changes in dockerfile.
- add documentation for developper used vulnx library
- fix regEx in prestashop version.
- error handling and ignore warnings.

#### v1.6
- Added Payloads.
- Added PS Exploits
- Added Joomla Exploits
- Fix Issues
- Added Dorks Output {logs}
- Scan Multiple targets.
- Docker Using User. {`Fix Permissions`}
- Fix .travis {`CI`: Run tests after merge or pull requests}
- Listing Dorks {list `ps` , `joo` , `wp` , `dru`} exploits manually

#### v1.5
- Added 8 Prestashop Exploits.
- Added `Windows` & `MacOS` Comptability
- Fixed a few bugs
- Added vulnx to Docker from Ubuntu Image.

#### v1.4
- Fix parsing url
- Fix Robot Detected when you searching for dorks.
- Deserialize `json` data from dnsdumpster
- Added `Bot` Automate Scan
- Fix Modules Name
- Exports `Dorks` Search into file

#### v1.3
- Added vulnx to `PyPi`
- Added a `ports` scanner **plugin**.
- Improve `dorks` google searching. 
- Added `termux` compatibility & fix pip package.

#### v1.2
- Use of `ThreadPoolExecutor` for more speed
- Added pip packages.
- Added `travis.yml` continuous integration
- Added shields to README.MD

#### v1.1
- Added `--timeout` , `--exploits` , `--cms-info` , `--domains-info` ,  options
- Added `Dorks` list
- Fixed `Dork Search`
- Added `wordpress`, `joomla` ,`prestashop`, `drupal` , `lokomedia` , `magento` , `opencart`  CMS DETECT.
- Disabled `SSL` Warning
- Added `WP-Exploits`
- Fixed `Dockerfile`
