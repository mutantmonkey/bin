#!/usr/bin/python2
#################################################################################
# check_gvoice.py - Check unread messages on Google Voice
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import googlevoice
import netrc

# get login info
nrc = netrc.netrc()
auth = nrc.authenticators('google.com')
username = auth[0]
password = auth[2]

voice = googlevoice.Voice()
voice.login(username, password)

unread_count = voice.inbox().unreadCounts['all']

f = open('/dev/shm/gvoice-mutantmonkey', 'w')
f.write(str(unread_count))
f.close()

#print(unread_count)
