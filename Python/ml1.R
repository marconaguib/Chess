rm(list = ls())

library(randomForest)

setwd("C:\\Users\\Nicolas Martin\\chess")


data <- read.table("./moves.csv",sep=",")

dataset<-data[,c(-66)]

columns <- c("a8","b8","c8","d8","e8","f8","g8","h8",
        "a7","b7","c7","d7","e7","f7","g7","h7",
        "a6","b6","c6","d6","e6","f6","g6","h6",
        "a5","b5","c5","d5","e5","f5","g5","h5",
        "a4","b4","c4","d4","e4","f4","g4","h4",
        "a3","b3","c3","d3","e3","f3","g3","h3",
        "a2","b2","c2","d2","e2","f2","g2","h2",
        "a1","b1","c1","d1","e1","f1","g1","h1","tour")

colnames(dataset) <- columns

y<- rep(0,dim(dataset)[1])
for (i in 1:dim(dataset)[1]){
  y[i] = dataset[[i,substring(data$V66[i],1,2)]]
}
y<- as.factor(y)
dataset$label=y
dataset2<-dataset


n <- nrow(dataset2)
test.ratio <- .01 # ratio of test/train samples
n.test <- round(n*test.ratio)
tr <- sample(1:n,n.test)
data.test <- dataset2[tr,]
data.train <- dataset2[-tr,]

attach(data.train)
rf_model<- randomForest(label ~ .,data = data.train, do.trace = 1, ntree=32)
#model <- neuralnet(label ~ .,data = data.train, hidden=c(16,16), linear.output=FALSE)
detach(data.train)


pred <- predict(rf_model, newdata = data.test)
table<-table(data.test$label,pred)
accuracy<- sum(diag(table))/sum(table)
print(accuracy)

saveRDS(model,"./mo.rds")
