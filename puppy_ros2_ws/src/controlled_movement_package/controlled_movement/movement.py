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




# # LF1; front left upper 4
# #     range 0(forward) 180 (backward)
# # LF2; front left lower 5
# #     range 0(extended) 180(in)
# # RF1 6
# #     range 0(backward) 180(forward)
# # RF2 7
# #     range 0(in) 180 (extended)
# # LR1 12
# #     range 0(forward) 180 (backward)
# # lR2 13
# #     range 0(extended) 180(in)
# # RR1 14
# #     range 0(backward) 180(forward)
# # RR2 15
# #     range 0(in) 180 (extended)

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


from time import sleep, time
from adafruit_servokit import ServoKit
import math

kit = ServoKit(channels=16)

# Servo channels
lf1, lf2 = 4, 5
lr1, lr2 = 12, 13
rf1, rf2 = 6, 7
rr1, rr2 = 14, 15

# Define leg config
legs = {
    'lf': {'hip': lf1, 'knee': lf2, 'hip_home': 152, 'knee_home': 66, 'swing_dir': -1, 'phase': 0.0},
    'lr': {'hip': lr1, 'knee': lr2, 'hip_home': 152, 'knee_home': 66, 'swing_dir': -1, 'phase': 0.5},
    'rf': {'hip': rf1, 'knee': rf2, 'hip_home': 13,  'knee_home': 96, 'swing_dir': 1,  'phase': 0.5},
    'rr': {'hip': rr1, 'knee': rr2, 'hip_home': 13,  'knee_home': 96, 'swing_dir': 1,  'phase': 0.0},
}

def clamp(val, min_val=0, max_val=180):
    return max(min(val, max_val), min_val)

def generate_leg_trajectory(t, hip_home, knee_home, swing_dir, lift=30, swing=40):
    hip_offset = math.sin(2 * math.pi * t) * swing * 0.5
    knee_offset = math.sin(math.pi * (t % 1)) * lift if t < 0.5 else 0
    hip_angle = clamp(hip_home + swing_dir * hip_offset)
    knee_angle = clamp(knee_home - knee_offset if swing_dir == 1 else knee_home + knee_offset)
    return hip_angle, knee_angle

def stand():
    for cfg in legs.values():
        kit.servo[cfg['hip']].angle = cfg['hip_home']
        kit.servo[cfg['knee']].angle = cfg['knee_home']

def trot_forward(time_now, start_time, cycle_time=1.2):
    t = ((time_now - start_time) % cycle_time) / cycle_time
    for leg_name, cfg in legs.items():
        hip_angle, knee_angle = generate_leg_trajectory(
            t=(t + cfg['phase']) % 1.0,
            hip_home=cfg['hip_home'],
            knee_home=cfg['knee_home'],
            swing_dir=cfg['swing_dir'],
        )
        kit.servo[cfg['hip']].angle = hip_angle
        kit.servo[cfg['knee']].angle = knee_angle

def walk_back(time_now, start_time, cycle_time=1.2):
    t = ((time_now - start_time) % cycle_time) / cycle_time
    for leg_name, cfg in legs.items():
        # Reverses swing direction for backward walking
        hip_angle, knee_angle = generate_leg_trajectory(
            t=(t + cfg['phase']) % 1.0,
            hip_home=cfg['hip_home'],
            knee_home=cfg['knee_home'],
            swing_dir=-cfg['swing_dir'],
        )
        kit.servo[cfg['hip']].angle = hip_angle
        kit.servo[cfg['knee']].angle = knee_angle

def turn_left(time_now, start_time, cycle_time=1.2):
    t = ((time_now - start_time) % cycle_time) / cycle_time
    for leg_name, cfg in legs.items():
        mod_cfg = cfg.copy()
        mod_cfg['swing_dir'] *= -1 if leg_name in ['rf', 'lr'] else 1
        hip_angle, knee_angle = generate_leg_trajectory(
            t=(t + mod_cfg['phase']) % 1.0,
            hip_home=mod_cfg['hip_home'],
            knee_home=mod_cfg['knee_home'],
            swing_dir=mod_cfg['swing_dir'],
        )
        kit.servo[mod_cfg['hip']].angle = hip_angle
        kit.servo[mod_cfg['knee']].angle = knee_angle

def turn_right(time_now, start_time, cycle_time=1.2):
    t = ((time_now - start_time) % cycle_time) / cycle_time
    for leg_name, cfg in legs.items():
        mod_cfg = cfg.copy()
        mod_cfg['swing_dir'] *= -1 if leg_name in ['lf', 'rr'] else 1
        hip_angle, knee_angle = generate_leg_trajectory(
            t=(t + mod_cfg['phase']) % 1.0,
            hip_home=mod_cfg['hip_home'],
            knee_home=mod_cfg['knee_home'],
            swing_dir=mod_cfg['swing_dir'],
        )
        kit.servo[mod_cfg['hip']].angle = hip_angle
        kit.servo[mod_cfg['knee']].angle = knee_angle



# def main():
#     #st.stand()
#     sleep(1)
#     # for i in range (5):
#     #     turn_left()

# if __name__ == "__main__":
#     main()



# from time import sleep
# from adafruit_servokit import ServoKit

# kit = ServoKit(channels=16)

# # Servo mapping
# lf1, lf2 = 4, 5
# lr1, lr2 = 12, 13
# rf1, rf2 = 6, 7
# rr1, rr2 = 14, 15

# def safe(angle): return max(0, min(180, angle))

# # === Stand Pose ===
# def stand():
#     print("Standing...")
#     kit.servo[lf1].angle = 152
#     kit.servo[lf2].angle = 66
#     kit.servo[lr1].angle = 152
#     kit.servo[lr2].angle = 66
#     kit.servo[rf1].angle = 13
#     kit.servo[rf2].angle = 96
#     kit.servo[rr1].angle = 13
#     kit.servo[rr2].angle = 96
#     sleep(0.5)

# # === Single Trot Phase ===
# def swing_leg(name, hip_servo, knee_servo, hip_start, hip_end, knee_up, knee_down):
#     print(f"Swinging {name}...")
#     kit.servo[knee_servo].angle = knee_up   # Lift leg
#     sleep(0.2)
#     kit.servo[hip_servo].angle = hip_end    # Swing leg
#     sleep(0.2)
#     kit.servo[knee_servo].angle = knee_down # Set leg down
#     sleep(0.2)

# def trot_forward():
#     # Start from stand
#     stand()

#     # Phase 1: RF + LR swing
#     swing_leg("RF", rf1, rf2, 13, 40, 75, 96)
#     swing_leg("LR", lr1, lr2, 152, 125, 87, 66)

#     # Delay to stabilize
#     sleep(0.2)

#     # Phase 2: LF + RR swing
#     swing_leg("LF", lf1, lf2, 152, 125, 87, 66)
#     swing_leg("RR", rr1, rr2, 13, 40, 75, 96)

#     sleep(0.2)

# def main():
#     stand()
#     #for _ in range(3):
#     #    trot_step()
#     #stand()

# if __name__ == "__main__":
#     main()



