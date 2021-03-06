# Droppy

![Screenshot of Droppy](screenshot.png)

**The easiest and most convenient file-sharing utility based on Dropbox.**

Drop any file on its icon, and it will be uploaded to your Dropbox, with the public URL copied to your clipboard!


## Features

* insanely convenient
* no configuration needed, It Just Works(TM)
* cute notifications
* really small
* well-documented code


## Installation

- Download the source and run the install script `INSTALL` as superuser.
- Add it's application icon to your dock or whatever, or simply invoke `droppy` anywhere with a filename as a parameter.
- Profit!


## Optional screenshot uploader

So there is [puush](http://puush.me/) for Windows, which is a super handy tool to share screenshots instantly - but is not available on Linux... I wanted to create the same experience with Droppy, so I did, with the help of Compiz. (this is compiz-dependant in my case, but you could likely use some other tools, like Shutter or etc.)

The main components are:

* a screenshooter tool, which should paste the images in `~/Screenshots/.incoming/`
* a background script, which periodically scans this directory
* Droppy, which does its thing

How to set up:

* Tell your screenshooter to paste images into `~/Screenshots/.incoming/`
  * With Compiz, you can set it by opening CompizConfig Settings Manager, enabling the Screenshot plugin, and setting the "Save Directory"
* The script `ss_monitor.sh` is the monitoring one, set it to automatically start when you log in your computer.
  * You probably have some GUI to set the startup applications, do it there.
* Take screenshots and feel the convenience!


## Licence

MIT.