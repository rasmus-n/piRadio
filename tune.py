#! /usr/bin/python

import urllib
import xml.etree.ElementTree as ET
from os import system

list_url = "https://docs.google.com/spreadsheets/d/1dCXBgD1Uk9x22yD8Scgne8FMQj1lgORfflnNiU7Eodk/pub?output=tsv"

def get_playlist(number):
  list_tsv = urllib.urlopen(list_url).read()

  for l in list_tsv.split("\n"):
    (n, name, typ, vol, url) = l.split("\t")
    url = url.strip()
    if n.isdigit() and int(n) == number:
      if typ.find("Podcast") > -1:
        (typ, l) = typ.split(":")
        url = get_podcasts(url, int(l)) 
      system("mpc clear; mpc volume " + str(vol) + "; mpc add \"" + url + "\"; mpc play")

def get_podcasts(url, number):
  xml_data=urllib.urlopen(url).read()
  root = ET.fromstring(xml_data)

  number = int(number)
  stream_list = []
  c=0
  for item in root.iter('item'):
    if (c < number):
      c += 1
      stream_list.append(item.find('enclosure').get('url'))
    else:
      break
  return " ".join(stream_list[::-1])


if __name__ == "__main__":
  from sys import argv
  
  if len(argv) == 2:
    n = argv[1]
    if n.isdigit():
      get_playlist(int(n))

