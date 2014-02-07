#!/bin/bash
#Script to launch Steam BPM from Xbmc, by teeedubb
#steam.launcher.script.revision=001

export DISPLAY=:0

case "$(uname -s)" in
    Darwin)
        XBMC_PID=$(ps -A | grep XBMC.app | grep -v Helper | grep -v grep | awk '{print $1}')
        XBMC_BIN=$(ps -A | grep XBMC.app | grep -v Helper | grep -v grep | awk '{print $5}')
        STEAM_PID=$(ps -A | grep STEAM.app | grep -v Helper | grep -v grep | awk '{print $1}')
        STEAM_BIN=$(ps -A | grep STEAM.app | grep -v Helper | grep -v grep | awk '{print $5}')
        # Is Steam running?
	if [[ $STEAM_PID ]]; then
	  $STEAM_BIN steam://open/bigpicture #steam is brought to focus better this way
	  echo "Steam already running"
	else
	   $STEAM_BIN -bigpicture #steam opens better like this if not already open
	    echo "Steam not running, launching"
	fi
	# Wait for Steam to exit
	while [ $(ps -A | grep STEAM.app | grep -v Helper | grep -v grep | awk '{print $1}') ]; do #STEAM_PID variable doesnt work here, needs work
	  echo "Steam running"
	  sleep 1
	done
	#Restart XBMC
	$XBMC_BIN &
        ;;
    Linux)

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
	  if [[ $3 = 0 ]]; then
	    kill -9 $(pidof xbmc.bin)
	  else
	    wmctrl -r "XBMC Media Center" -b remove,fullscreen
	  fi
	fi
    fi
    sleep 0.1
done

if [[ $(pidof xbmc.bin) ]]; then
	  if [[ $3 = 0 ]]; then
	    kill -9 $(pidof xbmc.bin)
	  else
	    wmctrl -r "XBMC Media Center" -b remove,fullscreen
	  fi
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
    if [[ $3 != 0 ]]; then
      wmctrl -r "XBMC Media Center" -b add,fullscreen
    fi
else
    "$2" &
fi

        ;;    
    *)
        echo "I don't support this OS!"
        exit 1
        ;;
esac