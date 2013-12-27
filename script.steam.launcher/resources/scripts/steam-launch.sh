#!/bin/bash
#Script to launch Steam BPM from Xbmc, by teeedubb
DISPLAY=:0

echo Kill XBMC
	kill -9 $(pidof xbmc.bin) #There are better ways of doing this but this is the most consistent
	echo "Shutdown XBMC" 
	
echo Is Steam running?
if [ $(pidof steam) ]
then
    if [[ $(wmctrl -l | grep "Steam$") ]]; then
      echo "Looks like Steam BPM is already running, giving focus"
      wmctrl -i -a $(wmctrl -l | grep "Steam$" | cut -c1-10)
    else
      "$1" steam://open/bigpicture & #steam is brought to focus better this way
      echo "Steam DM already running, switching to Steam BPM"
    fi
else
      "$1" -bigpicture & #steam opens better like this if not already open
      echo "Steam not running, launching"
fi


until [[ $(wmctrl -l | tail -n1 | grep "Steam$") ]]; do
	echo "Waiting for Steam BPM to start..."
	sleep 1
done

STEAM_WIN_ID=$(wmctrl -l | grep "Steam$" | cut -c1-10)

while [[ $(wmctrl -l | grep "$STEAM_WIN_ID") ]]; do
	echo "Steam BPM running!"
	sleep 1
done

if [ $(pidof xbmc.bin) ] ; then
    echo "XBMC already running, giving focus"
    wmctrl -a "XBMC Media Center"
    echo "Exiting script" 
    exit
else
    "$2" &
fi