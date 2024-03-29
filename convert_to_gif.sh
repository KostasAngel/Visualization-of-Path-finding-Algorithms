#!/usr/bin/env bash

## Converts individual pngs to a single gif in batches, requires ImageMagick and Gifsicle
## Adapted from https://askubuntu.com/a/573731

## Collect all png files in the files array
files=(*png)
## How many should be done at once
batch=200

## Read the array in batches of $batch
for ((i = 0; i < ${#files[@]}; i += batch)); do
  ## Convert this batch of frames to gif with ImageMagick
  convert -delay 2 -loop 0 "${files[@]:$i:$batch}" animated."$(printf "%05d" "$i")".gif
done

## Merge part gifs into a single file
## First merge into single gif
gifsicle --multifile ./*.gif -o all.gif

## Edit single gif to add delay on the last frame, and optimize it to reduce size (overwrites original file)
gifsicle --batch all.gif "#0--2" -d500 "#-1" -O3
