#!/bin/bash

HOST="localhost"
PORT="9999"

# if curl -v --connect-timeout 2 telnet://"$HOST":"$PORT" 2>&1 | grep -q "Connected"; then

for i in $(seq 1 60); do
  if nc -zv -w 1 $HOST $PORT >/dev/null 2>&1; then
    echo "Port $PORT on $HOST is OPEN."
  else
    echo "Port $PORT on $HOST is CLOSED."
  fi
  sleep 1
done

