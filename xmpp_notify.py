#!/usr/bin/python3
################################################################################
# xmpp_notify.py - xmpp-client notifications with libnotify
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import sys
from gi.repository import Notify


Notify.init("xmpp-client")

if len(sys.argv) > 0:
    msg = "new message: " + sys.argv[1]
else:
    msg = "new message"
n = Notify.Notification.new("xmpp-client", msg, 'dialog-information')
n.show()
