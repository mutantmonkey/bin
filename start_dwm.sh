#!/bin/sh

# Force LibreOffice to use GTK+ theme
export OOO_FORCE_DESKTOP=gnome

# Set cursor name
xsetroot -cursor_name left_ptr

# Start statnot (should be configured to write to ~/.statnot)
#statnot &

# Bars {{{

BAR_FONT="DejaVu Sans Mono-9"
BAR_FG="#aaaaaa"
BAR_BG="#111111"

BAR_LEFT_WIDTH=300
BAR_TRAY_X=1100
BAR_TRAY_SLOTS=6
BAR_RIGHT_X=1202

# Start stalonetray
(sleep 2 && stalonetray -c ~/.config/stalonetrayrc -geometry ${BAR_TRAY_SLOTS}x1+${BAR_TRAY_X}+0) &

# Start dzen2
(sleep 2 && conky -c ~/.config/dzen/conkyrc | dzen2 -bg "${BAR_BG}" -fg "${BAR_FG}" -fn "${BAR_FONT}" -ta r -x "${BAR_RIGHT_X}") &

#conky -c ~/.config/dwm/conkyrc | while read -r; do xsetroot -name "$REPLY"; done &

# }}}

# Run xdg startup apps
(sleep 2 && dex -a) &

# Hack to get unread counts working
update_unread_counts() {
	echo -n `check_gmail.py` > /dev/shm/gmail-${USER}
	echo -n `check_greader.py` > /dev/shm/greader-${USER}
	sleep 300
	update_unread_counts
};
(sleep 2 && update_unread_counts) &

#exec dwm

# Start dwm in an infinite loop so that we can restart it without killing apps
while true; do
	# Log stderror to a file 
	dwm 2> ~/.dwm.log
	# No error logging
	#dwm >/dev/null 2>&1
done

