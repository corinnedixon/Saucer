import time
import serial

# Open UART serial connection
ser = serial.Serial("/dev/ttyAMA0", 9600)  # opens port with baud rate

# Define speeds
s1_speed = 50 # Sauce stepper motor 1 speed
s2_speed = 50 # Sauce stepper motor 2 speed
s3_speed = 50 # Sauce stepper motor 3 speed
s4_speed = 50 # Sauce stepper motor 4 speed

# Start sauce pumps for 2 seconds
ser.write('$STEPPER_START,PUMP1,FORWARD,' + str(s1_speed) + ',0\n')
ser.write('$STEPPER_START,PUMP2,FORWARD,' + str(s2_speed) + ',0\n')
ser.write('$STEPPER_START,PUMP3,FORWARD,' + str(s3_speed) + ',0\n')
ser.write('$STEPPER_START,PUMP4,FORWARD,' + str(s4_speed) + ',0\n')

time.sleep(2)

ser.write("$STEPPER_STOP,PUMP1'\n'")
ser.write("$STEPPER_STOP,PUMP2'\n'")
ser.write("$STEPPER_STOP,PUMP3'\n'")
ser.write("$STEPPER_STOP,PUMP4'\n'")

# Spin turn table for 1000 steps at 1 ms per step
ser.write("$STEPPER_START,TURNTABLE,FORWARD,1000,1'\n'")
