"""Simple robot controller."""

from controller import Robot
import sys

# Define the target motor position in radians.
target = 0


# Get pointer to the robot.
robot = Robot()

# Print the program output on the console
print("Move the motors of the Thymio II to position " + str(target) + ".")
sys.stderr.write("This is a sample error message.\n")

# Set the target position of the left and right wheels motors.
robot.getDevice("motor.left").setPosition(target)
robot.getDevice("motor.right").setPosition(target)

class Robot():
    def __init__(
        gen,
        prob_mut,
        prob_cross,
        param1,
        param2,
        param3,
        param4,
        param5,
        param6):
        super(Robot, self).__init__()
        def calc_fitness()
            pass

