#include "ros/ros.h"
#include "std_msgs/String.h"
#include <string>
#include <iostream>
#include <fstream>

using namespace std;

int main(int argc, char **argv)
{	
  /** This node sets the prameter of ROS parameter
    * service, which we named as 'playflag'. Based 
    * on the value of this parameter certain behavior 
    * will run in assignment.py file */
  
  ros::init(argc, argv, "Speak"); 
  ros::NodeHandle n;

  n.setParam("playflag", 0); /** here the playflag has been set to zero */
  while (ros::ok())
  {
    std_msgs::String msg;
    cout << "Do you want to play with me? If yes, please write 'play' ";
    getline(cin, msg.data); /** taking input from the user from terminal */
	
    ROS_INFO("%s", msg.data.c_str());
    if(msg.data == "play")
    {
    	n.setParam("playflag", 1); /** if user inputs 'play' the parameter playflag will be set to 1 */ 

    }
  }

  return 0;
}
