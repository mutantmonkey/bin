#!/bin/bash

pkgs=$(cower -bu | sed 's/^:: \([A-Za-z0-9\.\-]*\) .*$/\1/')
for pkg in $pkgs; do
    description="Update package: $pkg"

    task "$description" >/dev/null
    if [ $? -eq 1 ]; then
        task add "$description" +arch
    fi
done
