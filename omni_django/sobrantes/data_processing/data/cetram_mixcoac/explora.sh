#!/bin/bash

for f in `ls *.kmz`; do
	echo '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
	unzip -o $f
	echo '###################################################################'
	echo '' >> Capa\ sin\ nombre.kml
	cat Capa\ sin\ nombre.kml
done
