#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from flask import Flask, render_template
from flask_ask import Ask, statement

app = Flask(__name__)
ask = Ask(app, '/')
pub = rospy.Publisher("StringPublisher", String, queue_size=1000)


@ask.intent('GetStringIntent')
def getString(string):
    text = render_template("publish", string=string)
    
    #now try and initialize a rospublisher with the input string
    try:
        pub.publish(string)
    except rospy.ROSInterruptException:
        pass
    return statement(text).simple_card("Publish", text)

def setup():
   # pub = rospy.Publisher("StringPublisher", String, queue_size=1000)
    rospy.init_node('StringPublisher', anonymous=True)

if __name__ == "__main__":
    setup()
    app.run(debug=True)
