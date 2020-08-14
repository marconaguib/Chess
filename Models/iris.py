#Import Libraries and Read the data
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, tree
from sklearn.model_selection import train_test_split
data  =  pd.read_csv("Iris.csv",sep=",")#Create Dependent and Independent Datasets based on our Dependent
#and Independent features
X  = data[['Sepal.Length','Sepal.Width','Petal.Length']]
y= data['Species']
#Split the Data into Training and Testing sets with test size as #30%
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3, shuffle=True)

classifiers=[]
model2 = svm.SVC()
classifiers.append(model2)
model3 = tree.DecisionTreeClassifier()
classifiers.append(model3)
model4 = RandomForestClassifier()
classifiers.append(model4)


for clf in classifiers:
    clf.fit(X_train,y_train)
    y_pred=clf.predict(X_test)
    acc=accuracy_score(y_test,y_pred)
    print(acc)
    cm=confusion_matrix(y_test,y_pred)
    print(cm)
