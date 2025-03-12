from time import *
import math
import stand as st

# Try to import the physical robot library
try:
    from adafruit_servokit import ServoKit
    kit = ServoKit(channels=16)
except ImportError:
    # Use simulation mode if the hardware library isn't available
    kit = None

# Use the simulation mode flag from the stand module
simulation_mode = st.simulation_mode

# Servo port mapping
lf1 = 4    # front left upper
lf2 = 5    # front left lower
lr1 = 12   # back left upper
lr2 = 13   # back left lower 
rf1 = 6    # front right upper
rf2 = 7    # front right lower
rr1 = 14   # back right upper
rr2 = 15   # back right lower

def set_servo_angle(servo_name, angle):
    """Set angle using either physical servo or simulation"""
    st.set_servo_angle(servo_name, angle)

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
    
    # NOTES FOR SWING TIME, interval_time is fast enough and slow enough to have a fluid motion
    for i in range(1):
        # phase 1, swing rf lr########################
        # lift
        i = 40 #lr and rf dif
        j = 30 #lf and rr dif
        while(i >= 0 or j >= 0):
            if(i >= 0):
                lr2_a += 1 #106
                rf2_a -= 1 #56
                set_servo_angle('lr2', lr2_a)
                set_servo_angle('rf2', rf2_a)
                i -= 1
            # move lf2 and rr2
            if(j >= 0):
                rr2_a += 1 #126
                lf2_a -=1 #36
                set_servo_angle('rr2', rr2_a)
                set_servo_angle('lf2', lf2_a)
                j -= 1
            sleep(interval_time)
        sleep(interval_time)
        ########################
        # move rf and lr down(finish swing)
        i = 30 #rf1 and lr1 dif
        j = 40 #rf2 and lr2 dif
        while(i >= 0 or j >= 0):
            if(i >= 0):
                rf1_a += 1 #30
                lr1_a -= 1 #140
                set_servo_angle('rf1', rf1_a)
                set_servo_angle('lr1', lr1_a)
                i -= 1
            if(j >= 0):
                rf2_a += 1 #91
                lr2_a -=1 #71
                set_servo_angle('lr2', lr2_a)
                set_servo_angle('rf2', rf2_a)
                j -= 1
            sleep(interval_time)
        # pahse 2 swing lf rr
        print(f"lf1: {lf1_a} lf2: {lf2_a} rr1: {rr1_a} rr2: {rr2_a}")
        sleep(interval_time)
        i = 11 # lf1 and rr1 dif 11
        j = 30 # rf1 and lr1 dif
        k = 5 # rf2 and lr2 dif 5
        while(i >= 0 or j >= 0 or k >= 0):
            if(i >= 0):
                lf1_a += 1
                rr1_a -= 1
                set_servo_angle('lf1', lf1_a)
                set_servo_angle('rr1', rr1_a)
                i-=1
            if(j >= 0):
                rf1_a -= 1
                lr1_a += 1
                set_servo_angle('rf1', rf1_a)
                set_servo_angle('lr1', lr1_a)
                j-=1
            if(k >= 0):
                rf2_a += 1 
                lr2_a -= 1
                set_servo_angle('rf2', rf2_a)
                set_servo_angle('lr2', lr2_a)
                k-=1
            sleep(interval_time)
        print("done ")
        # sleep(5)
        # retract lf2 and rr2
        i = 40 #lf2 and rr2 diff
        while(i >= 0):
            lf2_a += 1
            rr2_a -= 1
            set_servo_angle('lf2', lf2_a)
            set_servo_angle('rr2', rr2_a)
            i-=1
            sleep(interval_time)
        # swing lf1 and rr1 (return back to standing)
        i = 12 #lf1 and rr1 diff
        j = 10 #lf2 and rr2 diff
        k = 6  #lr2 and rf2 dif
        while(i > 0 or j > 0 or k > 0):
            if(i > 0):
                lf1_a -= 1
                rr1_a += 1
                set_servo_angle('lf1', lf1_a)
                set_servo_angle('rr1', rr1_a)
                i-=1
            if(j > 0):
                lf2_a -= 1
                rr2_a += 1
                set_servo_angle('lf2', lf2_a)
                set_servo_angle('rr2', rr2_a)
                j-=1
            if(k > 0):
                lr2_a += 1
                rf2_a -= 1
                set_servo_angle('lr2', lr2_a)
                set_servo_angle('rf2', rf2_a)
                k -= 1
            sleep(interval_time)
    
    print(f"lf1: {lf1_a}, lf2: {lf2_a}, rf1 : {rf1_a}, rf2: {rf2_a}, lr1: {lr1_a}, lr2: {lr2_a}, rr1: {rr1_a}, rr2: {rr2_a}")

# turn left
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
    
    # note right legs will be drag, left will be stationary
    i = 40
    while(i>0):
        rr2_a -= 1
        set_servo_angle('rr2', rr2_a)
        i -= 1
        sleep(interval_time)
    i = 40
    j = 60
    while(i>0 or j>0):
        if(i>0):
            rr1_a += 1
            set_servo_angle('rr1', rr1_a)
            i -= 1
        if(j>0):
            rr2_a += 1
            set_servo_angle('rr2', rr2_a)
            j -= 1
        sleep(interval_time)
    i = 40
    j = 20
    while(i>0):
        if(i>0):
            rr1_a -= 1
            set_servo_angle('rr1', rr1_a)
            i -= 1
        sleep(.005)
    while(j>0):
        rr2_a -= 1
        set_servo_angle('rr2', rr2_a)
        j -= 1
        sleep(interval_time)
    i = 40
    while(i>0):
        rf2_a -= 1
        set_servo_angle('rf2', rf2_a)
        i -= 1
        sleep(interval_time)
    i = 40
    j = 60
    while(i>0 or j>0):
        if(i>0):
            rf1_a += 1
            set_servo_angle('rf1', rf1_a)
            i -= 1
        if(j>0):
            rf2_a += 1
            set_servo_angle('rf2', rf2_a)
            j -= 1
        sleep(interval_time)
    i = 40
    j = 20
    while(i>0):
        if(i>0):
            rf1_a -= 1
            set_servo_angle('rf1', rf1_a)
            i -= 1
        sleep(.005)
    while(j>0):
        rf2_a -= 1
        set_servo_angle('rf2', rf2_a)
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
    # left legs will drag
    i = 40
    while(i>0):
        lr2_a += 1
        set_servo_angle('lr2', lr2_a)
        i -= 1
        sleep(interval_time)
    i = 50
    j = 70
    while(i>0 or j>0):
        if(i>0):
            lr1_a -= 1
            set_servo_angle('lr1', lr1_a)
            i -= 1
        if(j>0):
            lr2_a -= 1
            set_servo_angle('lr2', lr2_a)
            j -= 1
        sleep(interval_time)
    i = 50
    j =30
    while(i>0):
        if(i>0):
            lr1_a += 1
            set_servo_angle('lr1', lr1_a)
            i -= 1
        sleep(.005)
    while(j>0):
        lr2_a += 1
        set_servo_angle('lr2', lr2_a)
        j -= 1
        sleep(interval_time)
    
    i = 40
    while(i>0):
        lf2_a += 1
        set_servo_angle('lf2', lf2_a)
        i -= 1
        sleep(interval_time)
    i = 50
    j = 70
    while(i>0 or j>0):
        if(i>0):
            lf1_a -= 1
            set_servo_angle('lf1', lf1_a)
            i -= 1
        if(j>0):
            lf2_a -= 1
            set_servo_angle('lf2', lf2_a)
            j -= 1
        sleep(interval_time)
    i = 50
    j = 30
    while(i>0):
        if(i>0):
            lf1_a += 1
            set_servo_angle('lf1', lf1_a)
            i -= 1
        sleep(.005)
    while(j>0):
        lf2_a += 1
        set_servo_angle('lf2', lf2_a)
        j -= 1
        sleep(interval_time)

def main():
    st.stand()
    sleep(1)
    for i in range (5):
        turn_left()

if __name__ == "__main__":
    main()
