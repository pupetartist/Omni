#! /usr/bin/Rscript

library(dplyr)
library(ggplot2)
library(reshape2)
library(maptools)
library(googleVis)
library(rjson)

source('funciones_mapas.R')

dir.create('plots')

cetram_mixcoac <- read.csv('data/cetram_mixcoac/cetrammixcoacrutas.csv', sep=';', header=T, stringsAsFactors=F)

for(i in seq(nrow(cetram_mixcoac))) {
  f_kmz_u = cetram_mixcoac[i, 'Ruta']
  f_kmz = tolower(f_kmz_u)
  cat('Filename:', f_kmz, '\n')
  kmz_path = sprintf('data/cetram_mixcoac/%s', f_kmz) 
  if(file.exists(kmz_path)) {
    unzip(kmz_path)
    # Para que no salga el warning de incomplete file
    write('\n', file='Capa sin nombre.kml', append=TRUE)
    # salen 3 conjuntos de cordenadas: inicio, puntos de ruta, final
    kml_obj = getKMLcoordinates(kmlfile = 'Capa sin nombre.kml')
    df_ruta = transform_df(kml_obj)
    html_map = create_html_map(df_ruta, 'latlng', 'pointName', sprintf('plots/%s_%s.html', cetram_mixcoac[i, 'DERROTERO.1'], f_kmz))
    obj_out = list()
    obj_out$route_data = unlist(cetram_mixcoac[i, ]) 
    obj_out$points = unname(  split(df_ruta[ , c('latlng', 'pointName')], seq(nrow(df_ruta))) )
    cat(toJSON(obj_out), '\n')
  }
  else {
    cat('KMZ file not found', kmz_path, cetram_mixcoac[i, 'DERROTERO.1'], '\n')
  }
}
