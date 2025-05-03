# from time import *
# from adafruit_servokit import ServoKit
# # import stand as st

# #initialize kit to channel for operation, will not need to do any other place
# kit = ServoKit(channels=16)
# #servo port
# lf1 = 4
# lf2 = 5
# lr1 = 12
# lr2 = 13

# rf1 = 6
# rf2 = 7
# rr1 = 14
# rr2 = 15




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

# def trot_forward():
#     lf1_a = 152 #152
#     lf2_a = 66 #66
#     lr1_a = 152 #152
#     lr2_a = 66 #66
#     ########
#     rf1_a = 13 #13
#     rf2_a = 96 #96
#     rr1_a = 13 #13
#     rr2_a = 96 #96
#     interval_time =.00005 #.00005

# #NOTES FOR SWING TIME, interval_time is fast enough and slow enough to have a fluid motion
#     for i in range(1):
#         #phase 1, swing rf lr########################
#             #lift
#             i = 40 #lr and rf dif
#             j = 30 #lf and rr dif
#             while(i >= 0 or j >= 0):
#                 if(i >= 0):
#                     lr2_a += 1 #106
#                     rf2_a -= 1 #56
#                     kit.servo[lr2].angle = lr2_a
#                     kit.servo[rf2].angle = rf2_a
#                     i -= 1
#                 #move lf2 and rr2
#                 if(j >= 0):
#                     rr2_a += 1 #126
#                     lf2_a -=1 #36
#                     kit.servo[rr2].angle = rr2_a
#                     kit.servo[lf2].angle = lf2_a
#                     j -= 1
#                 sleep(interval_time)
#             sleep(interval_time)
#             ########################
#             #move rf and lr down(finish swing)
#             i = 30 #rf1 and lr1 dif
#             j = 40 #rf2 and lr2 dif
#             while(i >= 0 or j >= 0):
#                 if(i >= 0):
#                     rf1_a += 1 #30
#                     lr1_a -= 1 #140
#                     kit.servo[rf1].angle = rf1_a
#                     kit.servo[lr1].angle = lr1_a
#                     i -= 1
#                 if(j >= 0):
#                     rf2_a += 1 #91
#                     lr2_a -=1 #71
#                     kit.servo[lr2].angle = lr2_a
#                     kit.servo[rf2].angle = rf2_a
#                     j -= 1
#                 sleep(interval_time)
#         #pahse 2 swing lf rr
#             print(f"lf1: {lf1_a} lf2: {lf2_a} rr1: {rr1_a} rr2: {rr2_a}")
#             sleep(interval_time)
#             i = 11 # lf1 and rr1 dif 11
#             j = 30 # rf1 and lr1 dif
#             k = 5 # rf2 and lr2 dif 5
#             while(i >= 0 or j >= 0 or k >= 0):
#                 if(i >= 0):
#                     lf1_a += 1
#                     rr1_a -= 1
#                     kit.servo[lf1].angle = lf1_a
#                     kit.servo[rr1].angle = rr1_a
#                     i-=1
#                 if(j >= 0):
#                     rf1_a -= 1
#                     lr1_a += 1
#                     kit.servo[rf1].angle = rf1_a
#                     kit.servo[lr1].angle = lr1_a
#                     j-=1
#                 if(k >= 0):
#                     rf2_a += 1 
#                     lr2_a -= 1
#                     kit.servo[rf2].angle = rf2_a
#                     kit.servo[lr2].angle = lr2_a
#                     k-=1
#                 sleep(interval_time)
#             print("done ")
#             # sleep(5)
#             # retract lf2 and rr2
#             i = 40 #lf2 and rr2 diff
#             while(i >= 0):
#                 lf2_a += 1
#                 rr2_a -= 1
#                 kit.servo[lf2].angle = lf2_a
#                 kit.servo[rr2].angle = rr2_a
#                 i-=1
#                 sleep(interval_time)
#             #swing lf1 and rr1 (return back to standing)
#             i = 12 #lf1 and rr1 diff
#             j = 10 #lf2 and rr2 diff
#             k = 6  #lr2 and rf2 dif
#             while(i > 0 or j > 0 or k > 0):
#                 if(i > 0):
#                     lf1_a -= 1
#                     rr1_a += 1
#                     kit.servo[lf1].angle = lf1_a
#                     kit.servo[rr1].angle = rr1_a
#                     i-=1
#                 if(j > 0):
#                     lf2_a -= 1
#                     rr2_a += 1
#                     kit.servo[lf2].angle = lf2_a
#                     kit.servo[rr2].angle = rr2_a
#                     j-=1
#                 if(k > 0):
#                     lr2_a += 1
#                     rf2_a -= 1
#                     kit.servo[lr2].angle = lr2_a
#                     kit.servo[rf2].angle = rf2_a
#                     k -= 1
#                 sleep(interval_time)
    
#     print(f"lf1: {lf1_a}, lf2: {lf2_a}, rf1 : {rf1_a}, rf2: {rf2_a}, lr1: {lr1_a}, lr2: {lr2_a}, rr1: {rr1_a}, rr2: {rr2_a}")






# def stand():
# #left side
#     # kit.servo[4].angle = 132 #lf1
#     # kit.servo[5].angle = 86 #lf2
#     # kit.servo[12].angle = 132 #lr1
#     # kit.servo[13].angle = 86 #lr2

#     # #right side
#     # kit.servo[6].angle = 33 #rf1
#     # kit.servo[7].angle = 76 #rf2
#     # kit.servo[14].angle = 33 #rr1
#     # kit.servo[15].angle = 76 #rr2

#     #left side
#     kit.servo[4].angle = 152 #lf1
#     kit.servo[5].angle = 66 #lf2
#     kit.servo[12].angle = 152 #lr1
#     kit.servo[13].angle = 66 #lr2

#     #right side
#     kit.servo[6].angle = 13 #rf1
#     kit.servo[7].angle = 96 #rf2
#     kit.servo[14].angle = 13 #rr1
#     kit.servo[15].angle = 96 #rr2


# def trot_forward():
#     print("Starting improved symmetric trot...")

#     # Initial positions (based on your docs)
#     lf1_a, lf2_a = 152, 66   # Front left (back, down)
#     lr1_a, lr2_a = 152, 66   # Rear left
#     rf1_a, rf2_a = 13, 96    # Front right (back, down)
#     rr1_a, rr2_a = 13, 96    # Rear right

#     interval_time = 0.0001
#     step_count = 20

#     # === Phase 1: Swing RF + LR ===
#     for step in range(step_count):
#         # Lift phase
#         rf2_a -= 1
#         lr2_a += 1
#         kit.servo[rf2].angle = rf2_a
#         kit.servo[lr2].angle = lr2_a

#         # Swing phase
#         rf1_a += 1
#         lr1_a -= 1
#         kit.servo[rf1].angle = rf1_a
#         kit.servo[lr1].angle = lr1_a

#         sleep(interval_time)

#     # Set RF + LR down
#     for step in range(step_count):
#         rf2_a += 1
#         lr2_a -= 1
#         kit.servo[rf2].angle = rf2_a
#         kit.servo[lr2].angle = lr2_a
#         sleep(interval_time)

#     # === Phase 2: Swing LF + RR ===
#     for step in range(step_count):
#         # Lift phase
#         lf2_a -= 1
#         rr2_a += 1
#         kit.servo[lf2].angle = lf2_a
#         kit.servo[rr2].angle = rr2_a

#         # Swing phase
#         lf1_a -= 1
#         rr1_a += 1
#         kit.servo[lf1].angle = lf1_a
#         kit.servo[rr1].angle = rr1_a

#         sleep(interval_time)

#     # Set LF + RR down
#     for step in range(step_count):
#         lf2_a += 1
#         rr2_a -= 1
#         kit.servo[lf2].angle = lf2_a
#         kit.servo[rr2].angle = rr2_a
#         sleep(interval_time)

#     print("Trot complete.")
# #turn left
# def turn_left():
#     print("Turning Left (improved)...")

#     lf1_a, lf2_a = 152, 66
#     lr1_a, lr2_a = 152, 66
#     rf1_a, rf2_a = 13, 96
#     rr1_a, rr2_a = 13, 96
#     interval_time = 0.01

#     # Step 1: move RF + LR
#     for step in range(30):
#         if step < 20:
#             rf2_a -= 1
#             lr2_a += 1
#             kit.servo[rf2].angle = rf2_a
#             kit.servo[lr2].angle = lr2_a

#             rf1_a += 1
#             lr1_a -= 1
#             kit.servo[rf1].angle = rf1_a
#             kit.servo[lr1].angle = lr1_a
#         sleep(interval_time)

#     for step in range(20):
#         rf2_a += 1
#         lr2_a -= 1
#         kit.servo[rf2].angle = rf2_a
#         kit.servo[lr2].angle = lr2_a
#         sleep(interval_time)

#     # Step 2: move LF + RR
#     for step in range(30):
#         if step < 20:
#             lf2_a -= 1
#             rr2_a += 1
#             kit.servo[lf2].angle = lf2_a
#             kit.servo[rr2].angle = rr2_a

#             lf1_a -= 1
#             rr1_a += 1
#             kit.servo[lf1].angle = lf1_a
#             kit.servo[rr1].angle = rr1_a
#         sleep(interval_time)

#     for step in range(20):
#         lf2_a += 1
#         rr2_a -= 1
#         kit.servo[lf2].angle = lf2_a
#         kit.servo[rr2].angle = rr2_a
#         sleep(interval_time)

# def turn_right():
#     print("Turning Right (improved)...")

#     lf1_a, lf2_a = 152, 66
#     lr1_a, lr2_a = 152, 66
#     rf1_a, rf2_a = 13, 96
#     rr1_a, rr2_a = 13, 96
#     interval_time = 0.0001

#     # Step 1: move LF + RR
#     for step in range(30):
#         if step < 20:
#             lf2_a -= 1
#             rr2_a += 1
#             kit.servo[lf2].angle = lf2_a
#             kit.servo[rr2].angle = rr2_a

#             lf1_a -= 1
#             rr1_a += 1
#             kit.servo[lf1].angle = lf1_a
#             kit.servo[rr1].angle = rr1_a
#         sleep(interval_time)

#     for step in range(20):
#         lf2_a += 1
#         rr2_a -= 1
#         kit.servo[lf2].angle = lf2_a
#         kit.servo[rr2].angle = rr2_a
#         sleep(interval_time)

#     # Step 2: move RF + LR
#     for step in range(30):
#         if step < 20:
#             rf2_a -= 1
#             lr2_a += 1
#             kit.servo[rf2].angle = rf2_a
#             kit.servo[lr2].angle = lr2_a

#             rf1_a += 1
#             lr1_a -= 1
#             kit.servo[rf1].angle = rf1_a
#             kit.servo[lr1].angle = lr1_a
#         sleep(interval_time)

#     for step in range(20):
#         rf2_a += 1
#         lr2_a -= 1
#         kit.servo[rf2].angle = rf2_a
#         kit.servo[lr2].angle = lr2_a
#         sleep(interval_time)





# def main():
#     #st.stand()
#     sleep(1)
#     # for i in range (5):
#     #     turn_left()

# if __name__ == "__main__":
#     main()

from time import sleep
from adafruit_servokit import ServoKit
import math

# Initialize kit to channel for operation
kit = ServoKit(channels=16)

# Servo port mappings
lf1, lf2 = 4, 5
lr1, lr2 = 12, 13
rf1, rf2 = 6, 7
rr1, rr2 = 14, 15

def safe_angle(angle):
    """Clamp angle between 0 and 180 degrees."""
    return max(0, min(180, angle))

def stand():
    """Neutral standing pose."""
    print("Setting robot to stand position...")

    # left side
    kit.servo[lf1].angle = 152
    kit.servo[lf2].angle = 66
    kit.servo[lr1].angle = 152
    kit.servo[lr2].angle = 66

    # right side
    kit.servo[rf1].angle = 13
    kit.servo[rf2].angle = 96
    kit.servo[rr1].angle = 13
    kit.servo[rr2].angle = 96

    sleep(0.5)

def interpolate_swing(start, end, steps):
    """Generate smooth swing phase angles."""
    return [int(start + (end - start) * (0.5 - 0.5 * math.cos(math.pi * i / steps))) for i in range(steps)]

def interpolate_lift(start, end, steps):
    """Lift leg with a similar curve (smoother than linear)."""
    return interpolate_swing(start, end, steps)  # reuse cosine interpolation

def trot_forward():
    print("Starting improved symmetric trot...")
    step_count = 20
    interval_time = 0.02

    # Initialize to default stand position
    stand()

    # === Phase 1: RF + LR swing ===
    rf1_swing = interpolate_swing(13, 40, step_count)
    rf2_lift = interpolate_lift(96, 75, step_count)

    lr1_swing = interpolate_swing(152, 125, step_count)
    lr2_lift = interpolate_lift(66, 87, step_count)

    for i in range(step_count):
        kit.servo[rf1].angle = safe_angle(rf1_swing[i])
        kit.servo[rf2].angle = safe_angle(rf2_lift[i])
        kit.servo[lr1].angle = safe_angle(lr1_swing[i])
        kit.servo[lr2].angle = safe_angle(lr2_lift[i])
        sleep(interval_time)

    # === Phase 2: LF + RR swing ===
    lf1_swing = interpolate_swing(152, 125, step_count)
    lf2_lift = interpolate_lift(66, 87, step_count)

    rr1_swing = interpolate_swing(13, 40, step_count)
    rr2_lift = interpolate_lift(96, 75, step_count)

    for i in range(step_count):
        kit.servo[lf1].angle = safe_angle(lf1_swing[i])
        kit.servo[lf2].angle = safe_angle(lf2_lift[i])
        kit.servo[rr1].angle = safe_angle(rr1_swing[i])
        kit.servo[rr2].angle = safe_angle(rr2_lift[i])
        sleep(interval_time)

    print("Trot complete.")
    stand()

def main():
    #stand()
    sleep(1)
    #for _ in range(3):  # Trot forward 3 times
    #    trot_forward()
    #    sleep(0.5)

if __name__ == "__main__":
    main()
