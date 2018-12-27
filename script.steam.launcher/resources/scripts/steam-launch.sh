#!/bin/bash
#Script to launch Steam BPM from Kodi, by teeedubb
#See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.kodi.tv/showthread.php?tid=157499
#Manual script usage: SteamLauncher-AHK.exe "e:\path\to\steam.exe" "d:\path\to\kodi.exe" "0/1" "true/false" "scriptpath/false" "scriptpath/false" "steam parameters"
#$3 = 0 Quit KODI, 1 Minimize KODI. $4 = KODI portable mode. $5 = pre script. $6 post script. $7 steam parameters.
#Change the 'steam.launcher.script.revision =' number to 999 to preserve changes through addon updates, otherwise it shall be overwritten.
#steam.launcher.script.revision=016


if [ -z "$*" ]; then
        echo "No arguments provided, see script file for details."
        exit
fi

case "$(uname -s)" in
    Darwin)
#
export DISPLAY=:0

if [[ $5 != false ]] ; then
  "$5"
fi

open "$1" "$7" steam://open/bigpicture

for i in {1..6} ; do
  if [[ $(ps -A | grep steam.sh | grep -v Helper | grep -v grep | awk '{print $1}') ]] ; then
    if [[ $(ps -A | grep Kodi.app | grep -v Helper | grep -v grep | awk '{print $1}') ]] ; then
      if [[ $3 = 0 ]] ; then
	killall Kodi
	(sleep 5 ; if [[ $(ps -A | grep Kodi.app | grep -v Helper | grep -v grep | awk '{print $1}') ]] ; then killall -9 Kodi ; fi)&
      fi
    fi
  else
    sleep 1
  fi
done

if [[ $3 = 0 ]] ; then
  if [[ $(ps -A | grep Kodi.app | grep -v Helper | grep -v grep | awk '{print $1}') ]] ; then
    killall Kodi
    (sleep 5 ; if [[ $(ps -A | grep Kodi.app | grep -v Helper | grep -v grep | awk '{print $1}') ]] ; then killall -9 Kodi ; fi)&
  fi
fi

while [[ $(ps -A | grep steam_osx | grep -v grep | awk '{print $1}') ]] ; do
  sleep 1
done

if [[ $6 != false ]] ; then
  "$6"
fi

if [[ $4 = true ]] ; then
  open "$2" --args -p
else
  open "$2"
fi
#########################################
        ;;
    Linux)
#
DP=$(w -hs | awk '{print $3}') && export DISPLAY=$DP
KODI_BIN=$(ps aux |pgrep 'kodi.bin|kodi-x11|kodi-wayland|kodi-gbm')

if [[ $5 != false ]] ; then
  "$5"
fi

if [[ $(uname -a |grep "steamos") ]] ; then
  if [[ $3 = 0 ]] ; then
    kill $KODI_BIN
    (sleep 5 ; if [[ $KODI_BIN ]] ; then kill -9 $KODI_BIN ; fi)&
  fi
  /usr/bin/returntosteam.sh
  exit
fi

if [[ $(pidof steam) ]] ; then
  if [[ $(wmctrl -l | grep "Steam$") ]] ; then
    wmctrl -i -a $(wmctrl -l | grep "Steam$" | awk '{print $1}') &
  else
    "$1" "$7" steam://open/bigpicture &
  fi
else
  "$1" "$7" -bigpicture &
fi

for i in {1..6} ; do
  if [[ $(wmctrl -l | grep "Steam$") ]] ; then
    if [[ $KODI_BIN ]] ; then
      if [[ $3 = 0 ]] ; then
	kill $KODI_BIN
	(sleep 5 ; if [[ $KODI_BIN ]] ; then kill -9 $KODI_BIN ; fi)&
      else
	wmctrl -i -r $(wmctrl -l | grep  "Kodi"$ | awk '{print $1}') -b remove,fullscreen
      fi
    fi
  else
    sleep 1
  fi
done

if [[ $KODI_BIN ]] ; then
  if [[ $3 = 0 ]] ; then
    kill $KODI_BIN
    (sleep 5 ; if [[ $KODI_BIN ]] ; then kill -9 $KODI_BIN ; fi)&
  else
    wmctrl -i -r $(wmctrl -l | grep  "Kodi"$ | awk '{print $1}') -b remove,fullscreen
  fi
fi

until [[ $(wmctrl -l | grep "Steam$") ]] ; do
  echo "Waiting for Steam BPM to start..."
  sleep 1
done

sleep 1

STEAM_WIN_ID=$(wmctrl -l | grep "Steam$" | awk '{print $1}')

while [[ $(wmctrl -l | grep "$STEAM_WIN_ID") ]] ; do
  sleep 0.5
done

(
  flock -x -n 200 || exit
  if [[ $6 != false ]] ; then
    "$6"
  fi
  if [[ $3 != 0 ]] ; then
echo "3 equal not zero"
  if [[ $KODI_BIN ]] ; then
    wmctrl -i -a $(wmctrl -l | grep  "Kodi"$ | awk '{print $1}')
    if [[ $3 != 0 ]] ; then
echo "2nd 3 equal not zero"
      wmctrl -i -r $(wmctrl -l | grep  "Kodi"$ | awk '{print $1}') -b add,fullscreen &
    fi
  fi
  else
    if [[ $4 = true ]] ; then
      "$2" -p &
    else
      "$2" &
    fi
  fi


  flock -u 200
) 200>/tmp/.steam-launcher.exclusivelock

#####################################
        ;;
    *)
        echo "I don't support this OS!"
        exit 1
        ;;
esac
