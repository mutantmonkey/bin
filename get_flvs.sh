#!/bin/bash
################################################################################
# get_flvs.sh - Get FLV files stored by Flash in /tmp
#
# author: Tom Glenne
# http://www.omgubuntu.co.uk/2010/09/64bit-flash-for-ubuntu/#comment-78723833
################################################################################

DEST="$HOME"
PID=`ps x | grep libflashplayer.so | grep -v grep | awk '{print $1}'`
FD=`lsof -p $PID | grep Flash | awk '{print $4}' | sed 's/u$//'`

while IFS=' ' read -ra ADDR; do
for x in "${ADDR[@]}"; do
# process "$x"
FN=`mktemp --tmpdir="$DEST"` # create a temp file
cp "/proc/$PID/fd/$x" "$FN" # copy video to the temp file
S=`du -h "$FN" | awk '{print $1}'` # get its size
echo "copied video $x to $FN ($S)" # print info
done
done <<< "$FD"

