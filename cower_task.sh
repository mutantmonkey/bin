#!/usr/bin/zsh

IFS=$'\n' pkgs=($(cower -bu | sed -r 's/^:: (\S+) .*$/\1/'))
for pkg in $pkgs; do
    description="Update package: $pkg"

    task "$description" >/dev/null
    if [ $? -eq 1 ]; then
        task add "$description" +arch
    fi
done
