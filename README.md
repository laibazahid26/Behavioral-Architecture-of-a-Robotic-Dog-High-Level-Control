# exp_rob_assignment_1

######Introduction: 

In this assignment we implemented and simulated three behaviors of MIRO Robot. Those three behaviors are:

    • Normal 
    • Sleep  
    • Play  

These three behaviors were implemented inside a finite state machine which was built using ROS library called SMACH. This node is named as assignment.py file. Apart from this node, one more node is built which is called as SpeakInteraction.cpp and this node simulates the speak interaction of the user with the robot. 

######Software Architecture:

Below is the image of my architecture. 

![alt text](https://github.com/laibazahid26/exp_rob_assignment_1/blob/main/architecture.png?raw=true)


The audio is fed to the ROS node “Speech Processor”. After processing and making sure that the audio provided does correspond to the ‘play’ command, we set the ‘playflag’ to 1 inside the ROS Parameter Server. This ‘playflag’ is then used by the finite state machine, which lies inside the “Command Manager” node, to jump to the ‘Play’ behavior. Notice that “Rigid Body Detector” node takes data from the camera. The camera detects the human arm posture and to find the coordinates of that arm posture, gives the data do “Gesture Processor” node.  The “Gesture Processor” node then passes a vector to “The Command Manager” node. The vector contains the estimated x and y coordinates of the point to which the user’s hand is pointing to.  The “Command Manger” node then finally gives the target to the “Path Planner” node and the “Path Planner” node after knowing the current position of the robot and the target, publishes a complete trajectory which the robot needs to follow. Finally, the “Robot Controller” node generates velocity commands one by one to reach to each vector.  

######List of messages of the proposed Architecture:

    1) The Speech Processor node produces a single string, which in our case should be ‘play’. If it’s some other string then nothing happens. 
    2) ROS Paramter Server sets the playflag, that is playflag is set to 1, if the ‘play’ command was given, otherwise this flag stays 0.
    3) The Rigid Body Detector node provides the position of the hand in the scenario.  
    4) The Gesture Processor Node gives the estimated x and y coordinates of the point to which the user’s hand is pointing to, which means this message is a 2D vector.
    5) The Command Manager node gives a target which is the final location of the robot and this target is a 2D vector.
    6) Path planner node provides a vector of vector. Which means it contains all the 2D points which the robot needs to follow to reach to the final destination. 
    7) Robot Controller node will generate velocity commands to reach to each vector and it will have type Twist. 

######State Diagram:

Below is the state diagram of this architecture. This finite state machine lies inside the command manager node of my architecture.

 ![alt text](https://github.com/laibazahid26/exp_rob_assignment_1/blob/main/finite%20state%20machine.png?raw=true)

As can be seen, there are three states, i.e. Normal, Sleep and, Play. The robot comes to life in being in the Normal state. Since we were required to ‘decide’ upon when the robot goes to sleep, I decided that  whenever the robot finishes the normal behavior ‘and’ there is no speech command, then the robot goes to the Sleep behavior. I also decided that the robot will come out of the Sleep behavior when it finishes its sleeping time, i.e. after finishing sleep time, the robot goes back to the Normal state. 

On the other hand, if the robot is in the Normal state and there comes a speech command: Play, then the robot enters in the Play behavior (not in the Sleep behavior, because in my architecture, Play behavior has priority over Sleep behavior). After finishing the Play behavior, the robot goes back to the Normal behavior. 

######Packages and File List:
I created a package named smach_tutorial. Inside smach_tutorial lie two folders named ‘src’ and ‘launch’. Folder src contains the two nodes for this assignment and the launch folder contains the .launch file. The execution of .launch file will run the complete project. Inside the src folder of the smach_tutorial resides two nodes named assignment.py and SpeakInteraction.cpp. 

######Installation and Running Procedure:

    • Download the folder named smach_tutorial. 
    • Place this folder inside your workspace. 
    • Go in your workspace using terminal and then do a catkin_make.
    • In the previous step you were in your workspace. Now move to the src foder of your smach_tutorial package and give running permissions to it by writing the following command:
                                  chmod +x assignment.py
    • Now, we are in the position to run the assignment completely. We can do it by launching the .launch file by running the following command on the terminal. 
		              roslaunch smach_tutorial smachlaunch.launch 

After running the above command, you will see a total of two terminals opened. The first terminal shows the complete simulation of the robot. Whereas, the second terminal simulates the speak behavior.  The user has the liberty to type ‘play’ anytime in that terminal. This writing of play in the second terminal let’s the robot go into Play behavior and then input the x and y coordinate (the gesture of the human) in the first terminal. 

######Working Hypothesis and Environment: 

This package simulates the Normal, Sleep and, Play behavior of the MIRO robot in the ROS environment. SMACH library was used to implement the finite state machine. These behaviors are implemented as classes in the assignment.py file. On certain outcomes, the transition from one state/behavior to the other state happens.  

The important part of this architecture is randomizing various tasks performed by the robot. So, for example in Normal behavior the robot is supposed to move randomly. The question arises that how many times does the robot moves randomly? The answer is that, it does it randomly. In my architecture, this random value comes between 2-4 times. There are other functionalities as well which have been made random using the same logic, for example, how many times should the robot ask for coordinates to the user? Same logic is used for dealing with this question as well. 

Second important part is scaling the velocity of the simulation, i.e. with what speed does the robot goes to the desired location? This could be set via ros parameter server inside the launch file.   

SpeakInteraction.cpp node allows the user to input ‘play’ anytime and then the robot enters in the Play behavior while continuously asking for the coordinates it needs to go to back and forth after coming near to the user.

######System’s limitations:

    1. If the robot has gone into the sleep behavior and at exactly that point the play command is given, the robot first finishes the complete Sleep time and only then the Play behavior will be implemented. 
    2. There is no way to come out of the Play behavior unless the Play behavior finishes. Only after finishing the Play behavior the robot goes back to the Normal behavior. 
    3. The time to reach from point A to B is same point A to C. Irrespective of the two different distances. Waiting time is same because it is set only at the launch file. 
    4. Error handling is not done in the system.

######Possible technical Improvements:

In my architecture, when the user inputs ‘play’ in the terminal, the ‘playflag’ which is the parameter of the ros parameter server gets set and then we check in assignment.py file that if this parameter is set, we jump to the Play behavior. 

I think, another way of doing this in a more modular and scalable way could be to use Publish and Subscribe model. Using ROS parameter server, the playflag is set to 1 and then after reading this value and taking the desired actions on this value this parameter is set back to 0. Here the problem is that what if some other class also wanted to use that same initial value 1? As the program continues to flow, when this value will be reached to some other class or function, there are great chances that this value would have been modified many times. But, if we had used Publish and Subscribe model, whatever the message would be subscribed, all the functions will be using that same value.   

######Authors and Contacts:

I collaborated with a fellow colleague during designing the architecture of this robot and then we also collaborated in coding for that architecture. We initially came up with two architectures but then discarded one architecture because of a lot of technical limitations in it. The biggest limitation in that architecture was that in its Normal Behavior, the program continuously prompted the user with statement ‘Do you want to play with me?’. And then when the user inputs ‘no’, the robot would then would go to some desired coordinate. After having reached that coordinate it would prompt the user again with the same question. This is how, the whole Normal behavior was taking place. We considered this as a big limitation and discarded that architecture. 

The commenting with doxygen, readme file and making the github repository was done individually.  
In any case, I will mention the names and contacts of both of us. 

Author 1: Laiba Zahid (S4853477)					email ID: laibazahid26@gmail.com
Author 2: Syed Muhammad Raza Rizvi (S4853521)		email ID: smrazarizvi96@gmail.com
 


  


  
