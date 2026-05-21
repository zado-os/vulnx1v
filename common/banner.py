from common.colors import bannerblue, bannerblue2, W, Y, G, end
from common.branding import APP_NAME, EDITION, MAINTAINER, MAINTAINER_ALIAS, REPO_URL


def banner():
    w = 58
    print(bannerblue + "+" + "=" * w + "+" + end)
    print(bannerblue + "|" + end + (G + ("  %s  " % APP_NAME).center(w)) + bannerblue + "|" + end)
    print(bannerblue + "|" + end + (Y + ("  %s  " % EDITION).center(w)) + bannerblue + "|" + end)
    print(bannerblue + "|" + end + W + "  CMS - Exploits Scan - Dorks - DNS - Ports  ".center(w) + bannerblue + "|" + end)
    print(bannerblue + "+" + "=" * w + "+" + end)
    print(bannerblue + "                    .:.        .:," + end)
    print(bannerblue + "                   xM;           XK." + end)
    print(bannerblue + "                  dx'            .lO." + end)
    print(bannerblue + "                 do                ,0." + end)
    print(bannerblue + "             .c.lN'      ,  '.     .k0.:'" + end)
    print(bannerblue + "              xMMk;d;''cOM0kWXl,',locMMX." + end)
    print(bannerblue + "               lMMO  lWMMMMMMMMMO. lMMO" + end)
    print(bannerblue + "                cWMxxMMMMMMMMMMMMKlWMk" + end)
    print(bannerblue + "                 .xWMMMMMMMMMMMMMMM0," + bannerblue2 + end)
    print(bannerblue + "                   .,OMd,,,;0MMMO,." + end)
    print(
        bannerblue + "             .l0O." + W + "NEXP" + bannerblue2 + "OX."
        + W + "NEXP" + bannerblue2 + "0MO" + W + "NEXP" + bannerblue + ".0Kd," + end
    )
    print(bannerblue + "             '0c      - " + Y + APP_NAME + bannerblue + " -      ,Ol" + end)
    print(bannerblue + "               ;.                     :." + end)
    print("")
    print(W + "  Repo    : " + G + REPO_URL + end)
    print(
        W + "  Credits : " + G + MAINTAINER + W + " (" + MAINTAINER_ALIAS + ")"
        + W + " | ZADO-OS Roger OS" + end
    )
    print("")
