from time import *
from adafruit_servokit import ServoKit

kit = ServoKit(channels= 16)

#standard standing
# kit.servo[4].angle = 130
# kit.servo[5].angle = 90
# kit.servo[6].angle = 40
# kit.servo[7].angle = 70
# kit.servo[12].angle = 130
# kit.servo[13].angle = 90
# kit.servo[14].angle = 40
# kit.servo[15].angle = 70

# #left side
# kit.servo[4].angle = 123
# kit.servo[5].angle = 66
# kit.servo[12].angle = 123
# kit.servo[13].angle = 66

# #right side
# kit.servo[6].angle = 33
# kit.servo[7].angle = 76
# kit.servo[14].angle = 33
# kit.servo[15].angle = 76

#standing 2########################################
# #left side
# kit.servo[4].angle = 132
# kit.servo[5].angle = 86 #86
# kit.servo[12].angle = 132
# kit.servo[13].angle = 86

# #right side
# kit.servo[6].angle = 33
# kit.servo[7].angle = 76 #76
# kit.servo[14].angle = 33
# kit.servo[15].angle = 76


def stand():
#left side
    # kit.servo[4].angle = 132 #lf1
    # kit.servo[5].angle = 86 #lf2
    # kit.servo[12].angle = 132 #lr1
    # kit.servo[13].angle = 86 #lr2

    # #right side
    # kit.servo[6].angle = 33 #rf1
    # kit.servo[7].angle = 76 #rf2
    # kit.servo[14].angle = 33 #rr1
    # kit.servo[15].angle = 76 #rr2

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
    stand()

if __name__ == "__main__":
    main()
