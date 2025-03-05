from time import *
from adafruit_servokit import ServoKit

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



def trot_forward():
    print("in trot")
    lf1_a = 152
    lf2_a = 66
    lr1_a = 152
    lr2_a = 66
    ########
    rf1_a = 13
    rf2_a = 96
    rr1_a = 13
    rr2_a = 96
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
            sleep(interval_time)
            i = 11 # lf1 and rr1 dif
            j = 30 # rf1 and lr1 dif
            k = 5 # rf2 and lr2 dif
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
                    # rf2_a += 1
                    # lr2_a -= 1
                    # kit.servo[rf2].angle = rf2_a
                    # kit.servo[lr2].angle = lr2_a
                    k-=1
                sleep(interval_time)
            sleep(interval_time)
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
            while(i > 0 or j > 0):
                if(i > 0):
                    lf1_a -= 1
                    rr1_a += 1
                    kit.servo[lf1].angle = lf1_a
                    kit.servo[rr1].angle = rr1_a
                    i-=1
                if(j > 0):
                    lf2_a -= 1
                    rr2_a += 1
                    kit.servo[lf2].angle = lr2_a
                    kit.servo[rr2].angle = rr2_a
                    j-=1
                sleep(interval_time)
    # print(f"lf1: {lf1_a}, lf2: {lf2_a}, rf1 : {rf1_a}, rf2: {rf2_a}, lr1: {lr1_a}, lr2: {lr2_a}, rr1: {rr1_a}, rr2: {rr2_a}"

#turn left
def turn_left():
    lf1_a = 152
    lf2_a = 66
    lr1_a = 152
    lr2_a = 66
    ########
    rf1_a = 13
    rf2_a = 96
    rr1_a = 13
    rr2_a = 96
    interval_time =.00005 #.00005


def main():
    trot_forward()

if __name__ == "__main__":
    main()