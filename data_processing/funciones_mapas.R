#! /usr/bin/Rscript

library(dplyr)
library(ggplot2)
library(reshape2)
library(maptools)
library(googleVis)
library(rjson)
library(uuid)

# Transoroma un objeto kml de la CETRAM en un data frame con las coordenadas
transform_df <- function(kml_obj) {  
  df_start <- data.frame(kml_obj[[1]], pointName='Inicio') 
  df_route <- data.frame(kml_obj[[2]], pointName='Estacion')
  df_end <- data.frame(kml_obj[[3]], pointName='Fin')
  col_labels <- c('lng', 'lat', 'elevation', 'pointName')
  colnames(df_start) <- col_labels
  colnames(df_route) <- col_labels
  colnames(df_end) <- col_labels
  df_route$pointName <- paste(df_route$pointName, rownames(df_route), sep=' ')
  df_ret <- rbind(df_start, df_route, df_end)
  df_ret <- df_ret %>% mutate(latlng=paste(lat, lng, sep=":"))
  df_ret$uuid = replicate(nrow(df_ret), UUIDgenerate())
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

empresa_provider = list(
  "Red de Transporte de Pasajeros del Distrito Federal."='RTP',
  "Sistema de Transportes Eléctricos"='STE',
  "Unión de Taxistas de Reforma y Ramales Ruta 2 A.C."='Microbus',
  "Unión de Taxistas de la Ruta 15 Poniente y Ramales A. C."='Microbus',
  "Unión de Taxistas de la Ruta 57 Aguilas, Puerta Grande, Mixcoac, Metro Tacubaya y Ramales."='Microbus',
  "Transportes Unidos del Sur S. A. de C. V. Ruta 117"='Microbus',
  "Autotransportes Urbanos Siglo Nuevo, S.A. de C.V. 112"='Microbus',
  "Unión de Choferes Taxistas de Transportación Colectiva A.C. Ruta 1"='Microbus',  
  "Unión de Permisionarios de Transporte de la Ruta 25."='Microbus'
)

empresa_ruta = list(
  "Red de Transporte de Pasajeros del Distrito Federal."='Desconocido',
  "Sistema de Transportes Eléctricos"='Desconocido',
  "Unión de Taxistas de Reforma y Ramales Ruta 2 A.C."='Ruta 2',
  "Unión de Taxistas de la Ruta 15 Poniente y Ramales A. C."='Ruta 15',
  "Unión de Taxistas de la Ruta 57 Aguilas, Puerta Grande, Mixcoac, Metro Tacubaya y Ramales."='Ruta 57',
  "Transportes Unidos del Sur S. A. de C. V. Ruta 117"='Ruta 117',
  "Autotransportes Urbanos Siglo Nuevo, S.A. de C.V. 112"='Ruta 112',
  "Unión de Choferes Taxistas de Transportación Colectiva A.C. Ruta 1"='Ruta 1',  
  "Unión de Permisionarios de Transporte de la Ruta 25."='Ruta'

)

recategoriza <- function(x, catList, default.cat) {
  #default.cat = "Otro"
  comp = as.character(x)
  #browser('ja!')
  idx = which(comp==names(catList))
  if(length(idx)==0)
    return(default.cat)
  return(catList[[idx]])
}



process_node <- function(row_list, cetram_info, route_info, num_routes=1) {
  json_node = list()
  json_node$id = row_list$uuid
  json_node$type = 'node'
  if(num_routes==1)
    json_node$name = sprintf('%s %s', route_info$name, row_list$pointName)
  else if(num_routes>1)
    json_node$name = sprintf('%s %s %s', cetram_info$provider, 'CONEXION', row_list$pointName)
  else
    json_node$name = sprintf('%s %s', cetram_info$provider, row_list$pointName)
  json_node$transport_type = 'bus'
  json_node$transport_provider = cetram_info$provider
  json_node$geolocation = c(row_list$lat, row_list$lng)
  return(json_node)
}


process_route <- function(cetram_info) {
  json_route = list()
  json_route$transport_provider = cetram_info$provider 
  if(cetram_info$route=='Desconocido') {
    json_route$name = sprintf('%s %s', cetram_info$provider, cetram_info$DERROTERO.1)
  } else {
    json_route$name = sprintf('%s %s %s', cetram_info$provider, cetram_info$route, cetram_info$DERROTERO.1)
  }
  json_route$type = 'route'
  json_route$id = UUIDgenerate()
  return(json_route)
}


procesa_cetram <- function(csv_file) {
  cetram_table <- read.csv(csv_file, sep=';', header=T, stringsAsFactors=F)
  cetram_table$provider = sapply(cetram_table$EMPRESA, recategoriza, catList=empresa_provider, default.cat='Desconocido')
  cetram_table$route = sapply(cetram_table$EMPRESA, recategoriza, catList=empresa_ruta, default.cat='Desconocido')
  cetram_list = split(cetram_table, 1:nrow(cetram_table))

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
        df_ruta_list = split(df_ruta, 1:nrow(df_ruta))
        html_map = create_html_map(df_ruta, 'latlng', 'pointName', sprintf('plots/%s_%s.html', cetram_table[i, 'DERROTERO.1'], f_kmz))
        
        route_json = process_route(cetram_list[[i]])
        node_json_list = lapply(df_ruta_list, process_node, cetram_info=cetram_list[[i]], route_info=route_json)
        route_json$components = unname(sapply(node_json_list, FUN=function(x) x$id))
        num_nodes = length(node_json_list) 
        if(num_nodes>1) {
          for(idx in seq(node_json_list)) {
            if(idx==1) {
              node_json_list[[idx]]$connections = list(node_id_foward=node_json_list[[idx + 1]]$id)
              #if(node_json_list[[idx]]$name=='Inicio')
              route_json$start_node_id = node_json_list[[idx]]$id 
            }
            else if(idx==num_nodes) {
              node_json_list[[idx]]$connections = list(node_id_backward=node_json_list[[idx - 1]]$id)
              #if(node_json_list[[idx]]$name=='Fin')
              route_json$finish_node_id = node_json_list[[idx]]$id
            }
            else
              node_json_list[[idx]]$connections = list(node_id_foward=node_json_list[[idx + 1]]$id, node_id_backward=node_json_list[[idx - 1]]$id)
            node_json_list[[idx]]$routes = route_json$id
          }
        }
        write2file(toJSON(unname(node_json_list)), sprintf('out/nodes_%s.json', route_json$name))
        write2file(toJSON(route_json), sprintf('out/route_%s.json', route_json$name))
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

write2file <- function(str, filename) {
  fileConn <- file(filename)
  writeLines(str, fileConn)
  close(fileConn)
}

# Abrir un kml: NO JALA
#library(rgdal)
#walker <- readOGR(dsn='Capa sin nombre.kml', layer='Capa sin nombre', verbose=T, )


#library(RgoogleMaps)
#center = c(mean(df_ruta$lat), mean(df_ruta$lng))
#zoom: 1 = furthest out (entire globe), larger numbers = closer in
#errmap <- GetMap(center=center, zoom=5, maptype= "terrain", destfile = "plots/mapa_ruta.png") 
#lots of visual options, just like google maps: maptype = c("roadmap", "mobile", "satellite", "terrain", "hybrid", "mapmaker-roadmap", "mapmaker-hybrid")
