<h1 align="center">
  <br>
  <a href="https://github.com/zado-os/nexploit"><img src="https://i.ibb.co/ZxxFqxQ/vxv2.png" alt="Nexploit"></a>
  <br>
  <strong>Nexploit</strong> — ZADO-OS Roger OS Edition
  <br>
</h1>

<h4 align="center">
  <strong>ZADO-OS · Roger OS</strong> — فحص CMS، Exploits Scan، وحقن Shell تلقائي<br>
  <sub>Fork of <a href="https://github.com/anouarbensaad/vulnx">VulnX</a> by Anouar Ben Saad · maintained by ZADO-OS</sub>
</h4>

<p align="center">
  <img src="https://img.shields.io/badge/App-Nexploit-9cf?style=flat-square" alt="Nexploit">
  <img src="https://img.shields.io/badge/Developer-ZADO--OS-blue?style=flat-square" alt="ZADO-OS">
  <img src="https://img.shields.io/badge/Edition-Roger%20OS-green?style=flat-square" alt="Roger OS">
  <img src="https://img.shields.io/badge/Exploits-95%20modules-red?style=flat-square" alt="Exploits">
</p>

<p align="center">
  <a href="https://github.com/zado-os/nexploit">
    <img src="https://img.shields.io/github/stars/zado-os/nexploit?style=flat-square" alt="stars">
  </a>
  <a href="https://github.com/zado-os/nexploit/issues">
    <img src="https://img.shields.io/github/issues/zado-os/nexploit?style=flat-square" alt="issues">
  </a>
</p>

![Screenshot from 2019-06-19 05-22-04](https://user-images.githubusercontent.com/23563528/59736664-7c2fed00-9252-11e9-936d-53ea02628711.png)

<p align="center">
  <a href="https://github.com/zado-os/nexploit/archive/refs/heads/main.zip">Download ZIP</a> •
  <a href="https://github.com/zado-os/nexploit">Repository</a> •
  <a href="https://github.com/zado-os/nexploit/issues">Issues</a> •
  <a href="https://github.com/anouarbensaad/vulnx/wiki/Usage">Upstream Wiki</a> •
</p>

**Nexploit** ([zado-os/nexploit](https://github.com/zado-os/nexploit)) is an intelligent auto shell injector and CMS scanner. It detects the CMS, runs **95 Exploits Scan** modules with `[n/total]` progress, validates shells, and exports logs.

Maintained by **ZADO-OS (Roger OS)**. Based on [anouarbensaad/vulnx](https://github.com/anouarbensaad/vulnx) — same spirit, new name, sharper chains.

**Repository:** [github.com/zado-os/nexploit](https://github.com/zado-os/nexploit)

```bash
git clone https://github.com/zado-os/nexploit.git
cd nexploit
python3 -m pip install -r requirements.txt --break-system-packages   # Kali/Debian
chmod +x nexploit
./nexploit -u https://example.com --exploit-scan -o ./logs
```

> **Kali:** لا تستخدم `pip` أو `python` فقط — غالباً يشيران إلى **Python 2.7**. استخدم دائماً **`python3`** و **`pip3`** أو `./nexploit`.

-------------------------------------

### _🕷️ Features — ZADO-OS Roger OS_

#### CMS detection & intelligence
- Auto-detect: **WordPress, Joomla, PrestaShop, Drupal, OpenCart, Magento, Lokomedia / Lokomedia2**
- CMS info: themes, plugins, users, versions (`--cms`)
- Web / host OS & server fingerprint (`-w`, built-in server probe)
- Subdomain & domain gathering (`-d`)
- DNS dump + map export (`--dns`, `-o`)
- Port scan (`-p`)
- Multi-target from file (`-i`)

#### Exploits Scan (95 modules — verified chains)
| CMS | Modules | Command |
|-----|---------|---------|
| WordPress | 23 | `nexploit -u URL -x` |
| Joomla | 19 | `nexploit -u URL --exploit-cms joomla` |
| PrestaShop | 28 | `nexploit -u URL --exploit-cms prestashop` |
| Drupal | 8 | `nexploit -u URL --exploit-cms drupal` |
| Lokomedia | 6 | `nexploit -u URL --exploit-cms lokomedia` |
| OpenCart | 6 | `nexploit -u URL --exploit-cms opencart` |
| Magento | 5 | `nexploit -u URL --exploit-cms magento` |
| **All packs** | 95 | `nexploit -u URL --exploit-cms all` |

- CLI: `nexploit` أو `python3 nexploit.py` فقط (لا يوجد `vulnx`)
- Progress: `[7/23] WP File Manager VULN https://target/.../VulnX.php`
- Logs: `-o ./logs` → `exploits_wordpress.log`, etc.
- Catalog: `nexploit --list-exploits all`
- New probes: WP File Manager, Duplicator, Gravity Forms, WooCommerce, Elementor, Drupal Geddon2, Magento REST, OpenCart BruteForce

#### Automation & UX
- Interactive CLI (`--it`) — URLSET / DORKSET
- Exploit dork search (`-D`) + dork list (`-l`)
- Google dork paging (`-n`)
- Random User-Agent, SSL verify off, timeout-safe errors
- Linux / Termux / Windows / Docker

#### Payloads (`shell/`)
- `VulnX.php`, `VulnX.html`, `VulnX.txt`, `VulnX.php.png`, `VulnX.php.mp4` (auto-fallback paths)

- [`Ports Scan`](https://user-images.githubusercontent.com/23563528/58365946-40a83a00-7ec3-11e9-87c5-055ed67109b7.jpg) High Level
- [`Dns`](https://user-images.githubusercontent.com/23563528/58365784-09388e00-7ec1-11e9-8a05-e71fa39f146d.png) Servers Dump

-------------------------------------


### _🕷️ DNS-Map-Results_

To do this,run a scan with the --dns flag and -d for subdomains.
To generate a map of isetso.rnu.tn, you can run the command 
`nexploit -u isetso.rnu.tn --dns -d -o $PATH` in a new terminal.

`$PATH` : Where the graphs results will be stored.

![vokoscreen-2019-06-19_05-44-07](https://user-images.githubusercontent.com/23563528/59737395-696ae780-9255-11e9-9e09-26416de89bee.gif)


Let's generates an image displaying target Subdomains,MX & DNS data.


![demo](https://i.ibb.co/WfdhvWC/isetso-rnu-tn.png)

-------------------------------------

### _🕷️ Exploits Scan — Nexploit (95 modules)_
<h1 align="center">
<a href="https://github.com/zado-os/nexploit"><img src="https://user-images.githubusercontent.com/23563528/59737042-06c51c00-9254-11e9-87f8-876b33c87be1.gif" alt="Exploits Running"></a>
</h1>

> كل وحدة تُختبر عبر HTTP فعلي: رفع/طلب ثم التحقق من `Vuln X` في الاستجابة.  
> المصدر المرجعي للسلاسل: `modules/exploits/exploit_scanner.py`

##### Joomla (19) — `nexploit --list-exploits joomla`
| # | Module | Method | Status |
|---|--------|--------|--------|
| 1 | com_jce | `com_jce` | ✅ |
| 2 | com_media | `com_media` | ✅ |
| 3 | com_jdownloads | `com_jdownloads` | ✅ |
| 4 | com_jdownloads2 | `com_jdownloads2` | ✅ |
| 5 | com_jdownloads Index | `com_jdownloads_index` | ✅ NEW |
| 6 | com_fabrik | `com_fabrika` | ✅ |
| 7 | com_fabrik2 | `com_fabrikb` | ✅ |
| 8 | com_foxcontact | `com_foxcontact` | ✅ |
| 9 | com_ads_manager | `com_adsmanager` | ✅ |
| 10 | com_blog | `com_blog` | ✅ |
| 11 | com_users | `com_users` | ✅ |
| 12 | com_weblinks | `comweblinks` | ✅ |
| 13 | mod_simplefileupload | `mod_simplefileupload` | ✅ |
| 14 | com_jbcatalog | `com_jbcatalog` | ✅ |
| 15 | com_sexycontactform | `com_sexycontactform` | ✅ |
| 16 | com_rokdownloads | `com_rokdownloads` | ✅ |
| 17 | com_extplorer | `com_extplorer` | ✅ |
| 18 | com_jwallpapers | `com_jwallpapers` | ✅ |
| 19 | com_facileforms | `com_facileforms` | ✅ |

##### WordPress (23) — `nexploit --list-exploits wordpress`
| Module | EDB / ref |
|--------|-----------|
| Wysija, Blaze, Synoptic, Catpro, Cherry, Download Manager, Formcraft, Job Manager, Showbiz, WPshop, PowerZoom, Revslider (multi-path), SAM, InBoundio, Adblock, Levo, Thumbnail | [exploit-db.com](https://www.exploit-db.com) |
| **WP File Manager** (CVE-2020-25213), **Duplicator**, **Gravity Forms**, **WooCommerce Upload**, **Elementor**, **Contact Form 7** | ✅ NEW — ZADO-OS |

##### Drupal (8) — `nexploit --exploit-cms drupal`
| Module | Status |
|--------|--------|
| Avatar RCE, Drupalgeddon2 probe, **Geddon2 RCE**, **Add Admin**, **BruteForcer**, Install exposure, Views UI, files/VulnX | ✅ |

##### PrestaShop (28)
All README modules active: attributewizardpro, columnadverts, soopamobile, megamenu, pk_flex/vert, nvn_export, tdpstheme, psmodtheme, massedit, blocktestimonial, soopabanners, sliders, carts, videostab, wg24, fieldvmegamenu, wdoptionpanel, homepageadvertise(2), jro_homepage, advancedslider, etc.

##### Lokomedia (6) · OpenCart (6) · Magento (5)
| CMS | Highlights |
|-----|------------|
| Lokomedia | Admin upload, smiley, RSS, upload, config leak, filemanager |
| OpenCart | Filemanager, storage, vQmod, install, API, **BruteForce login** |
| Magento | REST API, downloader, config leak, media shell, cron.php |


-------------------------------------

### _🕷️ VulnxMode_ 
`NEW`
Nexploit interactive mode (`nexploit --it`).
***URLSET***

![vulnxmode_url](https://user-images.githubusercontent.com/23563528/68983791-fddd7400-080c-11ea-8e2b-c463a2c8f8c5.png)

***DORKSET***

![vulnxmode_dorks](https://user-images.githubusercontent.com/23563528/68985825-bf01eb00-0819-11ea-83ea-3db022b1d645.png)

-------------------------------------



### _🕷️ Available command line options_
[Upstream VulnX Wiki](https://github.com/anouarbensaad/vulnx/wiki/Usage) · [zado-os/nexploit](https://github.com/zado-os/nexploit)

Run `python nexploit.py -h` or `nexploit -h` after install.

    usage: nexploit [options]

      -u, --url             URL target to scan
      -D, --dorks           Search websites with dorks (exploit name)
      -o, --output          Specify output directory (DNS maps, dork logs)
      -n, --number-pages    Dork search: number of Google result pages (default: 1)
      -i, --input           Scan multiple domains from a text file (one URL per line)
      -l, --dork-list       List dork exploit names
                            choices: wordpress, prestashop, joomla, lokomedia, drupal, all
      -p, --ports           Port number to scan
      -e, --exploit         Search vulnerabilities and run exploits
      -x, --exploit-scan    Run Exploits Scan (per detected CMS)
      --exploit-cms         Force scan: wordpress, joomla, prestashop, drupal, lokomedia, opencart, all
      --list-exploits       List modules: wordpress, joomla, prestashop, drupal, lokomedia, opencart, all
      --it                  Interactive Nexploit mode (URLSET / DORKSET)
      --cms                 CMS info (themes, plugins, users, version, …)
      -w, --web-info        Web / host information gathering
      -d, --domain-info     Subdomain information gathering
      --dns                 DNS dump (subdomains, MX, maps via dnsdumpster)

### _🕷️ Requirements_

Python **3** only (`requirements.txt`):

    requests
    beautifulsoup4

```bash
python3 -m pip install -r requirements.txt --break-system-packages   # Kali
# أو
pip3 install -r requirements.txt
```

### _🕷️ Project layout_

    nexploit.py           Main entry point (only)
    install.sh            Install on Linux (root) / Termux
    update.sh             Update installed copy
    requirements.txt      Python dependencies
    common/               HTTP helpers, banner, colors, output
    modules/
      detector.py         CMS detection and scan orchestration
      cli/                Interactive mode
      dorks/              Dork search engine
      executor/           Per-CMS exploit runners
      exploits/           Exploit payloads
      gathering/          CMS / host intelligence
    shell/                Shell payloads (VulnX.php, VulnX.html, …)
    bin/                  Desktop launcher (nexploit.desktop)
    docker/               Dockerfile and Docker notes

-------------------------------------

### _🕷️ Docker_

Nexploit in Docker

```bash
$ git clone https://github.com/zado-os/nexploit.git
$ cd nexploit
$ docker build -t nexploit ./docker/
$ docker run -it --name nexploit nexploit:latest -u http://example.com
```

run Nexploit container in interactive mode


![vokoscreen-2019-06-23_11-53-20](https://user-images.githubusercontent.com/23563528/59975226-a31d5480-95ad-11e9-8252-ddd8291cbee4.gif)


to view logfiles mount it in a volume like so:

```bash
$ docker run -it --name nexploit -v "$PWD:/nexploit" nexploit:latest -u http://example.com
```

Volume mount: `/nexploit` (see `docker/Dockerfile`).

-------------------------------------

### _🕷️ Kali Linux (بدون install.sh)_

```bash
git clone https://github.com/zado-os/nexploit.git
cd nexploit
apt install -y python3 python3-pip
python3 -m pip install -r requirements.txt --break-system-packages
chmod +x nexploit
./nexploit -u https://mobile.punjigyan.com -x -o ./logs
```

| المشكلة | الحل |
|---------|------|
| `nexploit: command not found` | `./nexploit` من مجلد المشروع أو `sudo ./install.sh` |
| كتابة `nexploit.py` فقط | استخدم `python3 nexploit.py` أو `./nexploit` |
| `pip` → Python 2.7 | استخدم `python3 -m pip` وليس `pip` |

### _🕷️ Install Nexploit on Ubuntu / Kali (نظامي)_

```bash
git clone https://github.com/zado-os/nexploit.git
cd nexploit
sudo chmod +x install.sh
sudo ./install.sh
```

ثم:

```bash
nexploit -u http://example.com --exploit-scan
```

Portable:

```bash
python3 -m pip install -r requirements.txt --break-system-packages
chmod +x nexploit && ./nexploit -u http://example.com -x
```

![vokoscreen-2019-07-05_03-59-48](https://user-images.githubusercontent.com/23563528/60695392-7a645b80-9ed9-11e9-94fb-f6025594a9e3.gif)


### _🕷️ Install Nexploit on Termux_

```bash
$ pkg update
$ pkg install -y git python
$ git clone https://github.com/zado-os/nexploit.git
$ cd nexploit
$ chmod +x install.sh
$ ./install.sh
```

Run as root in Termux when prompted by the installer.
[**CLICK HERE TO SHOW THE RESULT**](https://user-images.githubusercontent.com/23563528/58364091-98847800-7ea6-11e9-9a9a-c27717e4dda1.png)


### _🕷️ Install Nexploit on Windows_

- [Download ZIP](https://github.com/zado-os/nexploit/archive/refs/heads/main.zip)
- Install [Python 3](https://www.python.org/downloads/)
- Unzip to `C:\nexploit`
- Open **cmd** or PowerShell:

```
> cd C:\nexploit
> pip install -r requirements.txt
> python nexploit.py -u http://example.com --exploit-scan
```

-------------------------------------

##### Exploits Scan (detected CMS)

```bash
nexploit -u http://example.com --exploit-scan
# or
nexploit -u http://example.com -x
```

##### Force Exploits Scan for a specific CMS

```bash
nexploit -u http://example.com --exploit-cms wordpress
nexploit -u http://example.com --exploit-cms all
```

##### List exploit modules by CMS

```bash
nexploit --list-exploits wordpress
nexploit --list-exploits all
```

##### Scan target: CMS info, subdomains, web info, exploits

```bash
nexploit -u http://example.com --cms -d -w --exploit
```

##### DNS map and subdomain dump

```bash
nexploit -u http://example.com --dns -d -o ./output
```

##### Interactive mode

```bash
nexploit --it
```

##### Dorks: list names, then search

```bash
nexploit --dork-list wordpress
nexploit -D blaze -n 2
```

##### Multiple targets from a file

```bash
nexploit -i targets.txt --cms -w
```

##### Port scan

```bash
nexploit -u http://example.com -p 80
```

-------------------------------------

### _🕷️ Versions_
- **v2.3-nexploit** — Rebrand **Nexploit**, 95 modules, CLI `nexploit`, [zado-os/nexploit](https://github.com/zado-os/nexploit)
- **v2.1-zado** — ZADO-OS Roger OS: Exploits Scan chains, Drupal/Lokomedia/OpenCart packs, log export
- [v2.0](https://github.com/anouarbensaad/vulnx/releases) — OS / web server detection (see `CHANGELOG.md`)
- [v1.9](https://github.com/anouarbensaad/vulnx/releases/tag/v1.9)
- [v1.8](https://github.com/anouarbensaad/vulnx/releases/tag/v1.8)
- [v1.7](https://github.com/anouarbensaad/vulnx/releases/tag/v1.7)
- [v1.6](https://github.com/anouarbensaad/vulnx/releases/tag/v1.6)
- [v1.5](https://github.com/anouarbensaad/vulnx/releases/tag/v1.5)
- [v1.4](https://github.com/anouarbensaad/vulnx/releases/tag/v1.4)
- [v1.3](https://github.com/anouarbensaad/vulnx/releases/tag/v1.3)
- [v1.2](https://github.com/anouarbensaad/vulnx/releases/tag/v1.2)
- [v1.1](https://github.com/anouarbensaad/vulnx/releases/tag/v1.1)

-------------------------------------

### :warning: Warning!

***I Am Not Responsible of any Illegal Use***

-------------------------------------

### _🕷️ Credits — ZADO-OS Roger OS_

| Role | Name |
|------|------|
| **Developer / Maintainer** | **ZADO-OS** (Roger OS) |
| **Original author** | Anouar Ben Saad ([@anouarbensaad](https://github.com/anouarbensaad)) |
| **Edition** | ZADO-OS Roger OS Edition — Exploits Scan engine |

All banners, install scripts, and scan output include **ZADO-OS · Roger OS** branding.

### _🕷️ Contribution & License_

Contributions welcome:

- Report bugs & issues
- Add exploit modules to `modules/exploits/exploit_scanner.py` chains
- Improve CMS fingerprints & accuracy

***Nexploit (ZADO-OS Roger OS Edition)*** is licensed under [GPL-3.0 License](LICENSE)

Original project: [anouarbensaad/vulnx](https://github.com/anouarbensaad/vulnx)
