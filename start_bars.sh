#!/bin/sh
#################################################################################
# start_bars.sh - bar script script (stalonetray and dzen2)
#
# author: mutantmonkey <mutantmonkey@gmail.com>
################################################################################

source $XDG_CONFIG_HOME/bars.conf

# Start stalonetray
stalonetray -c ~/.config/stalonetrayrc -bg "${BAR_BG}" -geometry ${BAR_TRAY_SLOTS}x1+${BAR_TRAY_X}+0 &

# Start dzen2
conky -c ~/.config/dzen/conkyrc | dzen2 -e 'button3=' -bg "${BAR_BG}" -fg "${BAR_FG}" -fn "${BAR_FONT}" -ta r -x "${BAR_RIGHT_X}" &

