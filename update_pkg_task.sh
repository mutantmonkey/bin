#!/usr/bin/zsh

IFS=$'\n' pkgs=($(sed -r 's/^:: (\S+) .*$/\1/'))
for pkg in $pkgs; do
    description="Update package: $pkg"

    task "status=pending description=\"$description\"" minimal >/dev/null 2>&1
    if [ $? -eq 1 ]; then
        task add +arch -- "$description"
    fi
done
