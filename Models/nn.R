# load library
rm(list=ls(all=TRUE))
require(neuralnet)


train <- data.frame(fread("../mnist_train.csv"))
test <- data.frame(fread("../mnist_test.csv"))

train$label=as.factor(train$label)
test$label=as.factor(test$label)
nn=neuralnet(label~.,data=train, hidden=c(50,50),act.fct = "logistic",linear.output = FALSE)


## Prediction using neural network
Predict=predict(nn,newdata=test)

pred<-rep(0,length(test$label))
for (i in 1:length(test$label)){
 pred[i]<-which.max(Predict[i,])-1
}
table<-table(test$label, pred)
accuracy<-sum(diag(table))/sum(table)
print(accuracy)
