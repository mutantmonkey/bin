#!/bin/sh
################################################################################
# start_tmux.sh - tmux start script
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

tmux -u new -d -s0 -nirc
#tmux neww -d -t2 -nmutt

tmux neww -d -t2 -nalot 'exec alot'
tmux set-window-option -t2 remain-on-exit on

tmux neww -d -t3 -ntask
tmux neww -d -t4 -nncmpcpp

tmux -u new -d -salot -t0
#tmux set -tmutt status off

tmux -u new -d -sncmpcpp -t0
#tmux set -tncmpcpp status off
