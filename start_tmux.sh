#!/bin/sh
################################################################################
# start_tmux.sh - tmux start script
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

tmux -u new -d -s0 -nirc
tmux neww -d -t2 -nmutt
tmux neww -d -t3 -ntask
tmux neww -d -t4 -nncmpcpp

tmux -u new -d -smutt -t0
tmux -u new -d -sncmpcpp -t0
