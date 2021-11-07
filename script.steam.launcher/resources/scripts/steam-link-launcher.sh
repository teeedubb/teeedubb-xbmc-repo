#!/bin/bash

#1 steamLink,
#2 kodiLinux,
#3 quitKodiSetting,
#4 preScript,
#5 postScript,

l=script.steam.launcher:
if [ -z "$*" ]; then
  echo $l "No arguments provided, see script file for details."
  exit
fi
