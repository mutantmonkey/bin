#!/bin/sh
################################################################################
# flacenc.sh - Flac encoder preset
#
# author: mutantmonkey <mutantmonkey@gmail.com>
################################################################################

flac -8 -A "tukey(0.25)" -A "gauss(0.1875)" -b 4096 -V --sector-align $@

# -T "artist=%a" -T "title=%t" -T "album=%g" -T "date=%y" -T "tracknumber=%n" -T "genre=%m" 
