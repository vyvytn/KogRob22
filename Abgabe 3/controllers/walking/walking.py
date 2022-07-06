from controller import Robot, Motor, Supervisor, Receiver
#import NN

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep =  int(robot.getBasicTimeStep())

maxMotorVelocity = 6
speed = 2  # [rad/s]

hingejoints = []
hgnames = ['shoulderleft', 'shoulderright']
for name in hgnames:
    hingejoints.append(robot.getDevice(name))

for idx,name in enumerate(hingejoints):
    hingejoints[idx].setPosition(float('inf'))
    hingejoints[idx].setVelocity(speed)    
    
sensors=[]    
sensor_names=['dsfrontmiddle','dsfrontright','dsfrontleft','dsleft','dsright','dsback']
for s in sensor_names:
    sensors.append(robot.getDevice(s))

receiver = robot.getReceiver("receiver")
receiver.enable(timestep)
    

while robot.step(timestep) != -1:
    """ receive Data from emitter
    if receiver.getQueueLength() > 0:
        data = receiver.getData()
        receiver.nextPacket()
        weights = np.array(json.loads(data))
        NN.setWeights(weights)
    """
    pass

# Enter here exit cleanup code.
