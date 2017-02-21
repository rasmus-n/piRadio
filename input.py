#! /usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from os import system

SNOOZE = 27
SLEEP = 24

buttons = (SNOOZE, SLEEP)

GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttons, GPIO.IN, pull_up_down=GPIO.PUD_UP)

n = 0
d2 = ""

while True:
  try:
    c = GPIO.wait_for_edge(buttons, GPIO.FALLING, timeout=2000, bouncetime=200)
  except RuntimeError:
    sleep(0.5)
    print "hest"
    continue
  except KeyboardInterrupt:
#    GPIO.cleanup()
    exit(0)

  d1 = datetime.now().strftime("%H:%M")
  if c == None:
    if n > 0:
      print "Tune", n
      system("sudo -u rn -g rn /home/rn/tune " + str(n))
      n = 0
      d2 = ""

    else:
      if d1 != d2:
        print d1
        d2 = d1

  else:
    print c
    n += 1
    print n
