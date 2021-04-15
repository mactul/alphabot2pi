import RPi.GPIO as GPIO
import time
from datetime import datetime


IR_PIN = 17

_last_key_pressed = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IR_PIN, GPIO.IN)


def _getkey():
    if GPIO.input(IR_PIN) == 0:
        count = 0
        while GPIO.input(IR_PIN) == 0 and count < 200:  # 9ms
            count += 1
            time.sleep(0.00006)
        if(count < 10):
            return

        count = 0
        while GPIO.input(IR_PIN) == 1 and count < 80:  # 4.5ms
            count += 1
            time.sleep(0.00006)

        idx = 0
        cnt = 0
        data = [0, 0, 0, 0]
        for i in range(32):
            count = 0
            while GPIO.input(IR_PIN) == 0 and count < 15:  # 0.56ms
                count += 1
                time.sleep(0.00006)

            count = 0
            while GPIO.input(IR_PIN) == 1 and count < 40:  # 0: 0.56ms
                count += 1  # 1: 1.69ms
                time.sleep(0.00006)

            if count > 7:
                data[idx] |= 1 << cnt
            if cnt == 7:
                cnt = 0
                idx += 1
            else:
                cnt += 1

        if data[0] + data[1] == 0xFF and data[2] + data[3] == 0xFF:
            return data[2]
        else:
            return -1  # the key is the same as last time


def remote_getkey():
    """returns the keys as written on the remote control"""

    global _last_key_pressed

    key = _getkey()
    if key is not None:
        if key == 24:
            _last_key_pressed = "2"

        elif key == 82:
            _last_key_pressed = "8"

        elif key == 8:
            _last_key_pressed = "4"

        elif key == 90:
            _last_key_pressed = "6"

        elif key == 28:
            _last_key_pressed = "5"

        elif key == 94:
            _last_key_pressed = "3"

        elif key == 74:
            _last_key_pressed = "9"

        elif key == 12:
            _last_key_pressed = "1"

        elif key == 66:
            _last_key_pressed = "7"

        elif key == 22:
            _last_key_pressed = "0"

        elif key == 7:
            _last_key_pressed = "-"

        elif key == 21:
            _last_key_pressed = "+"

        elif key == 9:
            _last_key_pressed = "="

        elif key == 71:
            _last_key_pressed = "ch+"

        elif key == 70:
            _last_key_pressed = "ch"

        elif key == 69:
            _last_key_pressed = "ch-"

        elif key == 67:
            _last_key_pressed = "play"

        elif key == 68:
            _last_key_pressed = "prev"

        elif key == 64:
            _last_key_pressed = "next"

        elif key == 25:
            _last_key_pressed = "100+"

        elif key == 13:
            _last_key_pressed = "200+"

        return _last_key_pressed


if __name__ == "__main__":
    while True:
        key = _getkey()
        if key is not None:
            print(key)
