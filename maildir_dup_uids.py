#!/usr/bin/python3

import re
import os

uid_re = re.compile(r'U=(\d+):\d,')
uids = []

for filename in os.listdir(os.path.expanduser('~/.mail/main/spam/cur')):
    m = uid_re.search(filename)
    if m:
        uid = int(m.group(1))
        if uid in uids:
            print("duplicate UID: {}".format(filename))
        else:
            uids.append(uid)
    else:
        print(filename)
