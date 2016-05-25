#!/bin/zsh -y

inputs=("$(pactl list short sink-inputs | cut -f1,4 --output-delimiter=:)")

for line in $inputs; do
    s=("${(@s/:/)line}")
    if [[ "${s[2]}" == "module-rtp-recv.c" ]]; then
        input_index="${s[1]}"
        break
    fi
done

if [ -z "$input_index" ]; then
    exit 1
fi

case "$1" in
    mute)
        pactl set-sink-input-mute "$input_index" toggle
        ;;
    up)
        pactl set-sink-input-volume "$input_index" +2%
        ;;
    down)
        pactl set-sink-input-volume "$input_index" -2%
        ;;
esac
