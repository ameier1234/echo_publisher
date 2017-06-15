#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from flask import Flask, request, render_template
from flask_ask import Ask, statement

#updated to remove global variables
app = Flask(__name__)
ask = Ask(app, '/')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RunTimeError('Not running with werkzeug')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'server shutdown'

rospy.on_shutdown(shutdown)

class Intents(object):
    startRacePub = rospy.Publisher("maze", Bool, queue_size=1000)
        
    
    #gets called when a RunRace intent is recieved from alexa
    global ask 
    @ask.intent('RunRace')
    def getState(state):
        msg = Bool() 
        if state == "start":
            msg.data = True
        else:
            msg.data = False
            
        response = render_template("mazeResponse", state = state)

        try:
            Intents.startRacePub.publish(msg)
        except rospy.ROSInterruptException:
            pass
            
        return statement(response).simple_card("maze", response)

def setup():
    rospy.init_node('StringPublisher', anonymous=True)
    intents = Intents()
    app.run(debug=True)

if __name__ == "__main__":
    setup()

