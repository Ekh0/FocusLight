from eventLogger import EventLogger
import requests
import pytz
import time
from datetime import datetime
from datetime import timedelta
from dateutil import parser
from requests.auth import HTTPDigestAuth
import json
TD = 1 #time delta
class dataCollector:
    #collect window, mouse, keyboard data from user
    def __init__(self,port):
        self.bucketsInitialized = False
        self.port = port
        self.initBuckets()
        self.pastTime = datetime.utcnow().replace(tzinfo=pytz.UTC)
        self.logger = EventLogger()
        print("Collecting Data")
    def get(self,url):
        myResponse = requests.get(url)
        if(myResponse.ok):
            return myResponse
        else:
            myResponse.raise_for_status()
    #send request to activity watcher and initialize lists for corresponding buckets
    def initBuckets(self):
        url = "http://localhost:"+str(self.port)+"/api/0/buckets/"
        res = self.get(url)
        b = []
        for k in json.loads(res.content):
            b.append(k)
        for s in b:
            if "afk" in s:
                self.afkWatcher = str(s)
            elif "window" in s:
                self.windowWatcher = str(s)
        self.bucketsInitialized = True

    def getAfkEvents(self):
        if not self.bucketsInitialized:
            return None
        else:
            url = "http://localhost:"+str(self.port)+"/api/0/buckets/"+self.afkWatcher+"/events"
            res = self.get(url)
            jData = json.loads(res.content)
            return jData

    def getWindowEvents(self):
        if not self.bucketsInitialized:
            return None
        else:
            url = "http://localhost:"+str(self.port)+"/api/0/buckets/"+self.windowWatcher+"/events"
            res = self.get(url)
            jData = json.loads(res.content)
            return jData

    #get all events in the past timedelta and combine them to a json
    def getEvents(self):
        if(datetime.utcnow().replace(tzinfo=pytz.UTC)-timedelta(minutes = TD)<self.pastTime):
            #print("Nope")
            return None
        else:
            afkEvents = self.getAfkEvents()
            winEvents = self.getWindowEvents()
            res = {}
            win = []
            res['afk'] = afkEvents[0]
            first = True
            for key in winEvents:
                if first:
                    win.append(key)
                    first = False
                    continue
                if parser.parse(key['timestamp'])< self.pastTime:
                    break
                win.append(key)
            res['win'] = win
            kEvents,mEvents = self.logger.getEvents()
            res['key'] = kEvents
            res['mouse'] = mEvents
            res['past_time'] = self.pastTime
            self.pastTime = datetime.utcnow().replace(tzinfo=pytz.UTC)
            res['time'] = self.pastTime 
            return res
    #This method was used to collect initial data
    #Data was collected in raw text form to check correctness
    def recordData(self):
        while True:
            dic = d.getEvents()
            if dic:
                dic['past_time'] = str(dic['past_time'])
                dic['time'] = str(dic['time'])
                js = json.dumps(dic)
                f = open("data.json","a")
                f.write(js)
                f.write('\n')
                f.close()
                print ("record added")
            time.sleep(61)

if __name__ == '__main__':
    d = dataCollector(5600)
    d.recordData()