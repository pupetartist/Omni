#!/usr/bin/env python
import re
import sys
import numpy
import string
entrada=open(sys.argv[1])
test=entrada.read().split('\n')
wwn=''
for linea in test:
    if linea[0].isdigit():
        wwn=linea 
    else: IG=linea.rstrip()
    print "%s|%s"%(IG, wwn)  