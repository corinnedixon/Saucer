import os
import time

# Start sauce pumps for 2 seconds
os.system("STEPPER_START,PUMP1,FORWARD," + str(s1_speed) + ",0'\n'")
os.system("STEPPER_START,PUMP2,FORWARD," + str(s2_speed) + ",0'\n'")
os.system("STEPPER_START,PUMP3,FORWARD," + str(s3_speed) + ",0'\n'")
os.system("STEPPER_START,PUMP4,FORWARD," + str(s4_speed) + ",0'\n'")

time.sleep(2)

os.system("STEPPER_STOP,PUMP1'\n'")
os.system("STEPPER_STOP,PUMP2'\n'")
os.system("STEPPER_STOP,PUMP3'\n'")
os.system("STEPPER_STOP,PUMP4'\n'")

# Spin turn table for 1000 steps at 1 ms per step
os.system("STEPPER_START,TURNTABLE,FORWARD,1000,1'\n'")
