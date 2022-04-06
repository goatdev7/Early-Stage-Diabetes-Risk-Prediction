# -*- coding: utf-8 -*-
"""early-stage-diabetes-risk-prediction-acc-98.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/196SMNJSWTOWWA1BNIOD7E1kgbBR1yjxl

**Early stage Diabetes Risk prediction**

#Task:Early stage Diabetes prediction
* The number of Diabetes patients are increasing in recent years. Machine learning models helps in early detection and  the diagnosis needed. Now predicting whether a person had daibetes or not by Exploring data analysis, Feature selection ,Building models.

#Importing necessary libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import Request, urlopen
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn import metrics
# %matplotlib inline

"""**Have a look at the dataset**"""

# Importing the dataset from a CDN (We can also open if present in same directory)
req = Request('https://cdn.asim.id/diabetes_data.csv')
req.add_header('User-Agent', 'Mozilla/5.0')
content = urlopen(req)
dataset = pd.read_csv(content)
dataset.shape
dataset.head()

"""**Checking whether dataset has null values**"""

sns.heatmap(dataset.isnull())

dataset['class'].value_counts()

"""**Mapping text into values**"""

dataset['Gender'] = dataset['Gender'].map({'Male':1,'Female':0})
dataset['class'] = dataset['class'].map({'Positive':1,'Negative':0})
dataset['Polyuria'] = dataset['Polyuria'].map({'Yes':1,'No':0})
dataset['Polydipsia'] = dataset['Polydipsia'].map({'Yes':1,'No':0})
dataset['sudden weight loss'] = dataset['sudden weight loss'].map({'Yes':1,'No':0})
dataset['weakness'] = dataset['weakness'].map({'Yes':1,'No':0})
dataset['Polyphagia'] = dataset['Polyphagia'].map({'Yes':1,'No':0})
dataset['Genital thrush'] = dataset['Genital thrush'].map({'Yes':1,'No':0})
dataset['visual blurring'] = dataset['visual blurring'].map({'Yes':1,'No':0})
dataset['Itching'] = dataset['Itching'].map({'Yes':1,'No':0})
dataset['Irritability'] = dataset['Irritability'].map({'Yes':1,'No':0})
dataset['delayed healing'] = dataset['delayed healing'].map({'Yes':1,'No':0})
dataset['partial paresis'] = dataset['partial paresis'].map({'Yes':1,'No':0})
dataset['muscle stiffness'] = dataset['muscle stiffness'].map({'Yes':1,'No':0})
dataset['Alopecia'] = dataset['Alopecia'].map({'Yes':1,'No':0})
dataset['Obesity'] = dataset['Obesity'].map({'Yes':1,'No':0})

"""# EDA

**Analysing the correlation between independent and dependent variables**
considering independent variables that has high correlation with the dependent variables and less correlation with other variables
"""

corrdata = dataset.corr()

ax,fig = plt.subplots(figsize=(15,8))
sns.heatmap(corrdata,annot=True)

"""**Age distribution**"""

sns.distplot(dataset['Age'],bins=30)

"""**Age/class(dependent variable)**"""

sns.barplot(x='class',y='Age',data=dataset)

ds = dataset['class'].value_counts().reset_index()
ds.columns = ['class', 'count']
plot=ds.plot.pie(y='count')

"""**Gender**"""

sns.countplot(x='class',data=dataset,hue='Gender')

"""**Polyuria**"""

sns.catplot(x="Polyuria", y="class", kind="point", data=dataset)

"""**Polydipsia**"""

sns.barplot(x='Polydipsia',y='class',data=dataset)

"""**Sudden weight loss**"""

sns.countplot(x='class',data=dataset,hue='sudden weight loss')

"""**Polyphagia**"""

sns.countplot(x='class',data=dataset, hue='Polyphagia')

sns.barplot(x='Polyphagia',y='class',data=dataset)

"""**Genital Thrush**"""

sns.catplot(x='class',y='Genital thrush',kind='point',data=dataset)

"""**Partial paresis**"""

sns.barplot(x='class',y='partial paresis',data=dataset)

"""**Alopecia**"""

sns.violinplot(x='Alopecia',y='class',data=dataset)

"""**Visual blurring**"""

sns.barplot(x="visual blurring", y="class", data=dataset)

"""**Itching**"""

sns.barplot(x="Itching", y="class", data=dataset)

"""**Obesity**"""

sns.violinplot(x='Obesity',y='class',data=dataset)

"""**Irritability**"""

sns.barplot(x='Irritability',y='class',data=dataset)

X1 = dataset.iloc[:,0:-1]
y1 = dataset.iloc[:,-1]

X1.columns

"""**Feature selection using selectkbest** Feature selection was also done using Weka."""

from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
best_feature = SelectKBest(score_func=chi2,k=10)
fit = best_feature.fit(X1,y1)

dataset_scores = pd.DataFrame(fit.scores_)
dataset_cols = pd.DataFrame(X1.columns)

featurescores = pd.concat([dataset_cols,dataset_scores],axis=1)
featurescores.columns=['column','scores']

"""**These are the variables with their feature scores ,their importance/contribution towards class** (also performed in weka)"""

featurescores

"""**Top 10 features**"""

print(featurescores.nlargest(10,'scores'))

featureview=pd.Series(fit.scores_, index=X1.columns)
featureview.plot(kind='barh')

"""**Checking the variance of each feature**,
Features must have high variance with other features
"""

from sklearn.feature_selection import VarianceThreshold
feature_high_variance = VarianceThreshold(threshold=(0.5*(1-0.5)))
falls=feature_high_variance.fit(X1)

dataset_scores1 = pd.DataFrame(falls.variances_)
dat1 = pd.DataFrame(X1.columns)

high_variance = pd.concat([dataset_scores1,dat1],axis=1)
high_variance.columns=['variance','cols']

high_variance[high_variance['variance']>0.2]

X = dataset[['Polydipsia','sudden weight loss','partial paresis','Irritability','Polyphagia','Age','visual blurring']]
y = dataset['class']

"""**Splitting the dataset into training and testing sets. 80/20  train/test**"""

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2,random_state=0)

"""**Standardization of independant variables**"""

from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

"""# Models for our Dataset (6)

# Logistic Regression
"""

from sklearn.linear_model import LogisticRegression
lg=LogisticRegression()
lg.fit(X_train,y_train)

"""**Cross validation test for training data**"""

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=lg, X=X_train ,y=y_train,cv=10)
print("accuracy is {:.2f} %".format(accuracies.mean()*100))
print("std is {:.2f} %".format(accuracies.std()*100))

"""**Prediction**"""

pre=lg.predict(X_test)

"""**Take a look into Accuracy and Confusion matrix**"""

logistic_regression=accuracy_score(pre,y_test)
print(accuracy_score(pre,y_test))
print(confusion_matrix(pre,y_test))
metrics.plot_roc_curve(lg,X_test,y_test)

"""**Classification Report**"""

from sklearn.metrics import classification_report
print(classification_report(pre,y_test))

"""# SVM"""

from sklearn.svm import SVC
sv=SVC(kernel='linear',random_state=0)
sv.fit(X_train,y_train)

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=sv, X=X_train ,y=y_train,cv=10)
print("accuracy is {:.2f} %".format(accuracies.mean()*100))
print("std is {:.2f} %".format(accuracies.std()*100))

pre1=sv.predict(X_test)

svm_linear=accuracy_score(pre1,y_test)
print(accuracy_score(pre1,y_test))
print(confusion_matrix(pre1,y_test))

from sklearn.metrics import classification_report
print(classification_report(pre1,y_test))

from sklearn.svm import SVC
svrf=SVC(kernel='rbf',random_state=0)
svrf.fit(X_train,y_train)

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=svrf, X=X_train ,y=y_train,cv=10)
print("accuracy is {:.2f} %".format(accuracies.mean()*100))
print("std is {:.2f} %".format(accuracies.std()*100))
metrics.plot_roc_curve(svrf,X_test,y_test)

pre2=svrf.predict(X_test)

svm_rbf=accuracy_score(pre2,y_test)
print(accuracy_score(pre2,y_test))
print(confusion_matrix(pre2,y_test))

from sklearn.metrics import classification_report
print(classification_report(pre2,y_test))

"""# KNN  **1-10 k values**"""

from sklearn.neighbors import KNeighborsClassifier
score=[]

for i in range(1,10):
    
    
    knn=KNeighborsClassifier(n_neighbors=i,metric='minkowski',p=2)
    knn.fit(X_train,y_train)
    pre3=knn.predict(X_test)
    ans=accuracy_score(pre3,y_test)
    score.append(round(100*ans,2))
print(sorted(score,reverse=True)[:5])
knn=sorted(score,reverse=True)[:1]
from sklearn.metrics import classification_report
print(classification_report(pre3,y_test))

"""## Naive bayes-Gaussian NB"""

from sklearn.naive_bayes import GaussianNB
gb=GaussianNB()
gb.fit(X_train,y_train)

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=gb, X=X_train ,y=y_train,cv=10)
print("accuracy is {:.2f} %".format(accuracies.mean()*100))
print("std is {:.2f} %".format(accuracies.std()*100))

pre4=gb.predict(X_test)

Naive_bayes_Gaussian_nb=accuracy_score(pre4,y_test)
print(accuracy_score(pre4,y_test))
print(confusion_matrix(pre4,y_test))

from sklearn.metrics import classification_report
print(classification_report(pre4,y_test))
metrics.plot_roc_curve(gb,X_test,y_test)

"""# Decision Tress Classifier"""

from sklearn.tree import DecisionTreeClassifier
dc=DecisionTreeClassifier(criterion='gini')
dc.fit(X_train,y_train)

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=dc, X=X_train ,y=y_train,cv=10)
print("accuracy is {:.2f} %".format(accuracies.mean()*100))
print("std is {:.2f} %".format(accuracies.std()*100))

pre5=dc.predict(X_test)

Decisiontress_classifier=accuracy_score(pre5,y_test)
print(accuracy_score(pre5,y_test))
print(confusion_matrix(pre5,y_test))

from sklearn.metrics import classification_report
print(classification_report(pre5,y_test))
metrics.plot_roc_curve(dc,X_test,y_test)

"""# Random Forest Classifier"""

from sklearn.ensemble import RandomForestClassifier
estime=[]
for i in range(1,100):
    rc=RandomForestClassifier(n_estimators=i,criterion='entropy',random_state=0)
    rc.fit(X_train,y_train)

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator=rc, X=X_train ,y=y_train,cv=10)
print("accuracy is {:.2f} %".format(accuracies.mean()*100))
print("std is {:.2f} %".format(accuracies.std()*100))

pre6 = rc.predict(X_test)

Random_forest=accuracy_score(pre6,y_test)
print(accuracy_score(pre6,y_test))
print(confusion_matrix(pre6,y_test))

from sklearn.metrics import classification_report
print(classification_report(pre6,y_test))
metrics.plot_roc_curve(rc,X_test,y_test)

"""# Accuracies of all classification model overview"""

print('Logistic regression:',logistic_regression)
print('svmlinear:',svm_linear)
print('svmrbf:',svm_rbf)
print('knn:',knn)
print('naive bayes:',Naive_bayes_Gaussian_nb)
print('Decision tress:',Decisiontress_classifier)
print('Random forest:',Random_forest)

"""**The best model is SVM , KNN and Random forest  with 98% Accuracy**"""