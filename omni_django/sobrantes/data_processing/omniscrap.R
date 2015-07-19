library(rvest)

base <- html("http://viadf.com.mx/Directorio/Microbus")

#guardo el indice de las rutas a scrapear
rutas<-base %>%  
  html_nodes("td+ td a") %>%
  html_attr("href")

#genero una lista con los nombres de los archivos de las rutas
nombres<-sub('/Directorio/Microbus/', '', rutas)
z<-1
for(k in nombres){
nombres[z]<- paste0(k,".txt")
z<-z+1
}


#guardo en un archivo de texto la informacion de cada una de las rutas de la lista que defini previamente
j<-1
for (i in rutas){
  b <- paste0("http://viadf.com.mx/",i) %>%  html %>%  html_nodes(xpath = "/html/body/script[2]/text()") %>% html_text()
  write(b,file=nombres[j])
  j<-j+1
}


b<-rutas[1] %>%  html %>%  html_nodes(xpath = "/html/body/script[2]/text()") %>% html_text()

