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


# Abrir un kml: NO JALA
#library(rgdal)
#walker <- readOGR(dsn='data/cetram_mixcoac/Capa sin nombre.kml', layer='Capa sin nombre', verbose=T, )


#library(RgoogleMaps)
#center = c(mean(df_ruta$lat), mean(df_ruta$lng))
#zoom: 1 = furthest out (entire globe), larger numbers = closer in
#errmap <- GetMap(center=center, zoom=5, maptype= "terrain", destfile = "plots/mapa_ruta.png") 
#lots of visual options, just like google maps: maptype = c("roadmap", "mobile", "satellite", "terrain", "hybrid", "mapmaker-roadmap", "mapmaker-hybrid")
