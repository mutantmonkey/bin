#!/usr/bin/python3
################################################################################
# lockd.py - lock screen using i3lock on org.freedesktop.login1.Session.Lock
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

import dbus
import subprocess
from gi.repository import GObject
from dbus.mainloop.glib import DBusGMainLoop

def handler(*args):
    subprocess.call(["i3lock", "-c", "000000"])

if __name__ == "__main__":
    bus = dbus.SystemBus(mainloop=DBusGMainLoop())
    bus.add_signal_receiver(handler, dbus_interface="org.freedesktop.login1.Session", signal_name="Lock")

    loop = GObject.MainLoop()
    loop.run()
