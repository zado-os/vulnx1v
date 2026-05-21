from common.colors import bannerblue, bannerblue2, W, Y, G, R, end, msf_red, msf_dim
from common.branding import (
    APP_NAME,
    APP_VERSION,
    EDITION,
    MAINTAINER,
    MAINTAINER_ALIAS,
    REPO_URL,
    APP_TAGLINE,
)
from modules.exploits.exploit_scanner import exploit_module_total


def banner():
    total = exploit_module_total()
    print(msf_red + "       =[ %s v%s — %s ]=" % (APP_NAME, APP_VERSION, EDITION) + end)
    print(msf_dim + "+ -- --=[ %s ]=--" % APP_TAGLINE + end)
    print(msf_dim + "+ -- --=[ %d exploit modules loaded ]=--" % total + end)
    print("")
    print(bannerblue + "     .d8888b.                    d8b" + end)
    print(bannerblue + "    d88P  Y88b                   Y8P" + end)
    print(bannerblue + "    888    888" + bannerblue2 + " 888  888" + end)
    print(bannerblue + "    888    888" + bannerblue2 + " 888  888" + end)
    print(bannerblue + "    888    888" + bannerblue2 + " 888  888" + end)
    print(bannerblue + "    888    888" + bannerblue2 + " Y88b 888" + end)
    print(bannerblue + "    Y88b  d88P" + bannerblue2 + "  \"Y88888" + end)
    print(bannerblue + "     \"Y8888P\"" + bannerblue2 + "      888" + end)
    print(bannerblue + "              " + W + "DevXploit Framework" + end)
    print("")
    print(W + "  resource (repo) => " + G + REPO_URL + end)
    print(
        W + "  author          => "
        + G + MAINTAINER + W + " / " + MAINTAINER_ALIAS + end
    )
    print("")
