#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from flask import Flask, render_template
from flask_ask import Ask, statement

#updated to remove global variables

class Intents(object):
    def __init__():
        startRacePub = rospy.Publisher("maze", Bool, queue_size=1000)
        app = Flask(__name__)
        ask = Ask(app, '/')
        
    def startServer(self, debug):
        self.app.run(debug)
    
    #gets called when a RunRace intent is recieved from alexa 
    @ask.intent('RunRace')
    def getState(state):
        msg = Bool() 
        if state == "start":
            msg.data = True
        else:
            msg.data = False
            
            response = render_template("mazeResponse", state = state)

        try:
            startRacePub.publish(msg)
        except rospy.ROSInterruptException:
            pass
            
        return statement(response).simple_card("maze", response)

def setup():
    rospy.init_node('StringPublisher', anonymous=True)
    intents = Intents(debug=True)

if __name__ == "__main__":
    setup()

