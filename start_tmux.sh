#!/bin/sh
################################################################################
# start_tmux.sh - tmux start script
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

tmux -u new -d -s0 -nirc
tmux neww -d -nmutt
tmux neww -d -ntask
tmux neww -d -nncmpcpp
tmux neww -d -ncanto

tmux -u new -d -smutt -t0
tmux -u new -d -sncmpcpp -t0
