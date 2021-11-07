#!/bin/bash

l=script.steam.launcher:
if [ -z "$*" ]; then
  echo $l "No arguments provided, see script file for details."
  exit
fi

echo "trying to run $1"

$1 %u & disown

curl -X POST -H 'Content-Type: application/json' -i http://localhost:8080/jsonrpc --data '{"jsonrpc":"2.0","id":1,"method":"Application.Quit"}'
