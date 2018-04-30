import requests
import configparser
import time
class lightController:
    #Send requests to controll a phillips hue lightbulb
    def __init__(self):
        #read config
        config = configparser.ConfigParser()
        config.read('settings.config')
        self.id = config['LIGHT']['USER']
        self.ip = config['LIGHT']['IP']
        self.num = config['LIGHT']['LIGHT']
    #for send requests
    def put(self,body):    
        try:
            url = "http://"+self.ip+"/api/"+self.id+"/lights/"+self.num+"/state"
            res = requests.put(url,data = body)
            return res
        except:
            print("Light controlling request failed")
    #turn on the light
    def on(self):
        self.put('{"on":true}')
    #turn off the light
    def off(self):
        self.put('{"on":false}')
    #change color to red
    def red(self):
        self.put('{"on":true, "sat":254, "bri":254,"hue":65521}')
    #change color to green
    def green(self):
        self.put('{"on":true, "sat":254, "bri":254,"hue":23742}')
    #change color to yellow
    def yellow(self):
        self.put('{"on":true, "sat":254, "bri":254,"hue":10414}')
if __name__ == '__main__':
    #for testing
    LC = lightController()
    LC.on()
    time.sleep(5)
    LC.off()
    time.sleep(5)
    LC.red()
    time.sleep(5)
    LC.yellow()
    time.sleep(5)
    LC.green()