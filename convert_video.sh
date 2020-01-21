#!/bin/sh

## Converts a videofile to accepted videoformat for use as
## Hyperkin Duke Xbox One controller LCD animation
##
## Author: tuxuser @ 01/2020

if ! [ -x "$(command -v ffmpeg)" ]; then
  echo 'Error: ffmpeg is not installed.' >&2
  exit 1
fi

if [ "$#" -ne 2 ]; then
  echo "ERROR: Invalid parameters!"
  echo "Usage: $0 [input_videofile] [output_videofile]"
  exit 1
fi

input_videofile="$1"
output_videofile="$2"

if [ ! -f "$input_videofile" ]; then
  echo "ERROR: Input videofile does not exist!"
  exit 2
fi

ffmpeg \
  -i "$input_videofile" \
  -an \
  -c:v mjpeg \
  -s 240x320 \
  -aspect 3:4 \
  -filter:v fps=fps=25 \
  "$output_videofile"
