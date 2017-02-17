#!/usr/bin/env python2

import sys
import os
import gtk
import pygtk
import shutil
import pynotify
import uuid
import subprocess
import time
import json

got_file = False
# if we got a file, we should copy and upload it
# otherwise just open the droppy directory with our preferred file explorer
try:
    # this throws an exception if we got no command line argument
    sys.argv[1]
    got_file = True
except:
    got_file = False

# we init the notification system
pynotify.init("Droppy")

# this will hold the dropbox information with the path to the Dropbox folder
info = ""
try:
    # we try to read and parse dropbox's config
    info = json.loads(open(os.path.expanduser("~/.dropbox/info.json")).read())
except IOError:
    # if the file could not be found, we display a notification
    pynotify.Notification("Dropbox folder not found!", \
                          "Droppy could not determine your Dropbox folder location, because the Dropbox config file is missing!", \
                          "dropbox").show()
    # and exit
    exit(1)

# this will hold the path of the dropbox folder
DropboxRoot = ""
try:
    # we try to get the path
    DropboxRoot = info["personal"]["path"]
except KeyError:
    # if it could not be found, we display a notification
    pynotify.Notification("Dropbox folder not found!", \
                          "Droppy could not determine your Dropbox folder location from the Dropbox config file!", \
                          "dropbox").show()
    # and exit
    exit(1)


if got_file:

    # we get the filename of the dropped file
    filename = os.path.basename(sys.argv[1])

    # where the file will be copied
    destination_path = DropboxRoot + "/Public/droppy/" + filename

    # create the droppy folder if it doesnt exist
    if not os.path.exists(DropboxRoot + "/Public/droppy/"):
        os.makedirs(DropboxRoot + "/Public/droppy/")

    # we copy the file, which will then be automatically uploaded to our dropbox
    # by the official dropbox daemon
    shutil.copy(sys.argv[1], destination_path)

    # this is the command to check the file status
    command = ["dropbox", "stat", destination_path]

    while True:

        # for a small delay between checks
        time.sleep(0.5)

        # we check the file status
        # and store only the last word (it is enough)
        status = subprocess.check_output(command).split()[-1]

        if status == "syncing":
            # if we are still syncing, just jump to the next iteration
            continue

        if status == "date":
            # if it says "up to date", we can display the notification and set
            # the clipboard contents

            # we get the clipboard
            clipboard = gtk.clipboard_get()
            # set its contents
            # we use the dropbox sharelink command, which returns the unique and safe URL
            # for a given file

            sharelink = subprocess.check_output(["dropbox", "sharelink", destination_path]).strip()

            # we replace the dl=0 parameter with raw=1
            # this way we can get a hotlink to the file with no dropbox decoration
            # (join dropbox popups, commenting, preview, etc.)
            if sharelink[-4:] == 'dl=0':
                sharelink = sharelink[:-4] + 'raw=1'

            clipboard.set_text(sharelink)
            # save the contents
            clipboard.store()

            # display a nice notification
            pynotify.Notification("\"" + filename + "\" copied!", \
                                  "The public URL is in your clipboard!", \
                                  "dropbox").show()

            break

        if status == "exist":
            # if the response was "file doesn't exist", we display an error

            pynotify.Notification("Error!", \
                                  "The file \"" + filename + "\" got unexpectedly deleted while uploading!", \
                                  "dropbox").show()

            break

        # in every other case, we display a notification about the fact that
        # we just dont know what happened
        pynotify.Notification("Droppy got ivalid response from Dropbox!", \
                              "Please check your file \"" + filename + "\" manually!", \
                              "dropbox").show()

        break

else:
    # if we didnt get any file, just open the droppy directory with the default file explorer
    os.system("xdg-open " + DropboxRoot + "/Public/droppy")
