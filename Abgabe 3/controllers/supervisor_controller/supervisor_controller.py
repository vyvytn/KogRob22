"""robo_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Motor, Supervisor, Node
from Generation import Generation, Genotype
# create the Robot instance.
#robot = Robot()
supervisor = Supervisor()
robot= supervisor.getFromDef("Robot")
trans_field=robot.getField("translation")
# get the time step of the current world.
timestep = int(10)

"""    
maxMotorVelocity = 6
hingejoints = []
hgnames = ['shoulderleft']
for name in hgnames:
    hingejoints.append(robot.getDevice(name))
speed = 2  # [rad/s]
for idx,name in enumerate(hingejoints):
    hingejoints[idx].setPosition(float('inf'))
    hingejoints[idx].setVelocity(speed)    
sensors=[]    
sensor_names=['dsfrontmiddle','dsfrontright','dsfrontleft','dsleft','dsright','dsback']
for s in sensor_names:
    sensors.append(robot.getDevice(s))
    
for s in sensors:
    print(s)
"""
    
# Main loop:
# - perform simulation steps until Webots is stopping the controller
i=0
while supervisor.step(timestep) != -1:
    i+=1
    print('POSITION',robot.getPosition())

    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
   
    pass

# Enter here exit cleanup code.
