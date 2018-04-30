from sneakysnek.recorder import Recorder
from sneakysnek.mouse_event import MouseEvent
from sneakysnek.keyboard_event import KeyboardEvent
from sneakysnek.mouse_event import MouseEvents
from sneakysnek.keyboard_event import KeyboardEvents
from sneakysnek.mouse_buttons import MouseButton
import time

class EventLogger:
    #log mouse and keyboard activities
    def __init__(self):
        self.recorder = Recorder.record(self.callBack)
        self.keys = []#for saving keybard events
        self.mice = []#for saving mouse events

    #callback function for sneakysnek
    def callBack(self,event):
        try:
            if(type(event) is MouseEvent):
                #mouse Event
                if(event.event is not MouseEvents.MOVE):
                    #ignore mouse move since there is too many
                    e = ""                  #click or scroll
                    button = ""             #mouse button
                    direction = ""          #up or down
                    velocity = event.velocity
                    x = event.x
                    y = event.y
                    if(event.event is MouseEvents.CLICK):
                        e = "c"#clice
                    else:
                        e = "s"#scroll
                    if(event.button is MouseButton.LEFT):
                        button = "l"#left button
                    elif(event.button is MouseButton.RIGHT):
                        button = "r"#right button
                    else:
                        button = "m"#middle button
                    if(event.direction == "DOWN"):
                        direction = "d"#down
                    else:
                        direction = "u"#up
                    d = {"e":e,"b":button,"d":direction,"v":velocity,"x":x,"y":y}
                    #print(d)
                    self.mice.append(d)
                
            else:
                #keyboard Events
                e = ""#up or down
                k = str(event.keyboard_key)#key pressed
                if(event.event is KeyboardEvents.UP):
                    e = 'u'#up
                else:
                    e = 'd'#down
                d = {"e":e,"k":k}
                #print(d)
                self.keys.append(d)
        except:
            print("LOGGER ERROR")

    def getEvents(self):
        #return logged events and clear the storage
        k = list(self.keys)
        m = list(self.mice)
        self.keys = []
        self.mice = []
        return k,m
if __name__ == "__main__":
    #for testing
    e = EventLogger()
    time.sleep(60)
