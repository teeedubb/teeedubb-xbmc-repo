#!/bin/bash
#Script to launch Steam BPM from Xbmc, by teeedubb
#See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.xbmc.org/showthread.php?tid=157499
#Manual script usage: steam-launch.sh "/path/to/steam" "/path/to/xbmc" "0/1"
#0 = Quit Steam. 1 = Minimize xbmc while steam is running.
#Edit this script to launch external programs before Steam or XBMC. See the two marked locations below (First two are for MAC, Bottom two are for Linux).
#Change the 'steam.launcher.script.revision=' number below to 999 to preserve changes through addon updates, otherwise it shall be overwritten.

#steam.launcher.script.revision=004

export DISPLAY=:0

case "$(uname -s)" in
    Darwin)

#MAC ONLY#############################
#Steam starts here, insert code below:
######################################

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

#MAC ONLY##############################
#XBMC restarts here, insert code below:
#######################################


open "$2"

        ;;
    Linux)

#LINUX ONLY###########################	
#Steam starts here, insert code below:
######################################

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

#LINUX ONLY############################	
#XBMC restarts here, insert code below:
#######################################

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