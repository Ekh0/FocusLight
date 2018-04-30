import json
import numpy as np
import configparser
SCREEN_SPLITS = 16 #split screen into 16 areas
#map key to indice
KEY_MAPPING = {"KEY_ESCAPE":SCREEN_SPLITS+1,
               "KEY_F1":SCREEN_SPLITS+2,
               "KEY_F2":SCREEN_SPLITS+3,
               "KEY_F3":SCREEN_SPLITS+4,
               "KEY_F4":SCREEN_SPLITS+5,
               "KEY_F5":SCREEN_SPLITS+6,
               "KEY_F6":SCREEN_SPLITS+7,
               "KEY_F7":SCREEN_SPLITS+8,
               "KEY_F8":SCREEN_SPLITS+9,
               "KEY_F9":SCREEN_SPLITS+10,
               "KEY_F10":SCREEN_SPLITS+11,
               "KEY_F11":SCREEN_SPLITS+12,
               "KEY_F12":SCREEN_SPLITS+13,
               "KEY_PRINT_SCREEN":SCREEN_SPLITS+14,
               "KEY_1":SCREEN_SPLITS+15,
               "KEY_2":SCREEN_SPLITS+16,
               "KEY_3":SCREEN_SPLITS+17,
               "KEY_4":SCREEN_SPLITS+18,
               "KEY_5":SCREEN_SPLITS+19,
               "KEY_6":SCREEN_SPLITS+20,
               "KEY_7":SCREEN_SPLITS+21,
               "KEY_8":SCREEN_SPLITS+22,
               "KEY_9":SCREEN_SPLITS+23,
               "KEY_0":SCREEN_SPLITS+24,
               "KEY_MINUS":SCREEN_SPLITS+25,
               "KEY_EQUALS":SCREEN_SPLITS+26,
               "KEY_BACKSPACE":SCREEN_SPLITS+27,
               "KEY_TAB":SCREEN_SPLITS+28,
               "KEY_Q":SCREEN_SPLITS+29,
               "KEY_W":SCREEN_SPLITS+30,
               "KEY_E":SCREEN_SPLITS+31,
               "KEY_R":SCREEN_SPLITS+31,
               "KEY_T":SCREEN_SPLITS+33,
               "KEY_Y":SCREEN_SPLITS+34,
               "KEY_U":SCREEN_SPLITS+35,
               "KEY_I":SCREEN_SPLITS+36,
               "KEY_O":SCREEN_SPLITS+37,
               "KEY_P":SCREEN_SPLITS+38,
               "KEY_LEFT_BRACKET":SCREEN_SPLITS+39,
               "KEY_RIGHT_BRACKET":SCREEN_SPLITS+40,
               "KEY_BACKSLASH":SCREEN_SPLITS+41,
               "KEY_DELETE":SCREEN_SPLITS+42,
               "KEY_CAPSLOCK":SCREEN_SPLITS+43,
               "KEY_A":SCREEN_SPLITS+44,
               "KEY_S":SCREEN_SPLITS+45,
               "KEY_D":SCREEN_SPLITS+46,
               "KEY_F":SCREEN_SPLITS+47,
               "KEY_G":SCREEN_SPLITS+48,
               "KEY_H":SCREEN_SPLITS+49,
               "KEY_J":SCREEN_SPLITS+50,
               "KEY_K":SCREEN_SPLITS+51,
               "KEY_L":SCREEN_SPLITS+52,
               "KEY_SEMICOLON":SCREEN_SPLITS+53,
               "KEY_APOSTROPHE":SCREEN_SPLITS+54,
               "KEY_RETURN":SCREEN_SPLITS+55,
               "KEY_LEFT_SHIFT":SCREEN_SPLITS+56,
               "KEY_Z":SCREEN_SPLITS+57,
               "KEY_X":SCREEN_SPLITS+58,
               "KEY_C":SCREEN_SPLITS+59,
               "KEY_V":SCREEN_SPLITS+60,
               "KEY_B":SCREEN_SPLITS+61,
               "KEY_N":SCREEN_SPLITS+62,
               "KEY_M":SCREEN_SPLITS+63,
               "KEY_COMMA":SCREEN_SPLITS+64,
               "KEY_PERIOD":SCREEN_SPLITS+65,
               "KEY_SLASH":SCREEN_SPLITS+66,
               "KEY_RIGHT_SHIFT":SCREEN_SPLITS+67,
               "KEY_UP":SCREEN_SPLITS+68,
               "KEY_LEFT_CTRL":SCREEN_SPLITS+69,
               "KEY_LEFT_SUPER":SCREEN_SPLITS+70,
               "KEY_LEFT_ALT":SCREEN_SPLITS+71,
               "KEY_SPACE":SCREEN_SPLITS+72,
               "KEY_RIGHT_ALT":SCREEN_SPLITS+73,
               "KEY_RIGHT_SUPER":SCREEN_SPLITS+74,
               "KEY_RIGHT_CTRL":SCREEN_SPLITS+75,
               "KEY_LEFT":SCREEN_SPLITS+76,
               "KEY_DOWN":SCREEN_SPLITS+77,
               "KEY_RIGHT":SCREEN_SPLITS+78}

#return the corresponding screen area number for a mouse event
def getSplitNum(x,y):
    config = configparser.ConfigParser()
    config.read('settings.config')
    maxX = int(config['SCREEN']['RESOLUTION_WIDTH'])
    maxY = int(config['SCREEN']['RESOLUTION_HEIGHT'])
    xS = maxX/4
    yS = maxY/4
    if(0<=y<yS):
        if(0<=x<xS):
            return 1
        elif(xS<=x<2*xS):
            return 2
        elif(2*xS<=x<3*xS):
            return 3
        elif(3*xS<=x<maxX):
            return 4
    elif(yS<=y<2*yS):
        if(0<=x<xS):
            return 5
        elif(xS<=x<2*xS):
            return 6
        elif(2*xS<=x<3*xS):
            return 7
        elif(3*xS<=x<maxX):
            return 8
    elif(2*yS<=y<3*yS):
        if(0<=x<xS):
            return 9
        elif(xS<=x<2*xS):
            return 10
        elif(2*xS<=x<3*xS):
            return 11
        elif(3*xS<=x<maxX):
            return 12
    else:
        if(0<=x<xS):
            return 13
        elif(xS<=x<2*xS):
            return 14
        elif(2*xS<=x<3*xS):
            return 15
        elif(3*xS<=x<maxX):
            return 16

#for testing, print differnt field in the collected data
def printLine(line):
    print(line['past_time'])
    print(line['time'])
    print(line['afk']['data']['status'])
    for w in line['win']:
        print(w)
    for k in line['key']:
        k2 = k['k'].split(".")
        print(k2[1])
        print(k2[1] in KEY_MAPPING.keys())
    for m in line['mouse']:
        print(m)
        print(getSplitNum(int(m['x']),int(m['y'])))

#extract features from raw data and create a sample
def getFeatures(line):
    aU = np.zeros(SCREEN_SPLITS+79)
    aD = np.zeros(SCREEN_SPLITS+79)
    arr = ""
    for m in line['mouse']:
        if(m['d']=='u'):
            arr = aU
            #button up
        else:
            arr = aD
            #button down
        if m['e']=='s':
                #scroll
                arr[0] += 1
        else:
            #click
            arr[getSplitNum(int(m['x']),int(m['y']))] += 1

    for k in line['key']:
        if(k['e']=='u'):
            #up
            arr = aU
        else:
            #down
            arr = aD
        try:
            arr[KEY_MAPPING[k['k'].split(".")[1]]]+=1
        except:
            print("KEY ERROR "+k['k'].split(".")[1])
            
    aH = np.zeros(1)
    return np.concatenate([aH,aU,aD],axis = 0)

#get the active application information from raw data
def getApps(line):
    totalTime = 0
    apps = []
    for w in line['win']:
        totalTime += float(w['duration'])
    for w in line['win']:
        l = []
        l.append(w['data']['app'])
        l.append(w['data']['title'])
        l.append("{0:.2f}".format(float(w['duration'])/totalTime))
        apps.append(l)
    return apps

#format the raw json, return a list of application information, and a array of features extracted from the corresponding mouse&keyboard events
def format(js):
    return getApps(js),getFeatures(js)

if __name__ == '__main__':
    f = open("data.json","r")
    lines = f.readlines()
    js = json.loads(lines[-30])
    print(getFeatures(js))
    print(getApps(js))