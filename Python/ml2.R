rm(list = ls())


library(randomForest)
library(data.table)

#ssh 3800666@ssh.ufr-info-p6.jussieu.fr
#ssh 3800666@pc56.polytech.upmc.fr

data <- fread("moves.csv")

columns <- c("a8","b8","c8","d8","e8","f8","g8","h8",
        "a7","b7","c7","d7","e7","f7","g7","h7",
        "a6","b6","c6","d6","e6","f6","g6","h6",
        "a5","b5","c5","d5","e5","f5","g5","h5",
        "a4","b4","c4","d4","e4","f4","g4","h4",
        "a3","b3","c3","d3","e3","f3","g3","h3",
        "a2","b2","c2","d2","e2","f2","g2","h2",
        "a1","b1","c1","d1","e1","f1","g1","h1","tour","move")

dataset<-data
colnames(dataset) <- columns

y_sour<- rep(0,dim(dataset)[1])
for (i in 1:dim(dataset)[1]){
  y_sour[i] = dataset[[i,substring(data$V66[i],1,2)]]
}
dataset$piece=abs(y_sour)

###############################################################################
dataset5= dataset[dataset$piece==5,-c(67)]
y<- rep(0,dim(dataset5)[1])
for (i in 1:dim(dataset5)[1]){
  y[i] = match(substring(dataset5$move[i],3,4),columns)
}
dataset5$dest=y
dataset5 = dataset5[,-c(66)]
dataset5[] = lapply(dataset5,factor)


n <- nrow(dataset5)
test.ratio <- .01 # ratio of test/train samples
n.test <- round(n*test.ratio)
tr <- sample(1:n,n.test)
data.test <- dataset5[tr,]
data.train <- dataset5[-tr,]

attach(data.train)
rf_model5 <- randomForest(data = data.train, dest ~ ., do.trace = 1,ntree=32)
detach(data.train)

pred <- predict(rf_model5, newdata = data.test)
table<-table(data.test$dest,pred)
accuracy<- sum(diag(table))/sum(table)
print(accuracy)
saveRDS(rf_model5,"./model5.rds")

###############################################################################
dataset6= dataset[dataset$piece==6,-c(67)]
y<- rep(0,dim(dataset6)[1])
for (i in 1:dim(dataset6)[1]){
  y[i] = match(substring(dataset6$move[i],3,4),columns)
}
dataset6$dest=y
dataset6 = dataset6[,-c(66)]
dataset6[] = lapply(dataset6,factor)


n <- nrow(dataset6)
test.ratio <- .01 # ratio of test/train samples
n.test <- round(n*test.ratio)
tr <- sample(1:n,n.test)
data.test <- dataset6[tr,]
data.train <- dataset6[-tr,]

attach(data.train)
rf_model6 <- randomForest(data = data.train, dest ~ ., do.trace = 1,ntree=8)
detach(data.train)

pred <- predict(rf_model6, newdata = data.test)
table<-table(data.test$dest,pred)
accuracy<- sum(diag(table))/sum(table)
print(accuracy)
saveRDS(rf_model6,)



###############################################################################
dataset4= dataset[dataset$piece==4,-c(67)]
y<- rep(0,dim(dataset4)[1])
for (i in 1:dim(dataset4)[1]){
  y[i] = match(substring(dataset4$move[i],3,4),columns)
}
dataset4$dest=y
dataset4 = dataset4[,-c(66)]
dataset4[] = lapply(dataset4,factor)


n <- nrow(dataset4)
test.ratio <- .01 # ratio of test/train samples
n.test <- round(n*test.ratio)
tr <- sample(1:n,n.test)
data.test <- dataset4[tr,]
data.train <- dataset4[-tr,]

attach(data.train)
rf_model4 <- randomForest(data = data.train, dest ~ ., do.trace = 1,ntree=4)
detach(data.train)

pred <- predict(rf_model4, newdata = data.test)
table<-table(data.test$dest,pred)
accuracy<- sum(diag(table))/sum(table)
print(accuracy)
saveRDS(rf_model4,"./model4.rds")


###############################################################################
dataset3= dataset[dataset$piece==3,-c(67)]
y<- rep(0,dim(dataset3)[1])
for (i in 1:dim(dataset3)[1]){
  y[i] = match(substring(dataset3$move[i],3,4),columns)
}
dataset3$dest=y
dataset3 = dataset3[,-c(66)]
dataset3[] = lapply(dataset3,factor)


n <- nrow(dataset3)
test.ratio <- .01 # ratio of test/train samples
n.test <- round(n*test.ratio)
tr <- sample(1:n,n.test)
data.test <- dataset3[tr,]
data.train <- dataset3[-tr,]

attach(data.train)
rf_model3 <- randomForest(data = data.train, dest ~ ., do.trace = 1,ntree=8)
detach(data.train)

pred <- predict(rf_model3, newdata = data.test)
table<-table(data.test$dest,pred)
accuracy<- sum(diag(table))/sum(table)
print(accuracy)
saveRDS(rf_model3,"./model3.rds")


###############################################################################
dataset2= dataset[dataset$piece==2,-c(67)]
y<- rep(0,dim(dataset2)[1])
for (i in 1:dim(dataset2)[1]){
  y[i] = match(substring(dataset2$move[i],3,4),columns)
}
dataset2$dest=y
dataset2 = dataset2[,-c(66)]
dataset2[] = lapply(dataset2,factor)


n <- nrow(dataset2)
test.ratio <- .01 # ratio of test/train samples
n.test <- round(n*test.ratio)
tr <- sample(1:n,n.test)
data.test <- dataset2[tr,]
data.train <- dataset2[-tr,]

attach(data.train)
rf_model2 <- randomForest(data = data.train, dest ~ ., do.trace = 1,ntree=4)
detach(data.train)

pred <- predict(rf_model2, newdata = data.test)
table<-table(data.test$dest,pred)
accuracy<- sum(diag(table))/sum(table)
print(accuracy)
saveRDS(rf_model2,"./model2.rds")


###############################################################################
dataset1= dataset[dataset$piece==1,-c(67)]
y<- rep(0,dim(dataset1)[1])
for (i in 1:dim(dataset1)[1]){
  y[i] = match(substring(dataset1$move[i],3,4),columns)
}
dataset1$dest=y
dataset1 = dataset1[,-c(66)]
dataset1[] = lapply(dataset1,factor)


n <- nrow(dataset1)
test.ratio <- .01 # ratio of test/train samples
n.test <- round(n*test.ratio)
tr <- sample(1:n,n.test)
data.test <- dataset1[tr,]
data.train <- dataset1[-tr,]

attach(data.train)
rf_model1 <- randomForest(data = data.train, dest ~ ., do.trace = 1,ntree=4)
detach(data.train)

pred <- predict(rf_model1, newdata = data.test)
table<-table(data.test$dest,pred)
accuracy<- sum(diag(table))/sum(table)
print(accuracy)
saveRDS(rf_model1,"./model1.rds")
