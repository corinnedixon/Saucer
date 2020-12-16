import time
import serial

# Open UART serial connection
ser = serial.Serial("/dev/ttyS0", 115200)  # opens port with baud rate

# Define speeds
s1_speed = 50 # Sauce stepper motor 1 speed
s2_speed = 50 # Sauce stepper motor 2 speed
s3_speed = 50 # Sauce stepper motor 3 speed
s4_speed = 50 # Sauce stepper motor 4 speed

# Start sauce pumps for 2 seconds
line1 = "$STEPPER_START,PUMP1,FORWARD," + str(s1_speed) + ",0\n"
ser.reset_output_buffer()
ser.write(line1.encode())
line2 = "$STEPPER_START,PUMP2,FORWARD," + str(s2_speed) + ",0\n"
ser.reset_output_buffer()
ser.write(line2.encode())
line3 = "$STEPPER_START,PUMP3,FORWARD," + str(s3_speed) + ",0\n"
ser.reset_output_buffer()
ser.write(line3.encode())
line4 ="$STEPPER_START,PUMP4,FORWARD," + str(s4_speed) + ",0\n"
ser.reset_output_buffer()
ser.write(line4.encode())

time.sleep(2)

stop1 = "$STEPPER_STOP,PUMP1\n"
ser.reset_output_buffer()
ser.write(stop1.encode())
stop2 = "$STEPPER_STOP,PUMP2\n"
ser.reset_output_buffer()
ser.write(stop2.encode())
stop3 = "$STEPPER_STOP,PUMP3\n"
ser.reset_output_buffer()
ser.write(stop3.encode())
stop4 = "$STEPPER_STOP,PUMP4\n"
ser.reset_output_buffer()
ser.write(stop4.encode())

# Spin turn table for 1000 steps at 1 ms per step
spin = "$STEPPER_START,TURNTABLE,FORWARD,1000,1\n"
ser.reset_output_buffer()
ser.write(spin.encode())
