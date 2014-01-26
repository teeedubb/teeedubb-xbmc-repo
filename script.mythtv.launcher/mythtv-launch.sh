#!/bin/bash
export DISPLAY=:0

if [ $(pidof openbox) ]; then
	kill -9 $(pidof xbmc.bin)
	mythfrontend &&
	xbmc &
else
	touch /tmp/mythtv.load && kill $(pidof xinit)
fi

