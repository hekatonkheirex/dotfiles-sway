#!/usr/bin/env bash
filename="/home/mura/Pictures/Screenshots/$(date +'%Y.%m.%d-%H:%m:%S').png"
touch $filename
grim $filename
