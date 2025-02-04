from time import *
from adafruit_servokit import ServoKit

#initialize kit to channel for operation, will not need to do any other place
kit = ServoKit(channels=16)

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



def trot():
    lf1 = 147
    lf2 = 104
    lr1 = 147
    lr2 = 76
    rf1 = 33
    rf2 = 76
    rr1 = 33
    rr2 = 76
    for i in range (10):
        #PICK UP RF2
        #RF2 NEEDS 26, 30 DIFFERENCE
        kit.servo[7].angle = 46
        sleep(.1)

        #MOVE FOWARE RF1
        #RF1 NEEDS 83 30 DIFFERENCE
        kit.servo[6].angle = 43
        sleep(.1)

        #MOVE RF2 DOWN
        kit.servo[7].angle = 76
        sleep(.1)

        ##############LR
        kit.servo[13].angle = 134
        sleep(.1)
        kit.servo[12].angle = 137
        sleep(.1)
        kit.servo[13].angle = 104
        sleep(.1)
        #############LF
        kit.servo[5].angle = 134
        sleep(.1)
        kit.servo[4].angle = 137
        sleep(.1)
        kit.servo[5].angle = 104
        sleep(.1)
        ###############RR
        kit.servo[15].angle = 46
        sleep(.1)
        kit.servo[14].angle = 43
        sleep(.1)
        kit.servo[15].angle = 76
        sleep(.1)
        stand()


def stand():
    kit.servo[4].angle = 147
    kit.servo[5].angle = 104
    kit.servo[12].angle = 147
    kit.servo[13].angle = 104

    kit.servo[6].angle = 33
    kit.servo[7].angle = 76
    kit.servo[14].angle = 33
    kit.servo[15].angle = 76
    sleep(.1)
    
def main():
    stand()
    trot()


if __name__ == "__main__":
    main()