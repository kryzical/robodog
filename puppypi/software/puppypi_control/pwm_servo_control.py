#!/usr/bin/env python3
import os
import sys
import time
import json
import threading
from ros_robot_controller_sdk import *

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

class PWMServoControl:
    def __init__(self, board, time_out=100):
        self.board = board
        self.time_out = time_out
        self.pwm_servo_deviation_path = '/home/ubuntu/software/puppypi_control/servo_deviation.json'
        self.pwm_servo_duty_now = {}
        self.pwm_servo_threshold = {}
        self.pwm_servo_deviation = {}
        self.lock = threading.Lock()
        self.setDevBySelf = False

        for id in range(1,12):
            self.pwm_servo_duty_now[id] = 0
            self.pwm_servo_threshold[id] = {'min':500,'max':2500}
            self.pwm_servo_deviation[id] = 0

        try:
            with open(self.pwm_servo_deviation_path, 'r') as f:
                d = json.load(f)
                for key in d:
                    self.pwm_servo_deviation[int(key)] = d[key]
                    self.board.pwm_servo_set_offset(int(key),d[key])
                    
        except:
            with open(self.pwm_servo_deviation_path, 'w') as f:
                json.dump(self.pwm_servo_deviation, f)
        
    def setPulse(self, servo_id, pulse, use_time):
        if pulse < 500 or pulse > 2500:
            print("Angle is out of range")
            return False
        if pulse < self.pwm_servo_threshold[servo_id]['min']:pulse = self.pwm_servo_threshold[servo_id]['min']
        if pulse > self.pwm_servo_threshold[servo_id]['max']:pulse = self.pwm_servo_threshold[servo_id]['max']
        if use_time < 0:use_time = 0
        if use_time > 30000:use_time = 30000
          
        if pulse < 500:pulse=500
        elif pulse > 2500:pulse = 2500
        self.pwm_servo_duty_now[servo_id] = pulse
        self.board.pwm_servo_set_position(use_time/1000, [[servo_id, pulse]])

    def setThreshold(self, servo_id, min,max):
        if min < 500 or max > 2500:
            return False
        self.pwm_servo_threshold[servo_id] = {'min':min,'max':max}

    def setDeviation(self, servo_id, d):
        if d >= -100 and d <= 100:
            with self.lock:
                self.setDevBySelf = True
                self.pwm_servo_deviation[servo_id] = d
                self.board.pwm_servo_set_offset(servo_id,d)
        else:print("Deviation is out of range")
    
    def getDeviation(self, servo_id):
        return self.pwm_servo_deviation[servo_id]

    def saveDeviation(self):
        with self.lock:
            with open(self.pwm_servo_deviation_path, 'w') as f:
                json.dump(self.pwm_servo_deviation, f)
    
    def updatePulse(self, servo_id):
        if servo_id == -1:# all ids
            for id in range(1,12):
                try:
                    self.pwm_servo_duty_now[id] = self.board.pwm_servo_read_position(id) - self.pwm_servo_deviation[id]
                except:
                    self.pwm_servo_duty_now[id] = 0
        else:
            try:
                self.pwm_servo_duty_now[servo_id] = self.board.pwm_servo_read_position(servo_id) - self.pwm_servo_deviation[servo_id]
            except:
                self.pwm_servo_duty_now[servo_id] = 0

    def unload(self, servo_id):
        self.board.pwm_servo_set_position(0.01, [[servo_id, 0]])


    

