from time import sleep
from adafruit_servokit import ServoKit
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


#initialize kit to channel for operation, will not need to do any other place
kit = ServoKit(channels=16)
#servo port
lf1 = 4
lf2 = 5
lr1 = 12
lr2 = 13

rf1 = 6
rf2 = 7
rr1 = 14
rr2 = 15

#LF1; front left upper 4
    #range 0(forward) 180 (backward)
#LF2; front left lower 5
    #range 0(extended) 180(in)
#RF1 6
    #range 0(backward) 180(forward)
#RF2 7
    #range 0(in) 180 (extended)
#LR1 12
    #range 0(forward) 180 (backward)
#lR2 13
    #range 0(extended) 180(in)
#RR1 14
    #range 0(backward) 180(forward)
#RR2 15
    #range 0(in) 180 (extended)

joint_names = [
    'lf1_joint', 'lf2_joint', 'lr1_joint', 'lr2_joint',
    'rf1_joint', 'rf2_joint', 'rr1_joint', 'rr2_joint'
]
servo_channels = {
    'lf1_joint': 4, 'lf2_joint': 5,
    'lr1_joint': 12, 'lr2_joint': 13,
    'rf1_joint': 6, 'rf2_joint': 7,
    'rr1_joint': 14, 'rr2_joint': 15
}

class JointStateBroadcaster(Node):
    def __init__(self):
        super().__init__('movement_joint_publisher')
        self.publisher_ = self.create_publisher(JointState, '/joint_states', 10)

    def publish_joint_states(self, angles):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = joint_names
        msg.position = [angles[name] * 3.14159 / 180 for name in joint_names]  # deg → rad
        self.publisher_.publish(msg)

# Initialize ROS2 before main loop
rclpy.init()
joint_pub = JointStateBroadcaster()

def publish_and_move(angles):
    """Set servo positions and publish joint states."""
    for name, angle in angles.items():
        kit.servo[servo_channels[name]].angle = angle
    joint_pub.publish_joint_states(angles)

def trot_forward():
    print("starting integrated trot...")

    angles = {
        'lf1_joint': 152, 'lf2_joint': 66,
        'lr1_joint': 152, 'lr2_joint': 66,
        'rf1_joint': 152, 'rf2_joint': 66,
        'rr1_joint': 152, 'rr2_joint': 66,
    }

    interval = 0.0001

    for _ in range(20):
        angles['rf2_joint'] -= 1
        angles['lr2_joint'] += 1
        publish_and_move(angles)
        angles['rf1_joint'] += 1
        angles['lr1_joint'] -= 1
        publish_and_move(angles)
        sleep(interval)

def trot_forward():
    lf1_a = 152 #152
    lf2_a = 66 #66
    lr1_a = 152 #152
    lr2_a = 66 #66
    ########
    rf1_a = 13 #13
    rf2_a = 96 #96
    rr1_a = 13 #13
    rr2_a = 96 #96
    interval_time =.00005 #.00005

#NOTES FOR SWING TIME, interval_time is fast enough and slow enough to have a fluid motion
    for i in range(1):
        #phase 1, swing rf lr########################
            #lift
            i = 40 #lr and rf dif
            j = 30 #lf and rr dif
            while(i >= 0 or j >= 0):
                if(i >= 0):
                    lr2_a += 1 #106
                    rf2_a -= 1 #56
                    kit.servo[lr2].angle = lr2_a
                    kit.servo[rf2].angle = rf2_a
                    i -= 1
                #move lf2 and rr2
                if(j >= 0):
                    rr2_a += 1 #126
                    lf2_a -=1 #36
                    kit.servo[rr2].angle = rr2_a
                    kit.servo[lf2].angle = lf2_a
                    j -= 1
                sleep(interval_time)
            sleep(interval_time)
            ########################
            #move rf and lr down(finish swing)
            i = 30 #rf1 and lr1 dif
            j = 40 #rf2 and lr2 dif
            while(i >= 0 or j >= 0):
                if(i >= 0):
                    rf1_a += 1 #30
                    lr1_a -= 1 #140
                    kit.servo[rf1].angle = rf1_a
                    kit.servo[lr1].angle = lr1_a
                    i -= 1
                if(j >= 0):
                    rf2_a += 1 #91
                    lr2_a -=1 #71
                    kit.servo[lr2].angle = lr2_a
                    kit.servo[rf2].angle = rf2_a
                    j -= 1
                sleep(interval_time)
        #pahse 2 swing lf rr
            print(f"lf1: {lf1_a} lf2: {lf2_a} rr1: {rr1_a} rr2: {rr2_a}")
            sleep(interval_time)
            i = 11 # lf1 and rr1 dif 11
            j = 30 # rf1 and lr1 dif
            k = 5 # rf2 and lr2 dif 5
            while(i >= 0 or j >= 0 or k >= 0):
                if(i >= 0):
                    lf1_a += 1
                    rr1_a -= 1
                    kit.servo[lf1].angle = lf1_a
                    kit.servo[rr1].angle = rr1_a
                    i-=1
                if(j >= 0):
                    rf1_a -= 1
                    lr1_a += 1
                    kit.servo[rf1].angle = rf1_a
                    kit.servo[lr1].angle = lr1_a
                    j-=1
                if(k >= 0):
                    rf2_a += 1 
                    lr2_a -= 1
                    kit.servo[rf2].angle = rf2_a
                    kit.servo[lr2].angle = lr2_a
                    k-=1
                sleep(interval_time)
            print("done ")
            # sleep(5)
            # retract lf2 and rr2
            i = 40 #lf2 and rr2 diff
            while(i >= 0):
                lf2_a += 1
                rr2_a -= 1
                kit.servo[lf2].angle = lf2_a
                kit.servo[rr2].angle = rr2_a
                i-=1
                sleep(interval_time)
            #swing lf1 and rr1 (return back to standing)
            i = 12 #lf1 and rr1 diff
            j = 10 #lf2 and rr2 diff
            k = 6  #lr2 and rf2 dif
            while(i > 0 or j > 0 or k > 0):
                if(i > 0):
                    lf1_a -= 1
                    rr1_a += 1
                    kit.servo[lf1].angle = lf1_a
                    kit.servo[rr1].angle = rr1_a
                    i-=1
                if(j > 0):
                    lf2_a -= 1
                    rr2_a += 1
                    kit.servo[lf2].angle = lf2_a
                    kit.servo[rr2].angle = rr2_a
                    j-=1
                if(k > 0):
                    lr2_a += 1
                    rf2_a -= 1
                    kit.servo[lr2].angle = lr2_a
                    kit.servo[rf2].angle = rf2_a
                    k -= 1
                sleep(interval_time)
    
    print(f"lf1: {lf1_a}, lf2: {lf2_a}, rf1 : {rf1_a}, rf2: {rf2_a}, lr1: {lr1_a}, lr2: {lr2_a}, rr1: {rr1_a}, rr2: {rr2_a}")

def walk_back():
    # Initial servo angles
    lf1_a = 152  # Left Front 1
    lf2_a = 66   # Left Front 2
    lr1_a = 152  # Left Rear 1
    lr2_a = 66   # Left Rear 2
    rf1_a = 13   # Right Front 1
    rf2_a = 96   # Right Front 2
    rr1_a = 13   # Right Rear 1
    rr2_a = 96   # Right Rear 2
    interval_time = 0.00005  # Time interval for smooth movement

    # Phase 1: Swing Left Rear (lr2) and Right Front (rf2)
    for i in range(1):
        # Lift the legs first
        i = 40  # Diff between lr2 and rf2
        j = 30  # Diff between lf2 and rr2
        while i >= 0 or j >= 0:
            if i >= 0:
                lr2_a -= 1  # Moving the rear leg in the opposite direction (reverse)
                rf2_a += 1  # Move right front backward
                kit.servo[lr2].angle = lr2_a
                kit.servo[rf2].angle = rf2_a
                i -= 1
            if j >= 0:
                rr2_a -= 1  # Move the rear right leg backward
                lf2_a += 1  # Move left front backward
                kit.servo[rr2].angle = rr2_a
                kit.servo[lf2].angle = lf2_a
                j -= 1
            sleep(interval_time)
        sleep(interval_time)

        # Lower the rf1, rf2, lr1, lr2 back down
        i = 30
        j = 40
        while i >= 0 or j >= 0:
            if i >= 0:
                rf1_a -= 1  # Move right front 1 servo down
                lr1_a += 1  # Move left rear 1 servo down
                kit.servo[rf1].angle = rf1_a
                kit.servo[lr1].angle = lr1_a
                i -= 1
            if j >= 0:
                rf2_a -= 1  # Move right front 2 servo down
                lr2_a += 1  # Move left rear 2 servo down
                kit.servo[lr2].angle = lr2_a
                kit.servo[rf2].angle = rf2_a
                j -= 1
            sleep(interval_time)

        # Phase 2: Swing Left Front (lf1) and Right Rear (rr1)
        print(f"lf1: {lf1_a} lf2: {lf2_a} rr1: {rr1_a} rr2: {rr2_a}")
        sleep(interval_time)
        i = 11  # Diff between lf1 and rr1
        j = 30  # Diff between rf1 and lr1
        k = 5   # Diff between rf2 and lr2
        while i >= 0 or j >= 0 or k >= 0:
            if i >= 0:
                lf1_a -= 1  # Left front 1 moves backward
                rr1_a += 1  # Right rear moves backward
                kit.servo[lf1].angle = lf1_a
                kit.servo[rr1].angle = rr1_a
                i -= 1
            if j >= 0:
                rf1_a += 1  # Move right front 1 backward
                lr1_a -= 1  # Move left rear 1 backward
                kit.servo[rf1].angle = rf1_a
                kit.servo[lr1].angle = lr1_a
                j -= 1
            if k >= 0:
                rf2_a -= 1  # Move right front 2 backward
                lr2_a += 1  # Move left rear 2 backward
                kit.servo[rf2].angle = rf2_a
                kit.servo[lr2].angle = lr2_a
                k -= 1
            sleep(interval_time)
        print("done ")

        # Retract left front (lf2) and right rear (rr2)
        i = 40
        while i >= 0:
            lf2_a -= 1  # Move left front 2 back
            rr2_a += 1  # Move right rear back
            kit.servo[lf2].angle = lf2_a
            kit.servo[rr2].angle = rr2_a
            i -= 1
            sleep(interval_time)

        # Final phase: Return to standing position (retract)
        i = 12
        j = 10
        k = 6
        while i > 0 or j > 0 or k > 0:
            if i > 0:
                lf1_a += 1  # Left front 1 goes back to normal
                rr1_a -= 1  # Right rear goes back to normal
                kit.servo[lf1].angle = lf1_a
                kit.servo[rr1].angle = rr1_a
                i -= 1
            if j > 0:
                lf2_a += 1  # Left front 2 goes back to normal
                rr2_a -= 1  # Right rear 2 goes back to normal
                kit.servo[lf2].angle = lf2_a
                kit.servo[rr2].angle = rr2_a
                j -= 1
            if k > 0:
                lr2_a -= 1  # Left rear 2 goes back to normal
                rf2_a += 1  # Right front 2 goes back to normal
                kit.servo[lr2].angle = lr2_a
                kit.servo[rf2].angle = rf2_a
                k -= 1
            sleep(interval_time)

    print(f"lf1: {lf1_a}, lf2: {lf2_a}, rf1 : {rf1_a}, rf2: {rf2_a}, lr1: {lr1_a}, lr2: {lr2_a}, rr1: {rr1_a}, rr2: {rr2_a}")

#turn left
def turn_left():
    lf1_a = 152 #152
    lf2_a = 66 #66
    lr1_a = 152 #152
    lr2_a = 66 #66
    ########
    rf1_a = 13 #13
    rf2_a = 96 #96
    rr1_a = 13 #13
    rr2_a = 96 #96
    interval_time =.0005 #.005
    
    #note right legs will be drag, left will be stationary
    i = 40
    while(i>0):
        rr2_a -= 1
        kit.servo[rr2].angle = rr2_a
        i -= 1
        sleep(interval_time)
    i = 40
    j = 60
    while(i>0 or j>0):
        if(i>0):
            rr1_a += 1
            kit.servo[rr1].angle = rr1_a
            i -= 1
        if(j>0):
            rr2_a += 1
            kit.servo[rr2].angle = rr2_a
            j -= 1
        sleep(interval_time)
    i = 40
    j = 20
    while(i>0):
        if(i>0):
            rr1_a -= 1
            kit.servo[rr1].angle = rr1_a
            i -= 1
        sleep(.005)
    while(j>0):
        rr2_a -= 1
        kit.servo[rr2].angle = rr2_a
        j -= 1
        sleep(interval_time)


    i = 40
    while(i>0):
        rf2_a -= 1
        kit.servo[rf2].angle = rf2_a
        i -= 1
        sleep(interval_time)
    i = 40
    j = 60
    while(i>0 or j>0):
        if(i>0):
            rf1_a += 1
            kit.servo[rf1].angle = rf1_a
            i -= 1
        if(j>0):
            rf2_a += 1
            kit.servo[rf2].angle = rf2_a
            j -= 1
        sleep(interval_time)
    i = 40
    j = 20
    while(i>0):
        if(i>0):
            rf1_a -= 1
            kit.servo[rf1].angle = rf1_a
            i -= 1
        sleep(.005)
    while(j>0):
        rf2_a -= 1
        kit.servo[rf2].angle = rf2_a
        j -= 1
        sleep(interval_time)

    print(f"lf1: {lf1_a}, lf2: {lf2_a}, rf1 : {rf1_a}, rf2: {rf2_a}, lr1: {lr1_a}, lr2: {lr2_a}, rr1: {rr1_a}, rr2: {rr2_a}")

def turn_right():
    lf1_a = 152 #152
    lf2_a = 66 #66
    lr1_a = 152 #152
    lr2_a = 66 #66
    ########
    rf1_a = 13 #13
    rf2_a = 96 #96
    rr1_a = 13 #13
    rr2_a = 96 #96
    interval_time =.0005 #.00005     #.00005
    #left legs will drag
    i = 40
    while(i>0):
        lr2_a += 1
        kit.servo[lr2].angle = lr2_a
        i -= 1
        sleep(interval_time)
    i = 50
    j = 70
    while(i>0 or j>0):
        if(i>0):
            lr1_a -= 1
            kit.servo[lr1].angle = lr1_a
            i -= 1
        if(j>0):
            lr2_a -= 1
            kit.servo[lr2].angle = lr2_a
            j -= 1
        sleep(interval_time)
    i = 50
    j =30
    while(i>0):
        if(i>0):
            lr1_a += 1
            kit.servo[lr1].angle = lr1_a
            i -= 1
        sleep(.005)
    while(j>0):
        lr2_a += 1
        kit.servo[lr2].angle = lr2_a
        j -= 1
        sleep(interval_time)

    
    i = 40
    while(i>0):
        lf2_a += 1
        kit.servo[lf2].angle = lf2_a
        i -= 1
        sleep(interval_time)
    i = 50
    j = 70
    while(i>0 or j>0):
        if(i>0):
            lf1_a -= 1
            kit.servo[lf1].angle = lf1_a
            i -= 1
        if(j>0):
            lf2_a -= 1
            kit.servo[lf2].angle = lf2_a
            j -= 1
        sleep(interval_time)
    i = 50
    j = 30
    while(i>0):
        if(i>0):
            lf1_a += 1
            kit.servo[lf1].angle = lf1_a
            i -= 1
        sleep(.005)
    while(j>0):
        lf2_a += 1
        kit.servo[lf2].angle = lf2_a
        j -= 1
        sleep(interval_time)

def stand():
    #left side
    kit.servo[4].angle = 152 #lf1
    kit.servo[5].angle = 66 #lf2
    kit.servo[12].angle = 152 #lr1
    kit.servo[13].angle = 66 #lr2

    #right side
    kit.servo[6].angle = 13 #rf1
    kit.servo[7].angle = 96 #rf2
    kit.servo[14].angle = 13 #rr1
    kit.servo[15].angle = 96 #rr2

def main():
    sleep(1)
    #trot_forward()
    rclpy.spin_once(joint_pub, timeout_sec=0.1)
    joint_pub.destroy_node()
    #rclpy.shutdown()

if __name__ == "__main__":
    main()

# from time import sleep, time
# from adafruit_servokit import ServoKit
# import math

# kit = ServoKit(channels=16)

# # Servo channels
# lf1, lf2 = 4, 5
# lr1, lr2 = 12, 13
# rf1, rf2 = 6, 7
# rr1, rr2 = 14, 15

# # Define leg config
# legs = {
#     'lf': {'hip': lf1, 'knee': lf2, 'hip_home': 152, 'knee_home': 66, 'swing_dir': -1, 'phase': 0.0},
#     'lr': {'hip': lr1, 'knee': lr2, 'hip_home': 152, 'knee_home': 66, 'swing_dir': -1, 'phase': 0.5},
#     'rf': {'hip': rf1, 'knee': rf2, 'hip_home': 13,  'knee_home': 96, 'swing_dir': 1,  'phase': 0.5},
#     'rr': {'hip': rr1, 'knee': rr2, 'hip_home': 13,  'knee_home': 96, 'swing_dir': 1,  'phase': 0.0},
# }

# def clamp(val, min_val=0, max_val=180):
#     return max(min(val, max_val), min_val)

# def generate_leg_trajectory(t, hip_home, knee_home, swing_dir, lift=30, swing=40):
#     hip_offset = math.sin(2 * math.pi * t) * swing * 0.5
#     knee_offset = math.sin(math.pi * (t % 1)) * lift if t < 0.5 else 0
#     hip_angle = clamp(hip_home + swing_dir * hip_offset)
#     knee_angle = clamp(knee_home - knee_offset if swing_dir == 1 else knee_home + knee_offset)
#     return hip_angle, knee_angle

# def stand():
#     for cfg in legs.values():
#         kit.servo[cfg['hip']].angle = cfg['hip_home']
#         kit.servo[cfg['knee']].angle = cfg['knee_home']

# def trot_forward(time_now, start_time, cycle_time=1.2):
#     t = ((time_now - start_time) % cycle_time) / cycle_time
#     for leg_name, cfg in legs.items():
#         hip_angle, knee_angle = generate_leg_trajectory(
#             t=(t + cfg['phase']) % 1.0,
#             hip_home=cfg['hip_home'],
#             knee_home=cfg['knee_home'],
#             swing_dir=cfg['swing_dir'],
#         )
#         kit.servo[cfg['hip']].angle = hip_angle
#         kit.servo[cfg['knee']].angle = knee_angle

# def walk_back(time_now, start_time, cycle_time=1.2):
#     t = ((time_now - start_time) % cycle_time) / cycle_time
#     for leg_name, cfg in legs.items():
#         # Reverses swing direction for backward walking
#         hip_angle, knee_angle = generate_leg_trajectory(
#             t=(t + cfg['phase']) % 1.0,
#             hip_home=cfg['hip_home'],
#             knee_home=cfg['knee_home'],
#             swing_dir=-cfg['swing_dir'],
#         )
#         kit.servo[cfg['hip']].angle = hip_angle
#         kit.servo[cfg['knee']].angle = knee_angle

# def turn_left(time_now, start_time, cycle_time=1.2):
#     t = ((time_now - start_time) % cycle_time) / cycle_time
#     for leg_name, cfg in legs.items():
#         mod_cfg = cfg.copy()
#         mod_cfg['swing_dir'] *= -1 if leg_name in ['rf', 'lr'] else 1
#         hip_angle, knee_angle = generate_leg_trajectory(
#             t=(t + mod_cfg['phase']) % 1.0,
#             hip_home=mod_cfg['hip_home'],
#             knee_home=mod_cfg['knee_home'],
#             swing_dir=mod_cfg['swing_dir'],
#         )
#         kit.servo[mod_cfg['hip']].angle = hip_angle
#         kit.servo[mod_cfg['knee']].angle = knee_angle

# def turn_right(time_now, start_time, cycle_time=1.2):
#     t = ((time_now - start_time) % cycle_time) / cycle_time
#     for leg_name, cfg in legs.items():
#         mod_cfg = cfg.copy()
#         mod_cfg['swing_dir'] *= -1 if leg_name in ['lf', 'rr'] else 1
#         hip_angle, knee_angle = generate_leg_trajectory(
#             t=(t + mod_cfg['phase']) % 1.0,
#             hip_home=mod_cfg['hip_home'],
#             knee_home=mod_cfg['knee_home'],
#             swing_dir=mod_cfg['swing_dir'],
#         )
#         kit.servo[mod_cfg['hip']].angle = hip_angle
#         kit.servo[mod_cfg['knee']].angle = knee_angle
