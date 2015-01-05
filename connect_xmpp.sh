#!/bin/zsh
################################################################################
# connect_xmpp.sh - spawn xmpp-client in tmux windows
#
# author: mutantmonkey <mutantmonkey@mutantmonkey.in>
################################################################################

for session in "${XMPP_SESSIONS[@]}"; do
    parts=("${(s/:/)session}")
    window="${parts[1]}"
    name="${parts[2]}"

    tmux new-window -d -t "$window" -n "xmpp:$name" \
        "xmpp-client -config-file $HOME/.config/xmpp-client/$name"
    tmux set-window-option -t "$window" remain-on-exit on
done
