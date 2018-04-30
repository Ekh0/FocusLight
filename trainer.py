import dataFormatter
import json
import pandas as pd 
import numpy as np
from datetime import datetime
from sklearn.cross_validation import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
from sklearn.model_selection import GridSearchCV

def allToCsv(jsName,csvName):
    #label all data and create a csv file with those data
    array = []
    f = open(jsName,"r")
    lines = f.readlines()
    if(len(lines)<3):
        print("Need more data")
        return None
    for l in lines:
        js =json.loads(l)
        apps = dataFormatter.getApps(js)
        feature = dataFormatter.getFeatures(js)
        print(js['time'])
        for a in apps:
            print(a)
        print(feature)
        i = input("1 if working, 0 if not\n")
        while i not in ["1","0"]:
            i = input("1 if working, 0 if not\n")
        feature[0] = int(i)
        array.append(feature)
    df = pd.DataFrame(np.array(array))
    df.to_csv(csvName)
    return True
#evaluate a ML model with accuracy 
def evaluateModel(data,label,model):
    start = datetime.now()
    acc = cross_val_score(model,data,label,scoring='accuracy').mean()
    end = datetime.now()
    time_use = (end-start).seconds
    print ('Time use: ', time_use)
    print ('Accuracy by cross validation: ', acc)

def readData(filename):
    dataset = pd.read_csv(filename)
    data = dataset.values[0:, 2:]
    label = dataset.values[0:, 1]
    #see sample distribution
    unique, counts = np.unique(label, return_counts=True)
    print(dict(zip(unique, counts)))
    print ('Data Loaded!')
    return data, label
#create a initial model with collected data
def initModel():
    data, label = readData("labeled_data.csv")
    model = MultinomialNB()
    model.fit(data,label)
    joblib.dump(model, 'model.pkl')

#test different ML models
def findBestModel():
    data, label = readData('labeled_data.csv')

    model = MultinomialNB()
    print ('MNB: ')
    evaluateModel(data,label,model)

    model = BernoulliNB()
    print ('BNB')
    evaluateModel(data,label,model)

    model = Perceptron()
    print ('P')
    evaluateModel(data,label,model)

    model = SGDClassifier()
    print ('SGD')
    evaluateModel(data,label,model)

    model = PassiveAggressiveClassifier()
    print ('PAC')
    evaluateModel(data,label,model)

    model = MLPClassifier(solver='adam', hidden_layer_sizes=(16,), activation ='relu')
    print('NN: ')
    evaluateModel(data,label,model)

#tune parameters for Neural network
def findParam():
    data, label = readData('labeled_data.csv')
    param_grid = [
        {
            'activation' : ['identity', 'logistic', 'tanh', 'relu'],
            'solver' : ['sgd', 'adam'],
            'hidden_layer_sizes': [
             (1,),(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(10,),(11,), (12,),(13,),(14,),(15,),(16,),(17,),(18,),(19,),(20,),(21,),(5,2),(5,5),(5,5,2)
             ]
        }
       ]
    clf = GridSearchCV(MLPClassifier(), param_grid, cv=5,scoring='accuracy')
    clf.fit(X = data,y = label)
    print("Best parameters set found on development set:")
    print(clf.best_params_)

#train existing model with additional data
def trainNew():
    n = allToCsv("new_data.json","new_labeled_data.csv")
    if(n == None):
        quit()
    data,label = readData("new_labeled_data.csv")
    clf = joblib.load('model.pkl') 
    clf.partial_fit(data,label)
    joblib.dump(clf, 'model.pkl')
    open("new_data.json","w").close()
    open("new_labeled_data.csv","w").close()
    print("Model updated.")

if __name__ == '__main__':
    ##for testing
    #allToCsv("data.json","labeled_data.csv")
    #initModel()
    #data, label = readData()
    #clf = joblib.load('model.pkl') 
    #findBestModel()
    #findParam()

    #fit the model incrementally with new data
    try:
        trainNew()
    except FileNotFoundError:
        print("No new data")

