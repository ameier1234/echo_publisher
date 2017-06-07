#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from flask import Flask, render_template
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')
pub = rospy.Publisher("maze", Bool, queue_size=1000)


@ask.intent('RunRace')
def getString(state):
    msg = Bool() 
    if state == "start":
        msg.data = True
    else:
        msg.data = False
    

    try:
        response = render_template("mazeResponse", state = state)
    except e:
        rospy.loginfo(e)


    try:
        pub.publish(msg)
    except rospy.ROSInterruptException:
        pass
    return statement(response).simple_card("maze", response)

def setup():
   # pub = rospy.Publisher("StringPublisher", String, queue_size=1000)
    rospy.init_node('StringPublisher', anonymous=True)

if __name__ == "__main__":
    setup()
    app.run(debug=True)
