#!/bin/sh

# Force LibreOffice to use GTK+ theme
export OOO_FORCE_DESKTOP=gnome

# Set cursor name
xsetroot -cursor_name left_ptr

# Start statnot (should be configured to write to ~/.statnot)
statnot &

# Run xdg startup apps
dex -a &

# Hack to get unread counts working
update_unread_counts() {
	echo -n `check_gmail.py` > /dev/shm/gmail-${USER}
	echo -n `check_greader.py` > /dev/shm/greader-${USER}
	sleep 300
	update_unread_counts
};
(sleep 2 && update_unread_counts) &

exec xmonad
