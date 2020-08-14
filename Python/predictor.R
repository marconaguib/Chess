options(warn=-1)
suppressMessages(library(randomForest))
suppressMessages(library(data.table))

rm(list=ls(all=TRUE))

startall <- Sys.time()
st1 <- Sys.time()
model <- readRDS("C:/Users/Nicolas\ Martin/chess/models/model0.rds")
end1 <- Sys.time()
df=fread("a8,b8,c8,d8,e8,f8,g8,h8,a7,b7,c7,d7,e7,f7,g7,h7,a6,b6,c6,d6,e6,f6,g6,h6,a5,b5,c5,d5,e5,f5,g5,h5,a4,b4,c4,d4,e4,f4,g4,h4,a3,b3,c3,d3,e3,f3,g3,h3,a2,b2,c2,d2,e2,f2,g2,h2,a1,b1,c1,d1,e1,f1,g1,h1,tour\n")
df[] = lapply(df,factor)
for (colname in names(df)){
  levels(df[[colname]])=model$forest$xlevels[[colname]]
}
etat=read.table("C:/Users/Nicolas\ Martin/chess/state.csv",sep=",")
df<- rbind(df,etat,use.names=FALSE)
df$label = NA
pred <- abs(as.numeric(predict(model,df)))
if (pred==1 | pred==12){
  ind_mod = 6
} else if (pred==2 | pred==10){
  ind_mod = 5
} else if (pred==3 | pred==10){
  ind_mod = 4
} else if (pred==4 | pred==9){
  ind_mod = 3
} else if (pred==5 | pred==8){
  ind_mod = 2
} else {
  ind_mod = 1
}
st2 <- Sys.time()
model_piece <- readRDS(paste("C:/Users/Nicolas\ Martin/chess/models/model",ind_mod,".rds",sep=""))
end2 <- Sys.time()
#print(end1-st1+end2-st2)
df=fread("a8,b8,c8,d8,e8,f8,g8,h8,a7,b7,c7,d7,e7,f7,g7,h7,a6,b6,c6,d6,e6,f6,g6,h6,a5,b5,c5,d5,e5,f5,g5,h5,a4,b4,c4,d4,e4,f4,g4,h4,a3,b3,c3,d3,e3,f3,g3,h3,a2,b2,c2,d2,e2,f2,g2,h2,a1,b1,c1,d1,e1,f1,g1,h1,tour\n")
df[] = lapply(df,factor)
for (colname in names(df)){
  levels(df[[colname]])=model_piece$forest$xlevels[[colname]]
}
df<- rbind(df,etat,use.names=FALSE)
df$label = NA
write.table(c(ind_mod,names(df)[as.numeric(predict(model_piece,df))]),"C:/Users/Nicolas\ Martin/chess/response.csv",col.names=F,row.names=F,eol=",")
options(warn=0)
endall <- Sys.time()
#print(endall-startall)
