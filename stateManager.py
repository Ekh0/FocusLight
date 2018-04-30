from sklearn.externals import joblib
from lightController import lightController
from eventLogger import EventLogger
from dataCollector import dataCollector
import dataFormatter
import configparser
import time
import pytz
import threading
import numpy as np
from datetime import datetime
from datetime import timedelta
import json
class StateManager:
    #controll the state(light)
    def __init__(self):
        self.model = self.loadModel()#load the trained ML ,pde;
        self.state = -1#-1 for afk, 0 for not working, 1 for working
        self.light = lightController()
        self.pastStatus = [-1,-1,-1]#save the last 3 status
        self.loadWhiteList()
        self.light.yellow()
        self.TD = 1#time delta
        self.stop = False
    
    #load trained ML model
    def loadModel(self):
        clf = joblib.load('model.pkl') 
        return clf
    #load white list
    def loadWhiteList(self):
        f = open("whiteList.txt","r")
        self.wl = []
        for l in f.readlines():
            self.wl.append(l.rstrip('\n'))
        f.close()
        print(self.wl)

    #determine the current state from the past 3 status
    def determineState(self):
        d = {-1:0,0:0,1:0}
        for i in self.pastStatus:
            d[i] +=1
        for k,v in d.items():
            if v > 1:
                return k
        return -1

    # run the program, collect new data, determine the state and change light color
    def run(self):
        config = configparser.ConfigParser()
        config.read('settings.config')
        port = int(config['ACTIVITY_WATCHER']['PORT'])
        self.DC = dataCollector(port)

        while not self.stop:
            e = self.DC.getEvents()#get new events
            if(e == None):
                #new event not available
                time.sleep(1)
                continue
            else:
                #save new data point
                e['past_time'] = str(e['past_time'])
                e['time'] = str(e['time'])
                js = json.dumps(e)
                f = open("new_data.json","a")
                f.write(js)
                f.write('\n')
                f.close()

                #change past status
                self.pastStatus[0] = self.pastStatus[1]
                self.pastStatus[1] = self.pastStatus[2]
                if(e['afk']['data']['status']=='not-afk'):
                    #not afk
                    apps, features = dataFormatter.format(e)
                    finished = False
                    for i in range(len(apps)):
                        for j in self.wl:
                            if (float(apps[i][2]) > 0.25 and (j.lower() in apps[i][0].lower()) or (j.lower() in apps[i][1].lower())):
                                self.pastStatus[2] = 0
                                print("white list found")
                                finished = True
                    if not finished:
                        #state not determined by applications
                        re = self.model.predict(features[1:].reshape(1, -1))
                        print("prediction: "+str(re[0]))
                        self.pastStatus[2] = int(re[0])
                    #print(apps)
                else:
                    #afk
                    self.pastStatus[2] = -1
            self.state = self.determineState()
            if(self.state == -1):
                print("State: AFK")
                self.light.yellow()
            elif(self.state == 0):
                print("State: not working")
                self.light.green()
            else:
                print("State: working")
                self.light.red()

    def start(self):
        t = threading.Thread(target = self.run)
        t.start()
        while True:
            i = input()
            if i == 'q':
                #stopping
                 self.stop = True
                 print("Stopping...")
                 break        

if __name__ == '__main__':
    sm = StateManager()
    sm.start()