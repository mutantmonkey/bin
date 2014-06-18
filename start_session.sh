#!/bin/zsh

function spawn_tmux {
    start_irc=0
    start_ncmpcpp=0

    # read arguments and set variables as appropriate
    for arg in $@; do
        case "$arg" in
            "--irc")        start_irc=1;;
            "--ncmpcpp")    start_ncmpcpp=1;;
        esac
    done

    # tmux window 1: irc (first window of session)
    if [[ "$start_irc" != 0 ]]; then
        tmux -u new -d -s0 -nirc "exec $IRC_COMMAND"
    else
        tmux -u new -d -s0 -nirc
    fi
    tmux set-window-option -t1 remain-on-exit on

    # tmux window 2: alot
    tmux neww -d -t2 -nalot 'exec alot'
    tmux set-window-option -t2 remain-on-exit on

    # tmux window 3: task
    tmux neww -d -t3 -ntask
    tmux set-window-option -t3 remain-on-exit on

    # tmux window 4: ncmpcpp
    if [[ "$start_ncmpcpp" != 0 ]]; then
        tmux neww -d -t4 -nncmpcpp 'exec ncmpcpp'
    else
        tmux neww -d -t4 -nncmpcpp
    fi
    tmux set-window-option -t4 remain-on-exit on

    # tmux session: alot
    tmux -u new -d -salot -t0
    tmux select-window -t alot:2

    # tmux session: ncmpcpp
    tmux -u new -d -sncmpcpp -t0
    tmux select-window -t ncmpcpp:4
}

function restore_i3_layout {
    i3-msg "workspace 1; append_layout $HOME/.config/i3/workspace-1.json"
    roxterm --role roxterm-tmux -e 'tmux a -t0'
    roxterm --role roxterm-alot -e 'tmux a -talot'
    roxterm --role roxterm-ncmpcpp -e 'tmux a -tncmpcpp'
}

spawn_tmux $@
restore_i3_layout
