#! /usr/bin/Rscript

library(dplyr)
library(ggplot2)
library(reshape2)
library(maptools)
library(googleVis)
library(rjson)

source('funciones_mapas.R')

dir.create('plots')

viadf = read.table('../other_data/nuevasrutas.psv', sep='|', header=F, stringsAsFactors=F)

colnames(viadf) <- c('ruta', 'sentido', 'latlng')
viadf$lat_lng <- sapply(strsplit(viadf$latlng, split = ','), FUN=function(x) paste(x, collapse=':'))
viadf <- viadf %>% filter(lat_lng!='')
viadf <- unique(viadf)
create_html_map(viadf, 'lat_lng', 'ruta', 'plots/nuevas_rutas.html')
