#!/usr/bin/env python
import math
import rospy
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler

def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

def get_imu_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)

def get_gps_coordinates(msg):
    global latitude, longitude
    latitude = msg.latitude
    longitude = msg.longitude
    #print(msg.latitude, msg.longitude)

def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance
    R = 6378.137 # Radius of earth in km
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c * 1000 # in meters

    # Calculate heading
    y = math.sin(dLon) * math.cos(dLon)
    x = math.cos(lat1 * math.pi / 180) * math.sin(lat2 * math.pi / 180) - math.sin(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.cos(dLon)
    bearing = -math.atan2(y,x)

    return d, bearing

latitude, longitude = 0, 0
roll, pitch, yaw = 0, 0, 0

rospy.init_node('gps_waypoint_follower')

#sub_odom = rospy.Subscriber ('/odom', Odometry, get_rotation)
sub_odom = rospy.Subscriber ('/imu/data', Imu, get_imu_rotation)
sub_gps = rospy.Subscriber ('/navsat/fix', NavSatFix, get_gps_coordinates)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

rate = rospy.Rate(10)

rospy.loginfo("GPS waypoint follower node has started!")

# Example next waypoint [latitude, longitude]
next_waypoint = [47.47908802923231, 19.057747190129973]

cmd_vel = Twist()
cmd_vel.linear.x = 0
cmd_vel.angular.z = 0

while not rospy.is_shutdown():
    distance, bearing = haversine(latitude, longitude, next_waypoint[0], next_waypoint[1])
    rospy.loginfo("Distance: %.3f m, heading error: %.3f rad." % (distance, bearing - yaw))

    # Heading error, threshold is 0.1 rad
    if abs(bearing - yaw) > 0.1:
        # Only rotate in place if there is any heading error
        cmd_vel.linear.x = 0

        if bearing < yaw:
            cmd_vel.angular.z = -0.4
        else:
            cmd_vel.angular.z = 0.4
    else:
        # Only straight driving, no curves
        cmd_vel.angular.z = 0
        # Distance error, threshold is 0.2m
        if distance > 0.2:
            cmd_vel.linear.x = 0.5
        else:
            cmd_vel.linear.x = 0
            rospy.loginfo("Target waypoint reached!")

    pub.publish(cmd_vel)
    rate.sleep()

    