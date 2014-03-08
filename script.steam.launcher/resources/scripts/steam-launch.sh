#!/bin/bash
#Script to launch Steam BPM from Xbmc, by teeedubb
#steam.launcher.script.revision=003

export DISPLAY=:0

case "$(uname -s)" in
    Darwin)

open "$1" steam://open/bigpicture

for i in {1..6} ; do
    if [[ $(ps -A | grep steam.sh | grep -v Helper | grep -v grep | awk '{print $1}') ]]; then
        if [[ $(ps -A | grep XBMC.app | grep -v Helper | grep -v grep | awk '{print $1}') ]] ; then
          if [[ $3 = 0 ]]; then
            killall -9 XBMC
          fi
        fi
    fi
    sleep 1
done

if [[ $3 = 0 ]]; then
   if [[ $(ps -A | grep XBMC.app | grep -v Helper | grep -v grep | awk '{print $1}') ]] ; then
	killall -9 XBMC
   fi
fi

echo loop
while [[ $(ps -A | grep steam.sh | grep -v Helper | grep -v grep | awk '{print $1}') ]]; do
     sleep 1
done

open "$2"

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

for i in {1..6} ; do
    if [[ $(wmctrl -l | grep "Steam$") ]]; then
	if [[ $(pidof xbmc.bin) ]] ; then
	  if [[ $3 = 0 ]]; then
	    kill -9 $(pidof xbmc.bin)
	  else
	    wmctrl -r "XBMC Media Center" -b remove,fullscreen
	  fi
	fi
    fi
    sleep 1
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
	sleep 1
done

if [[ -f /tmp/xbmc-steam-launcher.running ]]; then
  exit
fi
touch /tmp/xbmc-steam-launcher.running

if [[ $(pidof xbmc.bin) ]] ; then
    wmctrl -a "XBMC Media Center"
    if [[ $3 != 0 ]]; then
      wmctrl -r "XBMC Media Center" -b add,fullscreen
    fi
else
  "$2" &
fi

rm -rf /tmp/xbmc-steam-launcher.running

        ;;    
    *)
        echo "I don't support this OS!"
        exit 1
        ;;
esac