#! /bin/sh

if [ `mpc | grep -c playing` -ne 0 ]; then
  echo "1" > /sys/class/gpio/gpio17/value
else
  echo "0" > /sys/class/gpio/gpio17/value
fi
