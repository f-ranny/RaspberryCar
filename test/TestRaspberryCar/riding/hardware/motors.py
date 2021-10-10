from gpiozero import Robot
from time import sleep

robot = Robot(left=(26, 20), right=(19, 16))

# Checking as motors work properly
if __name__ == "__main__":
    
    time = 3

    while 1:
        robot.forward()
        sleep(time)
        robot.backward()
        sleep(time)
        robot.right()
        sleep(time)
        robot.left
        sleep(time)
