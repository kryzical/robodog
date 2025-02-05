#!/usr/bin/python3
#coding=utf8
# 第8章 ROS机器狗拓展课程\4.传感器开发课程\第5课 语音识别传感器实验(8. ROS Robot Expanded Course\4.Sensor Development Course\Lesson 5 Voice Recognition Sensor)
import os
import sys
import rospy
import sensor.ASR as ASR
from ros_robot_controller.msg import RGBState, RGBsState
from std_msgs.msg import *

print('''
**********************************************************
*******************功能:语音识别例程(function: voice recognition routine)************************
**********************************************************
----------------------------------------------------------
Official website:https://www.hiwonder.com
Online mall:https://hiwonder.tmall.com
----------------------------------------------------------
Tips:
 * 按下Ctrl+C可关闭此次程序运行，若失败请多次尝试！(press Ctrl+C to close the program, please try multiple times if fail)
----------------------------------------------------------
''')

# 关闭RGB彩灯(turn off color light)
def turn_off_rgb():
    led1 = RGBState()
    led1.id = 1
    led1.r = 0
    led1.g = 0
    led1.b = 0
    led2 = RGBState()
    led2.id = 2
    led2.r = 0
    led2.g = 0
    led2.b = 0
    msg = RGBsState()
    msg.data = [led1,led2]
    rgb_pub.publish(msg)
    rospy.sleep(0.01)

# 设置RGB彩灯显示(set the RGB color light to display)
def set_rgb_show(r,g,b):
    led1 = RGBState()
    led1.id = 1
    led1.r = r
    led1.g = g
    led1.b = b
    led2 = RGBState()
    led2.id = 2
    led2.r = r
    led2.g = g
    led2.b = b
    msg = RGBsState()
    msg.data = [led1,led2]
    rgb_pub.publish(msg)
    rospy.sleep(0.01)

# 关闭检测函数(turn off detection function)
run_st = True
def Stop():
    global run_st
    run_st = False
    turn_off_rgb()
    print('关闭中...')


if __name__ == '__main__':
    # 语音识别模块初始化(voice recognition module initialization)
    asr = ASR.ASR()
    asr.getResult()
    asr.eraseWords()
    #1：循环识别模式。状态灯常亮（默认模式）(1: Loop recognition mode. The status light remains constantly on (default mode))
    #2：口令模式，以第一个词条为口令。状态灯常灭，当识别到口令词时常亮，等待识别到新的语音,并且读取识别结果后即灭掉(2: Password mode, using the first word as the password. The status light remains off; when the password is recognized, it stays on until a new voice is recognized, then turns off after reading the recognition result)
    #3：按键模式，按下开始识别，不按不识别。支持掉电保存。状态灯随按键按下而亮起，不按不亮(3: Button mode, recognition starts when the button is pressed, and stops when released. Supports power-off memory. The status light lights up when the button is pressed and goes off when released)
    asr.setMode(2)
    #添加的词条(added entry)
    asr.addWords(1, 'kai shi')
    asr.addWords(2, 'hong se')
    asr.addWords(3, 'lv se')
    asr.addWords(4, 'lan se')
    
    # 初始化节点(initialization node)
    rospy.init_node('ASR_detect_demo')
    rospy.on_shutdown(Stop)
    rgb_pub = rospy.Publisher('/ros_robot_controller/set_rgb', RGBsState, queue_size=1)
    rospy.sleep(0.2) # 延时一会，等待订阅生效(wait for a moment to allow the subscription to take effect)
    
    while run_st:
        data = asr.getResult()
        if data:
            print("result:", data)
            if data == 2:
                set_rgb_show(255,0,0) #红色(red)
                rospy.sleep(0.1)
                
            if data == 3:
                set_rgb_show(0,255,0) #绿色(green)
                rospy.sleep(0.1)
                
            if data == 4:
                set_rgb_show(0,0,255) #蓝色(blue)
                rospy.sleep(0.1)
                
        elif data is None:
            print('Sensor not connected!')
            break
            
            
        
        
    
