from ros_robot_controller_sdk import Board
import time

board = Board()
board.enable_reception()

board.pwm_servo_set_offset(1,0)
board.pwm_servo_set_position(0.1,[[1,499]])
time.sleep(0.5)

print(board.pwm_servo_read_offset(1))
print(board.pwm_servo_read_position(1))
