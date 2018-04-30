# Focus Light
This repository contains code for University of Alberta, Winter 2018, CMPUT 660 final project.

Data used in this project was not included in this repository since it contains personal informations.

## Environment
The codes run in Python 3.

### Dependencies
	sneakysnek 0.1.1
    numpy 1.13.3
    requests 2.18.4
    pandas 0.21.0
    sklearn 0.19.1
Also, this application requires [ActivityWatch
](https://github.com/ActivityWatch/activitywatch) for monitoring active applications.
## How to run the code
1. Install [ActivityWatch
](https://github.com/ActivityWatch/activitywatch).
2. Follow this [link](https://www.developers.meethue.com/documentation/getting-started), create a user for controlling the  Philips Hue Lightbulb
3.  Change the `settings.config`:

     Change`USER` to the user you created.
     
     Change`LIGHT` to the light that you want to be controlled.
     
     Change`IP` to the IP address of your HUE hub.
     
     You should found those information in step 2.

	Change`RESOLUTION_WIDTH`,`RESOLUTION_HEIGHT` according to your screen resolution.
    
    Change `PORT` to the port for [ActivityWatch
](https://github.com/ActivityWatch/activitywatch), on default it is 5600.

4. In command line, start the application by run `stateManager.py` with Python 3. When program is running, enter q to quit.
	
5. Run `trainer.py` to train the model with new data collected.

## Architecture
```
 +---------------+                                        +--------------+
 |               |                                        |              |
 | ActivityWatch |                  +----------+          | trainer.py   |
 |               |                  |          |   Train  |              |
 +--+--+---------+                  | ML Model +<---------+ Train&Update |
    ^  |                            |          |          | ML Model     |
REST|  |                            +-+--+-----+          |              |
API |  |Window Events                 ^  |                +-----+--------+
    |  |                        Sample|  |Prediction            ^
    |  v                              |  v                      |Formatted Data
 +--+--+------------+            +----+--+-----------+          |
 |                  |            |                   +----------+
 | DataCollector.py +----------->+ stateManager.py   |            +------------------+
 |                  |  Raw Data  |                   |            |                  |
 +-----+------------+            | Change user state +----------->+ dataFormatter.py |
       ^                         | according to data |  Raw Data  |                  |
       |                         | collected.        |            | Extract Features |
       |Keyboard&Mouse Events    |                   +<-----------+                  |
       |                         +--------+----------+  Formatted +------------------+
       |                                  |                Data
  +----+-----------+                  REST|
  |                |                  API |
  | eventLogger.py |                      v
  |                |             +--------+-----------+
  +----------------+             |                    |
                                 | lightController.py |
                                 |                    |
                                 | Controls the state |
                                 | of HUE lightbulb   |
                                 +--------------------+

```
For more information, see the codes and comments.