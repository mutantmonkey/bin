#!/usr/bin/python3
###############################################################################
# lockd.py - lock screen using i3lock on org.freedesktop.login1.Session.Lock
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
###############################################################################

import dbus
import subprocess
from gi.repository import GObject
from gi.repository import Notify
from dbus.mainloop.glib import DBusGMainLoop

Notify.init(__name__)


def lock(*args):
    # pause all notifications
    n = Notify.Notification.new("DUNST_COMMAND_PAUSE", None, None)
    n.show()

    subprocess.call(["i3lock", "-c", "000000", '--nofork'])

    # resume notifications
    n = Notify.Notification.new("DUNST_COMMAND_RESUME", None, None)
    n.show()


def unlock(*args):
    subprocess.call(['killall', 'i3lock'])

    # resume notifications
    n = Notify.Notification.new("DUNST_COMMAND_RESUME", None, None)
    n.show()


if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus(mainloop=DBusGMainLoop())
    bus.add_signal_receiver(lock,
                            dbus_interface="org.freedesktop.login1.Session",
                            signal_name="Lock")
    bus.add_signal_receiver(unlock,
                            dbus_interface="org.freedesktop.login1.Session",
                            signal_name="Unlock")

    loop = GObject.MainLoop()
    loop.run()
