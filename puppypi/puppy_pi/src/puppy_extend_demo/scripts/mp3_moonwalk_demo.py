#!/usr/bin/env python3
# coding=utf8
# 第8章 ROS机器狗拓展课程\4.传感器开发课程\第7课 MP3模块实验(8.ROS Robot Expanded Course\4.Sensor Development Course\Lesson 7 MP3 Module)
import os
import sys
import math
import rospy
import sensor.MP3 as MP3
from std_msgs.msg import *
from puppy_control.srv import SetRunActionName
from puppy_control.msg import Velocity, Pose, Gait

print('''
**********************************************************
******************功能:MP3模块例程(function: MP3 module routine)*************************
**********************************************************
----------------------------------------------------------
Official website:https://www.hiwonder.com
Online mall:https://hiwonder.tmall.com
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！(press Ctrl+C to close the program, please try multiple times if fail)
----------------------------------------------------------
''')

PuppyPose = {'roll':math.radians(0), 'pitch':math.radians(0), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}
# stance_x：4条腿在x轴上额外分开的距离，单位cm(the distance extra apart for each of the four legs on the X-axis, measured in centimeters)
# stance_y：4条腿在y轴上额外分开的距离，单位cm(the distance extra apart for each of the four legs on the Y-axis, measured in centimeters)
# x_shift: 4条腿在x轴上同向移动的距离，越小，走路越前倾，越大越后仰,通过调节x_shift可以调节小狗走路的平衡，单位cm(the distance traveled by the four legs along the x-axis determines the degree of forward or backward tilt during walking: smaller distances lead to more forward tilt, while larger distances result in more backward tilt. Adjusting the x_shift parameter can help maintain balance during the dog's movement, measured in centimeters)
# height： 狗的高度，脚尖到大腿转动轴的垂直距离，单位cm(the height of the dog, measured from the toe to the axis  of rotation of the thigh, is in centimeters)
# pitch： 狗身体的俯仰角，单位弧度(the pitch angle of the dog's body, measured in radians)


GaitConfig = {'overlap_time':0.3, 'swing_time':0.2, 'clearance_time':0.0, 'z_clearance':5}
# overlap_time:4脚全部着地的时间，单位秒(the time when all four legs touch the ground, measured in seconds)
# swing_time：2脚离地时间，单位秒(the time duration when legs are off the ground, measured in second)
# clearance_time：前后脚间隔时间，单位秒(the time interval between the front and rear legs, measured in seconds)
# z_clearance：走路时，脚抬高的距离，单位cm(the distance the paw needs to be raised during walking, measured in centimeters)

# 多轴联动(multi-axis linkage)
def linkage(times =1):
    # times:循环次数(number of iterations)
    for i in range(0,15,1):
        PuppyPose = {'roll':math.radians(i), 'pitch':math.radians(0), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}
        PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift'],
            height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 30)
        rospy.sleep(0.03)
    for i in range(0,15,1):
        PuppyPose = {'roll':math.radians(15), 'pitch':math.radians(i), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}
        PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift'],
            height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 30)
        rospy.sleep(0.03)
        
    for s in range(times):
        for i in range(15,-15,-1):
            PuppyPose = {'roll':math.radians(i), 'pitch':math.radians(15), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}
            PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift'],
                height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 30)
            rospy.sleep(0.03)
        for i in range(15,-15,-1):
            PuppyPose = {'roll':math.radians(-15), 'pitch':math.radians(i), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}
            PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift'],
                height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 30)
            rospy.sleep(0.03)
             
        for i in range(-15,15,1):
            PuppyPose = {'roll':math.radians(i), 'pitch':math.radians(-15), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}
            PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift'],
                height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 30)
            rospy.sleep(0.03)
        for i in range(-15,15,1):
            PuppyPose = {'roll':math.radians(15), 'pitch':math.radians(i), 'yaw':0.000, 'height':-10, 'x_shift':-0.5, 'stance_x':0, 'stance_y':0}
            PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift'],
                height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 30)
            rospy.sleep(0.03)
            

# 关闭检测函数(turn off detection function)
run_st = True
def Stop():
    global run_st
    run_st = False
    print('关闭中...')
    mp3.pause()
    runActionGroup_srv('stand.d6ac',True)
    PuppyVelocityPub.publish(x=0, y=0, yaw_rate=0)
    
            
if __name__ == "__main__":
    addr = 0x7b #传感器iic地址(sensor I2C address)
    mp3 = MP3.MP3(addr)
    mp3.volume(30) #设置音量为20，注意在播放前设置(set the volume to 20, note that set before playback)
    mp3.playNum(25) #播放歌曲3(play song number 3)
    
    mp3.play() #播放(play)
    # 初始化节点(initialization node)
    rospy.init_node('mp3_moonwalk_demo')
    rospy.on_shutdown(Stop)
    
    PuppyPosePub = rospy.Publisher('/puppy_control/pose', Pose, queue_size=1)
    PuppyGaitConfigPub = rospy.Publisher('/puppy_control/gait', Gait, queue_size=1)
    PuppyVelocityPub = rospy.Publisher('/puppy_control/velocity', Velocity, queue_size=1)
    runActionGroup_srv = rospy.ServiceProxy('/puppy_control/runActionGroup', SetRunActionName)
    rospy.sleep(0.3) # 延时一会(delay for a second)
    # 机器狗站立(the robot dog stands up)
    PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift'],
        height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 500)
    
    rospy.sleep(0.5)
    PuppyGaitConfigPub.publish(overlap_time = GaitConfig['overlap_time'], swing_time = GaitConfig['swing_time']
                    , clearance_time = GaitConfig['clearance_time'], z_clearance = GaitConfig['z_clearance'])
    
    # 原地踏步(stepping in place)
    PuppyVelocityPub.publish(x=0.01, y=0, yaw_rate=0) 
    rospy.sleep(3)
    PuppyVelocityPub.publish(x=0, y=0, yaw_rate=0)
    rospy.sleep(1)
    
    # 多轴联动(multi-axis linkage)
    linkage(2) 
    # 机器狗站立(robot dog stands up)
    PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift'],
        height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 500)
    rospy.sleep(0.5)
    
    # 向前走(move forward)
    PuppyVelocityPub.publish(x=5, y=0, yaw_rate=0) 
    rospy.sleep(3)
    
    PuppyVelocityPub.publish(x=-5, y=0, yaw_rate=0) 
    rospy.sleep(2)
    # 向后走(walk backward)
    PuppyVelocityPub.publish(x=0, y=0, yaw_rate=0)
    rospy.sleep(1)
    
    # 执行滑步动作组(perform the sliding step action group)
    runActionGroup_srv('moonwalk.d6ac',True)
    runActionGroup_srv('moonwalk.d6ac',True)
    rospy.sleep(0.5)
    
    # 机器狗站立(robot dog stands up)
    PuppyPosePub.publish(stance_x=PuppyPose['stance_x'], stance_y=PuppyPose['stance_y'], x_shift=PuppyPose['x_shift']
            ,height=PuppyPose['height'], roll=PuppyPose['roll'], pitch=PuppyPose['pitch'], yaw=PuppyPose['yaw'], run_time = 500)
    rospy.sleep(0.5)
    # 向前走(move forward)
    PuppyVelocityPub.publish(x=5, y=0, yaw_rate=0) 
    rospy.sleep(5)
    # 原地踏步(stepping in place)
    PuppyVelocityPub.publish(x=0.01, y=0, yaw_rate=0) 
    rospy.sleep(3)
    PuppyVelocityPub.publish(x=0, y=0, yaw_rate=0)
    rospy.sleep(1)
    
    
    
            