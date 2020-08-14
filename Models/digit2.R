rm(list = ls())


library(randomForest)
library(data.table)


train <- fread("../mnist_train.csv")
test <- fread("../mnist_test.csv")

print("started modelling...")

train$label <- factor(train$label)
attach(train)
rf_model <- randomForest(data = train, label ~ ., do.trace = 1,ntree=32)
detach(train)

print("random forest trained.")

pred <- predict(rf_model, newdata = test)
table<-table(test$label,pred)
accuracy<- sum(diag(table))/sum(table)
print(accuracy)
