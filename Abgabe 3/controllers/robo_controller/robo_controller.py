"""robo_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(10)
    
maxMotorVelocity = 6
hingejoints = []
hgnames = ['shoulder1', 'shoulder2', 'shoulder33', 'elle1', 'elle2', 'elle3']
for name in hgnames:
    hingejoints.append(robot.getDevice(name))
speed = -1.5  # [rad/s]
hingejoints[0].setPosition(float('inf'))
hingejoints[0].setVelocity(speed)    

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
