#!/bin/sh
################################################################################
# start_tmux.sh - tmux start script
#
# author: mutantmonkey <mutantmonkey@gmail.com>
################################################################################

tmux new  -d -s0 -nirc 'exec ssh cubensis.mutantmonkey.in'
tmux neww -d -nmutt
tmux neww -d -nranger 'exec ranger'
tmux neww -d -nncmpcpp 'exec ncmpcpp'
tmux neww -d
tmux neww -d

tmux new -d -smutt -t0
tmux new -d -sncmpcpp -t0

