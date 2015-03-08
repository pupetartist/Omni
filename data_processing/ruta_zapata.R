#! /usr/bin/Rscript

library(dplyr)
library(ggplot2)
library(reshape2)
library(maptools)
library(googleVis)
library(rjson)

source('funciones_mapas.R')

dir.create('plots')

procesa_cetram('../hackdf_data/datos-de-trafico-en-puntos-especificos_cetramzapatarutas.csv')
