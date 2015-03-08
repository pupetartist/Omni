#! /usr/bin/Rscript

library(dplyr)
library(ggplot2)
library(reshape2)
library(maptools)
library(googleVis)
library(rjson)


# Transoroma un objeto kml de la CETRAM en un data frame con las coordenadas
transform_df <- function(kml_obj) {  
  df_start <- data.frame(kml_obj[[1]], pointName='Inicio') 
  df_route <- data.frame(kml_obj[[2]], pointName='Ruta')
  df_end <- data.frame(kml_obj[[3]], pointName='Fin')
  col_labels <- c('lng', 'lat', 'elevation', 'pointName')
  colnames(df_start) <- col_labels
  colnames(df_route) <- col_labels
  colnames(df_end) <- col_labels
  df_route$pointName <- paste(df_route$pointName, rownames(df_route), sep='')
  df_ret <- rbind(df_start, df_route, df_end)
  
  df_ret <- df_ret %>% mutate(latlng=paste(lat, lng, sep=":"))
  return(data.frame(df_ret))
}

# Crea un mapa de google maps con las coordenadas
create_html_map <- function(df_data, location_var, tip_var, out_file) {
  htmlmap <- gvisMap(data=df_data, locationvar=location_var, tipvar=tip_var, 
                     options = list(showTip = TRUE, 
                                    showLine = TRUE,
                                    lineColor = '#800000',
                                    lineWidth = 20,
                                    enableScrollWheel = TRUE, 
                                    mapType = "roadmap", 
                                    useMapTypeControl = TRUE),
                     chartid='_id_mapa_rutas')
  
  sink(file=out_file)
  cat(
    "<!DOCTYPE html>
   <html>
    <head>
      <meta charset=\"UTF-8\">
      <title>Mapa Interactivo</title>
    </head>
    <body>\n")
  print(htmlmap, "chart")
  cat(
    " </body>
   </html>")
  sink() 
  return(htmlmap)
}

procesa_cetram <- function(csv_file) {
  cetram_table <- read.csv(csv_file, sep=';', header=T, stringsAsFactors=F)
  kmz_files <- dir(path='../hackdf_data/', pattern='*.kmz')
  for(i in seq(nrow(cetram_table))) {
    f_kmz_u = cetram_table[i, 'Ruta']
    f_kmz = tolower(f_kmz_u)
    cat('Filename:', f_kmz, ', Route:', cetram_table[i, 'DERROTERO.1'], '\n')
    
    kmz_matched = kmz_files[ grepl(f_kmz, kmz_files) ]
    if(length(kmz_matched)==1) {
      kmz_path = sprintf('../hackdf_data/%s', kmz_matched)  
      if(file.exists(kmz_path)) {
        unzip(kmz_path)
        # Para que no salga el warning de incomplete file
        write('\n', file='Capa sin nombre.kml', append=TRUE)
        # salen 3 conjuntos de cordenadas: inicio, puntos de ruta, final
        kml_obj = getKMLcoordinates(kmlfile = 'Capa sin nombre.kml')
        df_ruta = transform_df(kml_obj)
        html_map = create_html_map(df_ruta, 'latlng', 'pointName', sprintf('plots/%s_%s.html', cetram_table[i, 'DERROTERO.1'], f_kmz))
        obj_out = list()
        obj_out$route_data = unlist(cetram_table[i, ]) 
        obj_out$points = unname(  split(df_ruta[ , c('latlng', 'pointName')], seq(nrow(df_ruta))) )
        #cat(toJSON(obj_out), '\n')
        cat('OK\n')
      }
      else {
        cat('KMZ file not found', kmz_path, cetram_table[i, 'DERROTERO.1'], '\n')
      }
    }
    else {
      if(length(kmz_matched)==0) {
        cat('NO KMZ files matched for', f_kmz, '\n')
      }
      else {
        cat('Multiple KMZ files matched for', f_kmz, '\n')
        print(kmz_matched)
      }
    }
  }
}

# Abrir un kml: NO JALA
#library(rgdal)
#walker <- readOGR(dsn='Capa sin nombre.kml', layer='Capa sin nombre', verbose=T, )


#library(RgoogleMaps)
#center = c(mean(df_ruta$lat), mean(df_ruta$lng))
#zoom: 1 = furthest out (entire globe), larger numbers = closer in
#errmap <- GetMap(center=center, zoom=5, maptype= "terrain", destfile = "plots/mapa_ruta.png") 
#lots of visual options, just like google maps: maptype = c("roadmap", "mobile", "satellite", "terrain", "hybrid", "mapmaker-roadmap", "mapmaker-hybrid")
