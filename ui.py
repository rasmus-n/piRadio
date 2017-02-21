#! /usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from os import system

import tm1637

#CLK -> GPIO23 (Pin 16)
#Di0 -> GPIO24 (Pin 18)

CLK = 22
SW = 23
DT = 27

n = 1
t = 0
t2 = 0

def cb(pin):
  print pin

def select(pin):
  global n
  global t

  d = GPIO.input(DT)

  if t > 0:
    if d == 1:
      n += 1
    elif d == 0:
      n -= 1

  t = 10

  if n < 1:
    n = 10
  if n > 10:
    n = 1

  Display.Show([0x7f, 0x7f, int(n/10), n%10])
  Display.Point([0,0,0,0])

def play(pin):
  t2 = 1
  if (t>0):
    Display.Show([8, 8, 8, 8])
    Display.Point([1,1,1,1])
    system("/home/rn/tune.py " + str(n))
  else:
    Display.Show([0x7f, 0x7f, 0x7f, 0x7f])
    Display.Point([0,0,0,0])
    system("mpc toggle")

GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW,  GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT,  GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(SW,  GPIO.FALLING, callback=play, bouncetime=500)
GPIO.add_event_detect(CLK, GPIO.FALLING, callback=select, bouncetime=50)
#GPIO.add_event_detect(DT,  GPIO.FALLING, callback=select, bouncetime=500)

Display = tm1637.TM1637(8,7,tm1637.BRIGHT_TYPICAL)

#Display.Clear()
Display.SetBrightnes(1)

p = [1,0,1,0]

while True:
  if (t > 0) or (t2 > 0):
    t -= 1
    t2 -= 1
  else:
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    currenttime = [ int(hour / 10), hour % 10, int(minute / 10), minute % 10 ]

    Display.Show(currenttime)
    Display.Point(p)
    p.insert(0, p.pop())

  sleep(1)
