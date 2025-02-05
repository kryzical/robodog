import threading, os, time
from ros_robot_controller_sdk import Board
from pwm_servo_control import PWMServoControl

board = Board()
#board.enable_reception()
psc = PWMServoControl(board)

psc.setThreshold(2,650,2300)
psc.setThreshold(6,650,2300)

psc.setThreshold(4,700,2350)
psc.setThreshold(8,700,2350)

def getServoDeviation(id):
    return psc.getDeviation(id)

def setServoPulse(id, pulse, use_time):
    psc.setPulse(id, pulse, use_time)

def setServoDeviation(id ,dev):
    psc.setDeviation(id, dev)

def saveServoDeviation():
    psc.saveDeviation()

def unloadServo(id):
    psc.unload(id)

def updatePulse(id):
    psc.updatePulse(id)

def enable_reception(enable=True):
    if enable:
        board.enable_reception(not enable)
        time.sleep(1)
        threading.Thread(target=os.system, args=("/bin/zsh -c \'source $HOME/armpi_fpv/src/armpi_fpv_bringup/scripts/source_env.bash && rostopic pub /ros_robot_controller/enable_reception std_msgs/Bool \"data: true\"\'",), daemon=True).start()
        time.sleep(1)
    else:
        threading.Thread(target=os.system, args=("/bin/zsh -c \'source $HOME/armpi_fpv/src/armpi_fpv_bringup/scripts/source_env.bash && rostopic pub /ros_robot_controller/enable_reception std_msgs/Bool \"data: false\"\'",), daemon=True).start()
        time.sleep(3)
        board.enable_reception(not enable)
        time.sleep(1)

