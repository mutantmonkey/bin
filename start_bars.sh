#!/bin/sh
#################################################################################
# start_bars.sh - bar script script (dzen2)
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

conky -q -c ~/.config/dzen/conkyrc | dzen2 -dock -e 'button3=' -ta r -xs 1 &
