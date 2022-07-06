"""robo_controller controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(10)
    
maxMotorVelocity = 6
is_running= True
hingejoints = []
hgnames = ['shoulderright', 'shoulderleft']
for name in hgnames:
    hingejoints.append(robot.getDevice(name))
speed = 2  # [rad/s]
for idx,name in enumerate(hingejoints):
    hingejoints[idx].setPosition(float('inf'))
    hingejoints[idx].setVelocity(0.0)    
    hingejoints[idx].enableForceFeedback(1)
 
sensors=[]    
sensor_names=['dsfrontmiddle','dsfrontright','dsfrontleft','dsleft','dsright','dsback', 'start']
for i,s in enumerate(sensor_names):
    sensors.append(robot.getDevice(s))
    sensors[i].enable(timestep)
    

acc=robot.getDevice('accelerometer')
acc.enable(timestep)

MAX_SPEED = 6.28

# initialize motor speeds at 50% of MAX_SPEED.
leftSpeed  = 0.5 * MAX_SPEED
rightSpeed = 0.5 * MAX_SPEED

def fitness():
    pass

def detect_start():
    #sensor_values[6]<300:
    is_running=not is_running
    return is_running
    
def detect_fall():
    #if acc.getValues()[2]<=0:
    pass

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # read sensors outputs
    sensor_values = []
    for i,s in enumerate(sensors):
        sensor_values.append(sensors[i].getValue())
  
    if sensor_values[6]<300:
        print('DETECTED red')
        detect_start()
        
    #detect falling
    if acc.getValues()[2]<=0:
        print(acc.getValues())
        
    # detect obstacles
    right_obstacle = sensor_values[1] < 500.0 or sensor_values[4] < 500.0 
    left_obstacle = sensor_values[2] < 500.0 or sensor_values[3] < 500.0 
    
    if left_obstacle:
        # turn right
        print('LEFT OBSTACLE')
        leftSpeed  = -MAX_SPEED
        rightSpeed=0
    elif right_obstacle:
        print('RIGHT OBSTACLE')
        # turn left
        leftSpeed=0
        rightSpeed=-MAX_SPEED
    else:
        leftSpeed  = 0.5 * MAX_SPEED
        rightSpeed = 0.5 * MAX_SPEED
    
    # write actuators inputs
    hingejoints[1].setVelocity(leftSpeed)
    hingejoints[0].setVelocity(rightSpeed)
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass
#simulationReset() 
# Enter here exit cleanup code.
