#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random

# INSTALLATION
# - create ROS package in your workspace:
#          $ catkin_create_pkg smach_tutorial std_msgs rospy
# - move this file to the 'smach_tutorial/scr' folder and give running permissions to it with
#          $ chmod +x assignment.py
# - run the 'roscore' and then you can run the state machine with
#          $ rosrun smach_tutorial assignment.py
# - install the visualiser using
#          $ sudo apt-get install ros-melodic-smach-viewer
# - run the visualiser with
#          $ rosrun smach_viewer smach_viewer.py

""" In this node a finite state machine has been implemented which simulates the 
three behavior named the Normal, Sleep and Play behavior. """

""" declaration of the global variables"""
home_x= 1
home_y= 1
robot_x= home_x
robot_y= home_y
person_x= 25
person_y= 25

from std_msgs.msg import String

# define state Play
class Play(smach.State):
    """ 
    This class simulates the Play behavior of the robot 
    """
    """ 
    for-loop is used to simulate the movement cycles of the 
    robot for randomized variable 'i' times 
    """
    """ 
    this piece of code: time.sleep(rospy.get_param("velocity"))
    helps us scale the velocity of the simulation. Here, we used ros 
    parameter service whose parameter 'velocity' is set in the 
    launch file
    """
    """ 
    time.sleep(rospy.get_param("velocity")) gets its argument from 
    the ros parameter server. This parameter is named as 'velocity' 
    and is set in the .launch file. This line of code helps us to 
    scale the velocity of the simulation. Right now this paramter 
    is set to a sleep time of 3 seconds in .launch file
    """
    
    def __init__(self): 
        """ 
        The constructor/ the initialiser
        """
        # initialisation function, it should not wait
        smach.State.__init__(self, 
                             outcomes=['after finishing play time'])
        
    def execute(self, userdata):
        """ 
        When the user inputs the 'play' command, Play behavior will
 	run. The functionality of the play behavior is implemented in this
	function. random.randint() function is used to make sure that the 
	robot asks for the gesture for 2 to 4 times 
        """
      
        rospy.loginfo('Executing state PLAY')
        
	i = random.randint(2,4)	
	for x in range(i):
		
		robot_x = person_x-1
		robot_y = person_y-1
		time.sleep(rospy.get_param("velocity")) 
		
		print 'Reached Near Person:  (',robot_x,',',robot_y,')'
		print 'Please show with gesture where do you want me to go in x 		       coordinate:  ' 	
		
		""" 
                taking x coordinate from the user as input
                """		
		gesture_x = raw_input() 
		
		print 'Please show with gesture where do you want me to go in y 		       coordinate:  '
		
		""" 
                taking y coordinate from the user as input
                """
		gesture_y = raw_input() 
		
		robot_x = int(gesture_x)
		robot_y = int(gesture_y)

		time.sleep(rospy.get_param("velocity"))
		print 'Reached at pointed position:  (',robot_x,',',robot_y,')'
	
        return 'after finishing play time'

# define state Sleep
class Sleep(smach.State):
    """ 
    This class simulates the Sleep behavior of the robot 
    """
    """ 
    time.sleep(rospy.get_param("velocity")) gets its argument from 
    the ros parameter server. This parameter is named as 'velocity' 
    and is set in the .launch file. This line of code helps us to 
    scale the velocity of the simulation. Right now this paramter 
    is set to a sleep time of 3 seconds in .launch file
    """
    
    def __init__(self):
        """ 
        The constructor/ the initialiser
        """
        # initialisation function, it should not wait
        smach.State.__init__(self, 
                             outcomes=['after finishing sleep time'])
        
    def execute(self, userdata):
        """ 
        This function implements the sleep functionality
        """
        # function called when exiting from the node, it can be blacking
        rospy.loginfo('Executing state SLEEP')
       
	time.sleep(rospy.get_param("velocity"))
        robot_x= home_x;
	robot_y= home_y;
        print 'Reached Home:  (',robot_x,',',robot_y,')'
	print 'Sleeping...'
	time.sleep(rospy.get_param("velocity"))
        return 'after finishing sleep time'
    

# define state Normal
class Normal(smach.State):
    """ 
    This class simulates the Normal behavior of the robot 
    """
    """ 
    for-loop is used to simulate the movement cycles of the 
    robot for randomized variable 'i' times 
    """
    """
    checker variable checks the boolean status of the parameter
    named 'playflag'. If this parameter is set, we jump to play 
    behavior after setting the value of this paramater back to 0.     		
    This playflag is set inside file 'SpeakInteraction.cpp'
    when the voice command 'play' is received. If play command 
    is not provided, Normal behavior is performed by the robot 
    """
    """ 
    randmoly the x and y coordinates will be generated for 
    implementing the Normal behavior of the robot
    """
    """ 
    time.sleep() gets its argument from the ros parameter server.
    This parameter is named as 'velocity' and is set in the .launch 
    file. This line of code helps us to scale the velocity of the 
    simulation. Right now this paramter is set to a sleep time of     		
    3 seconds in .launch file
    """

    def __init__(self):
        """ 
        The constructor/ the initialiser
        """
        smach.State.__init__(self, 
                             outcomes=['after finishing normal behavior',
 				       'speech command:play'])

    def execute(self, userdata):
        while not rospy.is_shutdown():  
   
	    rospy.loginfo('Executing state NORMAL')
	    i = random.randint(2,5)
            

	    for x in range(i):
	    	checker = rospy.get_param("playflag")
	    	if (checker == 1):
	        	rospy.set_param("playflag", 0)
			return 'speech command:play'

	    	robot_x= random.randint(1,10)
	    	robot_y= random.randint(1,10)

	    	time.sleep(rospy.get_param("velocity"))
	    	print 'Reached Destination:  (',robot_x,',',robot_y,')'
	    checker = rospy.get_param("playflag")
	    if (checker == 1):
	        rospy.set_param("playflag", 0)
		return 'speech command:play'
	    return 'after finishing normal behavior'

        
def main():
    """ 
    a smach state machine is created here which is named as sm and 
    has outcome 'container_interface'. This outcome can we used by
    some other finite state machine or some node 
    """
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['container_interface'])
    
    # Open the container
    with sm:
        # Add states to the container

        smach.StateMachine.add('NORMAL', Normal(), 
                               transitions={'after finishing normal behavior':'SLEEP',
					    'speech command:play': 'PLAY'})
        smach.StateMachine.add('SLEEP', Sleep(), 
                               transitions={'after finishing sleep time':'NORMAL'})
	smach.StateMachine.add('PLAY', Play(), 
                               transitions={'after finishing play time':'NORMAL'})


    
    # Create and start the introspection server for visualization. We 
    # can visualize this is smach viewer
    
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    
    # Execute the state machine 
    
    outcome = sm.execute()

     
    # Wait for ctrl-c to stop the application 
    
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
