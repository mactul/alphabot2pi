# Alphabot 2 pi | libessential


Alphabot 2 pi is a nice little robot, but it lacks a lot of documentation on the web...\
I made this little library to condense in a single file the essential control functions of the robot.

With it, you can control very easily:
- the wheels of the robot
- the buzzer
- the camera
- the pan tilt (which holds the camera)
- the 5 buttons of the joystick
- the infrared distance sensors
- the remote control

all the functions are documented in the source code.

just be sure to use the `cleanup()` function at the end of all your programs to close the video stream and reset the GPIOs to their default values.
