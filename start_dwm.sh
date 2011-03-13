#!/bin/sh
#################################################################################
# start_dwm.sh - dwm start script
#
# author: mutantmonkey <mutantmonkey@gmail.com>
################################################################################

# Start bars
(sleep $SPAWN_DELAY && start_bars.sh) &
#conky -c ~/.config/dwm/conkyrc | while read -r; do xsetroot -name "$REPLY"; done &

# Run xdg startup apps
dex -a

# Hack to get unread counts working
update_unread_counts() {
	echo -n `check_gmail.py` > /dev/shm/gmail-${USER}
	echo -n `check_greader.py` > /dev/shm/greader-${USER}
	sleep 300
	update_unread_counts
};
(sleep $SPAWN_DELAY && update_unread_counts) &

exec dwm

