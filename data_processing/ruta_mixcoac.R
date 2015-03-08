#! /usr/bin/Rscript

library(dplyr)
library(ggplot2)
library(reshape2)
library(maptools)
library(googleVis)
library(rjson)

source('funciones_mapas.R')

dir.create('plots')

dir.create('out')

procesa_cetram('../hackdf_data/meteorolocurlcetrammixcoacrutas.csv')