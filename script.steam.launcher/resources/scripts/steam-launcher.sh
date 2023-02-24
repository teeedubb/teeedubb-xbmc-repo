#!/bin/bash
#Kodi Steam Launcher bash script by teeedubb
#See: https://github.com/teeedubb/teeedubb-xbmc-repo http://forum.xbmc.org/showthread.php?tid=157499
#
#Manual script usage: 
#steam-launcher.exe "/path/to/steam.exe" "/path/to/kodi" "0/1" "true/false" "prescriptpath/false" "postscriptpath/false" "steam parameters" "0" "true/false"
#$1 Full path to Steam
#$2 Full path to Kodi
#$3 Quit or minimise Kodi - 0 to quit, 1 to minimise
#$4 Run Kodi in portable mode - true or false
#$5 Pre Steam script - false for none or full path to script
#$6 Post Steam script - false for none or full path to script
#$7 Additional command line parameters to pass to Steam (see https://developer.valvesoftware.com/wiki/Command_Line_Options)
#$8 Force kill Kodi and how long to wait for before terminating in seconds. 0 to disable
#$9 Run Steam desktop mode - true or false
#
#Change the 'steam.launcher.script.revision =' number below to 999 to preserve changes through addon updates, otherwise it will be overwritten if the script is updated.
#
#steam.launcher.script.revision=018

l=script.steam.launcher: 
if [ -z "$*" ]; then
        echo $l "No arguments provided, see script file for details."
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
KODI_BIN=$(ps aux | grep -E 'kodi.bin|kodi-x11|kodi-wayland|kodi-gbm' | grep -v 'grep.*kodi' | head -n1 | awk '{print $11}' | sed 's:.*/::')
echo $l kodi executable is $KODI_BIN
#pre script
if [[ $5 != false ]] ; then
  "$5"
fi

#for use in steamos
if [[ $(uname -a | grep "steamos") ]] ; then
    if [[ $3 = 0 ]] ; then
        killall $KODI_BIN
        if [[ $8 != 0 ]] ; then
            (sleep $8 ; if [[ $(pidof $KODI_BIN) ]] ; then killall -9 $KODI_BIN ; fi)&
        fi
    fi
    /usr/bin/returntosteam.sh
    exit
fi

#check if steam is running and launch or focus steam
if [[ $(pidof steam) ]] ; then
    if [[ $(wmctrl -lpx | grep 'steamwebhelper.steamwebhelper.*Steam Big Picture Mode' | head -n1) ]] ; then
        echo $l steam bpm is already open - focusing
        wmctrl -i -a $(wmctrl -lpx | grep 'steamwebhelper.steamwebhelper.*Steam Big Picture Mode' | head -n1 | awk '{print $1}') &
    elif [[ $9 = true ]] ; then
        echo $l steam is already running - focusing desktop mode
        wmctrl -i -a $(wmctrl -lpx | grep '0 0.*Steam.Steam.*N/A N/A' | head -n1 | awk '{print $1}')
        wmctrl -i -r $(wmctrl -lpx | grep '0 0.*Steam.Steam.*N/A N/A' | head -n1 | awk '{print $1}') -b add,fullscreen &
    else
        echo $l steam is running - switching to bpm
        "$1" "$7" steam://open/bigpicture &
    fi
else
    if [[ $9 = true ]] ; then
        echo $l steam not running - launching desktop mode
        "$1" "$7" &
    else
        echo $l $l steam not running - launching steam bpm
        "$1" "$7" -gamepadui &
    fi
fi

#wait for steam to open
if [[ $9 = true ]] ; then
    until [[ $(wmctrl -lpx | grep '0 0.*Steam.Steam.*N/A N/A') ]] ; do
        echo $l steam window not deteced - looping
        sleep 0.5
    done
else
    until [[ $(wmctrl -lpx | grep 'steamwebhelper.steamwebhelper.*Steam Big Picture Mode') ]] ; do
        echo $l steam bpm window not deteced - looping
        sleep 0.5
    done
fi

#close/minimise kodi
if [[ $(pidof $KODI_BIN) ]] ; then
    if [[ $3 = 0 ]] ; then
        echo $l killing kodi
        killall $KODI_BIN
        if [[ $8 != 0 ]] ; then
            (echo $l forcefully killing kodi after "$8"s ; sleep $8 ; if [[ $(pidof $KODI_BIN) ]] ; then killall -9 $KODI_BIN ; fi)&
        fi
    elif [[ $3 = 1 ]] ; then
        echo $l minimising kodi
        #dont work with kodi + steam
        #wmctrl -i -r $(wmctrl -lp | grep '0 0.*Kodi$' | awk '{print $1}') -b remove,fullscreen
        #wmctrl -i -r $(wmctrl -lp | grep '0 0.*Kodi$' | awk '{print $1}') -b add,shaded
        #wmctrl -i -r $(wmctrl -lp | grep '0 0.*Kodi$' | awk '{print $1}') -b add,below
        xdotool windowminimize $(wmctrl -lpx | grep '0 0.*Kodi.Kodi.*Kodi' | head -n1 | awk '{print $1}')
    else
        echo $l not minimising or killing kodi
  fi
fi

#wait for steam to close
if [[ $9 = true ]] ; then
    while [[ $(pidof steam) ]] ; do
        echo $l steam extecutable deteced - looping
        sleep 0.5
    done
else
    while [[ $(wmctrl -lpx | grep 'steamwebhelper.steamwebhelper.*Steam Big Picture Mode') ]] ; do
        echo $l steam bpm windown detected - looping
        sleep 0.5
    done
fi
echo $l steam not detected any more - restarting kodi

#restarting/maximising kodi
(
    flock -x -n 500 || exit
    if [[ $6 != false ]] ; then
        "$6"
    fi
    if [[ $(pidof $KODI_BIN) ]] ; then
        echo $l kodi running - focusing
        wmctrl -i -a $(wmctrl -lpx | grep '0 0.*Kodi.Kodi.*Kodi' | head -n1 | awk '{print $1}')
        if [[ $3 = 1 ]] ; then
            echo $l fullscreening kodi
            wmctrl -i -r $(wmctrl -lpx | grep '0 0.*Kodi.Kodi.*Kodi' | head -n1 | awk '{print $1}') -b add,fullscreen &
        fi
    else
        if [[ $4 = true ]] ; then
            echo $l staring kodi in portable mode
            "$2" -p &
        else
            echo $l staring kodi
            "$2" &
        fi
    fi
  flock -u 500
) 500>/tmp/.steam-launcher.exclusivelock

#####################################
        ;;
    *)
        echo $l "I don't support this OS!"
        exit 1
        ;;
esac

#methods i have tried to detect between bpm minimised and hidden (eg when running a game)
#xwininfo -all -id $(wmctrl -lp | grep $(ps aux | grep -i 'ubuntu12_32/steam '| grep -v 'grep.*steam' | head -n1 | awk '{print $2}')| awk '{print $1}')
#xprop -id $(wmctrl -lp | grep $(ps aux | grep -i 'ubuntu12_32/steam '| grep -v 'grep.*steam' | head -n1 | awk '{print $2}')| awk '{print $1}')
#wmctrl -lpxG | grep $(ps aux | grep -i 'ubuntu12_32/steam '| grep -v 'grep.*steam' | head -n1 | awk '{print $2}')
