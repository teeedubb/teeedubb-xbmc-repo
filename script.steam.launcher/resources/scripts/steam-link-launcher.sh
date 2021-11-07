#!/bin/bash

l=script.steam.launcher:
if [ -z "$*" ]; then
  echo $l "No arguments provided, see script file for details."
  exit
fi

echo "trying to run $1"

$1 %u
