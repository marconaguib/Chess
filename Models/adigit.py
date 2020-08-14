import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm, tree
from sklearn.model_selection import train_test_split
import time

train = pd.read_csv("mnist_train.csv")
test  = pd.read_csv("mnist_test.csv")
print("c'est bon")

X_train,y_train = train.loc[:,train.columns!='label'],np.ravel(train.loc[:,train.columns=='label'])
X_test,y_test = test.loc[:,test.columns!='label'],np.ravel(test.loc[:,test.columns=='label'])


model = RandomForestClassifier()
acc=[]
temps=[]

start_time = time.time()
model.fit(X_train,y_train)
print(np.round((time.time() - start_time),3))
y_pred=model.predict(X_test)
print(np.round(accuracy_score(y_test,y_pred),3))
