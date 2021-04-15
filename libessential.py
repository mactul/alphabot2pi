"""
This module easily gathers in one file everything you need to control Alphabot2 pi
"""


import RPi.GPIO as GPIO
from adafruit_servokit import ServoKit
from picamera import PiCamera
import time
from includes.remote import remote_getkey

cam = PiCamera()
cam.start_preview()


# GPIO pins definition
BUZZ           = 4
CTR            = 7
A              = 8
B              = 9
C              = 10
D              = 11

IR_LEFT      = 16
IR_RIGHT       = 19
LEFT_FORWARD   = 13
LEFT_BACKWARD = 12
RIGHT_FORWARD    = 21
RIGHT_BACKWARD  = 20
PWM1           = 6
PWM2           = 26

kit = ServoKit(channels=16)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PWM1, GPIO.OUT)
GPIO.setup(PWM2, GPIO.OUT)
PWMA = GPIO.PWM(PWM1, 500)
PWMB = GPIO.PWM(PWM2, 500)
PWMA.start(50)
PWMB.start(50)


def bip(timer):
    """
    make a sound for timer seconds
    """
    GPIO.setup(BUZZ, GPIO.OUT)
    GPIO.output(BUZZ, GPIO.HIGH)
    time.sleep(timer)
    GPIO.output(BUZZ, GPIO.LOW)


def _setup_wheel(cycleA, cycleB):
    """
    change pwm motors
    """
    GPIO.setup(LEFT_FORWARD, GPIO.OUT)
    GPIO.setup(LEFT_BACKWARD, GPIO.OUT)
    GPIO.setup(RIGHT_FORWARD, GPIO.OUT)
    GPIO.setup(RIGHT_BACKWARD, GPIO.OUT)
    PWMA.ChangeDutyCycle(cycleA)
    PWMB.ChangeDutyCycle(cycleB)


def stop():
    """
    Stop the motors
    """
    _setup_wheel(0, 0)
    GPIO.output(LEFT_FORWARD, GPIO.LOW)
    GPIO.output(LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(RIGHT_BACKWARD, GPIO.LOW)


def forward(speed_left=50, speed_right=None):
    """
    if speed_left == speed_right: forward straight
    """
    if speed_right is None:
        speed_right = speed_left

    _setup_wheel(speed_left, speed_right)
    GPIO.output(LEFT_FORWARD, GPIO.HIGH)
    GPIO.output(LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(RIGHT_FORWARD, GPIO.HIGH)
    GPIO.output(RIGHT_BACKWARD, GPIO.LOW)


def backward(speed_left=50, speed_right=None):
    """
    same as forward in the other sens
    """
    if speed_right is None:
        speed_right = speed_left

    _setup_wheel(speed_left, speed_right)
    GPIO.output(LEFT_FORWARD, GPIO.LOW)
    GPIO.output(LEFT_BACKWARD, GPIO.HIGH)
    GPIO.output(RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(RIGHT_BACKWARD, GPIO.HIGH)


def left(speed_left=20, speed_right=None):
    """
    if speed_left == speed_right: left wheel and right wheel turn on opposite sens
    """
    if speed_right is None:
        speed_right = speed_left

    _setup_wheel(speed_left, speed_right)
    GPIO.output(LEFT_FORWARD, GPIO.LOW)
    GPIO.output(LEFT_BACKWARD, GPIO.HIGH)
    GPIO.output(RIGHT_FORWARD, GPIO.HIGH)
    GPIO.output(RIGHT_BACKWARD, GPIO.LOW)


def right(speed_left=20, speed_right=None):
    """
    if speed_left == speed_right: left wheel and right wheel turn on opposite sens
    """
    if speed_right is None:
        speed_right = speed_left

    _setup_wheel(speed_left, speed_right)
    GPIO.output(LEFT_FORWARD, GPIO.HIGH)
    GPIO.output(LEFT_BACKWARD, GPIO.LOW)
    GPIO.output(RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(RIGHT_BACKWARD, GPIO.HIGH)


def objet_left():
    """
    Returns True if there is an object in front of the left IR sensor
    """
    GPIO.setup(IR_LEFT, GPIO.IN)
    return not GPIO.input(IR_LEFT)


def objet_right():
    """
    Returns True if there is an object in front of the right IR sensor
    """
    GPIO.setup(IR_RIGHT, GPIO.IN)
    return not GPIO.input(IR_RIGHT)


def button_CTR():
    """
    Returns True if the middle button of the joystick is pressed
    """
    GPIO.setup(CTR, GPIO.IN, GPIO.PUD_UP)
    return not GPIO.input(CTR)


def button_A():
    """
    Returns True if the A button of the joystick is pressed
    """
    GPIO.setup(A, GPIO.IN, GPIO.PUD_UP)
    return not GPIO.input(A)


def button_B():
    """
    Returns True if the B button of the joystick is pressed
    """
    GPIO.setup(B, GPIO.IN, GPIO.PUD_UP)
    return not GPIO.input(B)


def button_C():
    """
    Returns True if the C button of the joystick is pressed
    """
    GPIO.setup(C, GPIO.IN, GPIO.PUD_UP)
    return not GPIO.input(C)


def button_D():
    """
    Returns True if the D button of the joystick is pressed
    """
    GPIO.setup(D, GPIO.IN, GPIO.PUD_UP)
    return not GPIO.input(D)


def pan(angle):
    """
    Change the pan camera angle
    need to be between 20 and 150
    """
    if angle >= 20 and angle <= 150:
        kit.servo[0].angle = angle
    elif angle < 20:
        kit.servo[0].angle = 20
    else:
        kit.servo[0].angle = 150


def tilt(angle):
    """
    Change the tilt camera angle
    need to be between 120 and 180
    """
    if angle >= 120 and angle <= 180:
        kit.servo[1].angle = angle
    elif angle < 120:
        kit.servo[0].angle = 120
    else:
        kit.servo[0].angle = 180


def photo(brightness, size=(500, 500)):
    """
    Take a photo and register it with the datetime as name
    """
    cam.brightness = brightness
    cam.capture("image" + str(time.time()) + ".jpg", resize=size)


def cleanup():
    """
    clean GPIO and camera
    """
    GPIO.cleanup()
    cam.stop_preview()


if __name__ == "__main__":
    """
    An example to control the robot with the remote control
    """
    try:
        pan_angle  = 90
        tilt_angle = 180
        pan(pan_angle)
        tilt(tilt_angle)

        brightness = 50

        speed = 50

        while True:
            key = remote_getkey()
            if key is not None:
                if key == "2":
                    forward(speed)

                elif key == "8":
                    backward(speed)

                elif key == "5":
                    stop()

                elif key == "4":
                    left(speed/1.5)

                elif key == "6":
                    right(speed/1.5)

                elif key == "3":
                    if pan_angle > 20:
                        for i in range(20):
                            pan_angle -= 0.5
                            pan(pan_angle)
                            time.sleep(0.001)
                elif key == "1":
                    if pan_angle < 150:
                        for i in range(20):
                            pan_angle += 0.5
                            pan(pan_angle)
                            time.sleep(0.001)

                elif key == "-":
                    if tilt_angle > 120:
                        for i in range(20):
                            tilt_angle -= 0.5
                            tilt(tilt_angle)
                            time.sleep(0.001)
                elif key == "0":
                    if tilt_angle < 180:
                        for i in range(20):
                            tilt_angle += 0.5
                            tilt(tilt_angle)
                            time.sleep(0.001)

                elif key == "play":
                    photo(brightness)
                    bip(0.008)

                elif key == "prev":
                    if brightness > 10:
                        brightness -= 10
                        print(brightness)
                        bip(0.008)

                elif key == "next":
                    if brightness < 90:
                        brightness += 10
                        print(brightness)
                        bip(0.008)

                elif key == "100+":
                    if speed > 30:
                        speed -= 5

                elif key == "200+":
                    if speed < 90:
                        speed += 5

                elif key == "ch+":
                    break

        cleanup()

    except KeyboardInterrupt:
        cleanup()