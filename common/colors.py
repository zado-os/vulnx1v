'''
Terminal palette — DevXploit console (MSF-inspired layout, distinct styling).
'''

import sys

if sys.platform.lower().startswith(('os', 'win', 'darwin', 'ios')):
    bannerblue = bannerblue2 = yellowhead = \
        W = Y = R = G = B = bg = green = \
        run = good = bad = info = red = end = que = \
        hitexploit = missmark = portopen = portclose = msf_red = msf_dim = ''
else:
    msf_red = '\033[1;31m'
    msf_dim = '\033[0;37m'
    bannerblue = '\033[1;90m'
    bannerblue2 = '\033[1;31m'
    yellowhead = '\033[1;93m'
    W = '\033[1;37m'
    Y = '\033[1;33m'
    R = '\033[1;31m'
    G = '\033[1;32m'
    B = '\033[1;36m'
    bg = '\033[7;91m'
    green = '\033[1;32m'
    run = '\033[1;36m[*]\033[1;37m'
    good = '\033[1;32m[+]\033[1;37m'
    bad = '\033[1;31m[-]\033[1;37m'
    info = '\033[1;33m[!]\033[1;37m'
    red = '\033[1;31m'
    end = '\033[1;0m'
    que = '\033[1;90m[?]\033[1;37m'
    hitexploit = '\033[1;32mHIT\033[1m'
    missmark = '\033[1;31mMISS\033[1m'
    portopen = '\033[92mOPEN \033[1m'
    portclose = '\033[91mCLOSE\033[1m'

# Legacy aliases (internal imports)
failexploit = missmark
vulnexploit = hitexploit
