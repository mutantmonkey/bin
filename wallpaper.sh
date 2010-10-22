#!/bin/sh

find $1 -type f -name '*.jpg' | shuf -n 1 | xargs feh --bg-scale
