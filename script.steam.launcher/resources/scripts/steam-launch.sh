#!/bin/bash
#Script to launch Steam BPM from Xbmc, by teeedubb
export DISPLAY=:0

if [[ $(pidof steam) ]]; then
    if [[ $(wmctrl -l | grep "Steam$") ]]; then
      wmctrl -i -a $(wmctrl -l | grep "Steam$" | cut -c1-10) &
    else
      "$1" steam://open/bigpicture &
    fi
else
      "$1" -bigpicture &
fi

for i in {1..30} ; do
    if [[ $(wmctrl -l | grep "Steam$") ]]; then
	if [[ $(pidof xbmc.bin) ]] ; then
	  kill -9 $(pidof xbmc.bin)
	fi
    fi
    sleep 0.1
done

if [[ $(pidof xbmc.bin) ]]; then
	kill -9 $(pidof xbmc.bin)
fi

until [[ $(wmctrl -l | tail -n1 | grep "Steam$") ]]; do
	echo "Waiting for Steam BPM to start..."
	sleep 1
done

sleep 3

STEAM_WIN_ID=$(wmctrl -l | grep "Steam$" | cut -c1-10)

while [[ $(wmctrl -l | grep "$STEAM_WIN_ID") ]]; do
	sleep 0.1
done

if [[ $(pidof xbmc.bin) ]] ; then
    wmctrl -a "XBMC Media Center"
else
    "$2" &
fi