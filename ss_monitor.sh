#!/bin/bash

# screenshot uploader script for Droppy
#
# you need this only if you want to create a puush-like service by hand.
# set up your sceenshot app to create images in ~/Screenshots/.incoming/
# and this script will automatically rename it to the current timestamp
# and invoke Droppy, so you can instantly share it.

# this is to eliminate the for loop when no file found
shopt -s nullglob

# infinite loop, runs every second
while [[ true ]]; do

    # we scan for screenshot files in the special directory
    for i in ~/Screenshots/.incoming/*.png; do

        # get the current date and time, which will be in the filename
        stamp=`date +%Y-%m-%d_%H.%M.%S.%3N`

        # move the original file, so it gets uploaded only once, but
        # we can find it easily afterwards
        mv $i ~/Screenshots/ss_${stamp}.png

        # send it to Droppy, which will also append a hex
        /opt/droppy/droppy.py ~/Screenshots/ss_${stamp}.png

    done

    # frequent enough, but light on the CPU
    sleep 1

    # we could use something like inotify or incron to monitor the screenshots
    # directory, but this is much easier to set up and has no dependencies

done