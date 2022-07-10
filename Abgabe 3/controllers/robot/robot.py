from controller import Robot, Motor, Emitter, Receiver, Supervisor


# create the Robot instance.
robot = Robot()
#receiver = robot.getDevice("receiver")

# get the time step of the current world.
timeStep = int(robot.getBasicTimeStep())

maxMotorVelocity = 6
velocity = 0.7 * maxMotorVelocity  # [rad/s]

hgnames = ['shoulderright', 'shoulderleft']
left_motor = robot.getDevice(hgnames[0])
right_motor = robot.getDevice(hgnames[1])

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(velocity)
right_motor.setVelocity(velocity)
    
# Get frontal distance sensors.
outerLeftSensor = robot.getDevice("dsleft")
centralLeftSensor = robot.getDevice("dsfrontleft")
centralSensor = robot.getDevice("dsfrontmiddle")
centralRightSensor = robot.getDevice("dsfrontright")
outerRightSensor = robot.getDevice("dsright")

#receiver.enable(timeStep)

while robot.step(timeStep) != -1:
    """ receive Data from emitter
    if receiver.getQueueLength() > 0:
        data = receiver.getData()
        receiver.nextPacket()
        weights = np.array(json.loads(data))
        NN.setWeights(weights)
    """
    pass

# Enter here exit cleanup code.
