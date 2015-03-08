#!/usr/bin/env python
#cat *.txt | grep -E "var routeCoords|new google\.maps\.LatLng\(|rrrr" | sed -e 's/ //g' -e 's/varrouteCoords2\=\[/ida/' -e 's/varrouteCoords\=\[/vuelta/' -e 's/newgoogle\.maps\.LatLng(//' -e 's/),//'
# Python extraewwn.py limpia.txt | sed -e 's/rrrr//' -e 's/\.txt//'
import re
import sys
import numpy
import string
entrada=open(sys.argv[1])
test=entrada.read().split('\n')
wwn=''
IG=''
for linea in test:
    if linea[0].isdigit():
        wwn=linea 
    elif linea.startswith("rrrr"):
    	archivo=linea
    else: IG=linea.rstrip()
    print "%s|%s|%s"%(archivo,IG, wwn)  