library(slidify)
library(slidifyLibraries)
library(pander)
library(xtable)

setwd()<-"C:/Users/Brian/Documents/mydeck/"
X<-read.csv("C:/Users/Brian/Documents/mydeck/results.csv",h=T,sep=",")
colnames(X)<-c("Rank","Player","TOTAL","Play-in (4 pts) ","64 Teams (2 pts)","32 Teams (4 pts)"," Sweet 16 (8pts)","Elite 8 (16 pts)"," 'Final 4 (32 Pts)"," National Champion (64 pts)","Wins"," Loses","Winning %")
slidify("C:/Users/Brian/Documents/mydeck/index.Rmd")

