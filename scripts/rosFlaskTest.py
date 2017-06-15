#!/usr/bin/env python
import os
import sys
import signal
from multiprocessing import Process, Pipe
import rospy
from std_msgs.msg import String
from flask import Flask, request, render_template
from flask_ask import Ask, statement

##signal.signal(signal.SIGTERM, lambda signum, stack_frame: sys.exit(1))

app = Flask(__name__)
ask = Ask(app, '/')

class RosProcess(object):
    
    def __init__(self, ros_pipe):
        self.ros_pipe = ros_pipe
        self.stringPub = rospy.Publisher("String_Pub", String, queue_size=1000)
    
    def listen(self):
        isData = True
        while(isData):
            if(ros_pipe.poll(100)):
                obj = ros_pipe.recv()
                rospy.loginfo(type(obj))
                rospy.loginfo(type(obj) is String)
                if(obj == False):
                    isData = False
                else:
                    rospy.loginfo("publishing string")
                    self.stringPub.publish(obj)






class AskProcess(object):
    def __init__(self, ask_pipe):
        self.ask_pipe = ask_pipe

    global ask
    @ask.intent('getStringIntent')
    def getString(string):
        response = render_template('publish', string=string)
        s = String()
        s.data = string
        ask_pipe.send(s)
        
        return statement(response).simple_card("Publish", response)
        
    




def startRosProcess(ros_pipe):
    try:
        rospy.init_node('String_publisher')
        ros_process = RosProcess(ros_pipe)
        ros_process.listen()
    except KeyboardInterrupt:
    	return 'KeyboardInterrupt'
def startAskProcess(ask_pipe):
	try:
		ask_process = AskProcess(ask_pipe)
		app.run(debug=True)
	except KeyboardInterrupt:
		return 'KeyboardInterrupt'

if __name__ == "__main__":
    ask_pipe, ros_pipe = Pipe()

    #rospy.on_shutdown(ask_process.terminate)

    try:
    	ask_process = Process(target=startAskProcess, args=(ask_pipe,))
    	ros_process = Process(target=startRosProcess, args=(ros_pipe,))
    	ask_process.start()
    	ros_process.start()
    	ask_process.join()
    	ros_process.join()
    except KeyboardInterrupt:
    	print("Recieved KeyboardInterrupt")
    	os.system('kill -9 {}'.format(ros_process.pid))
    	os.system('kill -9 {}'.format(ask_process.pid))
    	#ros_process.terminate()
    	#ask_process.terminate()



    


