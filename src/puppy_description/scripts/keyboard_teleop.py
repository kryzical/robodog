#!/usr/bin/env python3
import rospy, sys, termios, tty, select
from std_msgs.msg import Float64

msg = """
Keyboard Teleop:
  w: increase joint command
  s: decrease joint command
  CTRL-C to quit.
"""

def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    key = rlist[0].read(1) if rlist else ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    pub = rospy.Publisher('/puppy/joint1_position_controller/command', Float64, queue_size=1)
    rospy.init_node('keyboard_teleop')
    rate = rospy.Rate(10)
    joint_cmd = 0.0
    print(msg)
    while not rospy.is_shutdown():
        key = getKey()
        if key == "w":
            joint_cmd += 0.1
        elif key == "s":
            joint_cmd -= 0.1
        elif key == "\x03":
            break
        pub.publish(joint_cmd)
        rate.sleep()

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    try:
        main()
    except rospy.ROSInterruptException:
        pass
