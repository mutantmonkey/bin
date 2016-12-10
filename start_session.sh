#!/bin/zsh

# defaults
start_irc=0
start_ncmpcpp=0
start_messaging=1

# read arguments and set variables as appropriate
for arg in $@; do
    case "$arg" in
        "--irc")            start_irc=1;;
        "--ncmpcpp")        start_ncmpcpp=1;;
        "--no-messaging")   start_messaging=0;;
    esac
done

function spawn_tmux {
    # tmux window 1: irc (first window of session)
    if [[ "$start_irc" != 0 ]]; then
        tmux -u new -d -s0 -nirc "exec $IRC_COMMAND"
    else
        tmux -u new -d -s0 -nirc
    fi
    tmux set-window-option -t1 remain-on-exit on

    # tmux window 2: mail
    #tmux neww -d -t2 -nmail 'TERM=screen-256color exec alot'
    tmux neww -d -t2 -nmail
    tmux set-window-option -t2 remain-on-exit on

    # tmux window 3: task
    tmux neww -d -t3 -ntask
    tmux set-window-option -t3 remain-on-exit on

    # tmux window 4: music
    if [[ "$start_ncmpcpp" != 0 ]]; then
        tmux neww -d -t4 -nmusic 'exec ncmpcpp'
    else
        tmux neww -d -t4 -nmusic
    fi
    tmux set-window-option -t4 remain-on-exit on

    # tmux session: mail
    tmux -u new -d -smail -t0
    tmux select-window -t mail:2

    # tmux session: music
    tmux -u new -d -smusic -t0
    tmux select-window -t music:4
}

function restore_i3_layout {
    i3-msg "workspace 1; append_layout $HOME/.config/i3/workspace-1.json"
    nohup termite --role termite-tmux -e 'tmux a -t0' 2>/dev/null >/dev/null &
    nohup termite --role termite-mail -e 'tmux a -tmail' 2>/dev/null >/dev/null &
    nohup termite --role termite-music -e 'tmux a -tmusic' 2>/dev/null >/dev/null &
}

function connect_messaging {
    if [[ "$start_messaging" != 0 ]]; then
        sleep 5
        connect_xmpp.sh
    fi
}

spawn_tmux
restore_i3_layout
connect_messaging &
