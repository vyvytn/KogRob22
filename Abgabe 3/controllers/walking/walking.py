from controller import Robot, Motor, Supervisor, Receiver
#import NN

# create the Robot instance.
robot = Robot()
receiver=robot.getDevice("receiver")

timeStep =  int(robot.getBasicTimeStep())
#timeStep =  int(1)

maxMotorVelocity = 6
velocity = 0.7 * maxMotorVelocity  # [rad/s]
distanceSensorCalibrationConstant = 360

hgnames = ['shoulderleft', 'shoulderright']
left_motor=robot.getDevice(hgnames[0])
right_motor=robot.getDevice(hgnames[1])

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

# Enable distance sensors.
outerLeftSensor.enable(timeStep)
centralLeftSensor.enable(timeStep)
centralSensor.enable(timeStep)
centralRightSensor.enable(timeStep)
outerRightSensor.enable(timeStep)

receiver.enable(timeStep)

while robot.step(timeStep) != -1:

    """
    TODO: receive emitted weight AND call Neural Network and set weight in it
    
    if receiver.getQueueLength() > 0:
        data = receiver.getData()
        receiver.nextPacket()
        weights = np.array(json.loads(data))
        NN.setWeights(weights)
    """
    
    """
    TODO: read robot params and hand it over as input for the NN
    
    cur_velocity = left_moto.getVelocity()
    params_list.append(cur_velocity)
    predicted_output= NN.forward(params_list)
    """
   
    """TODO: wait for NN output and set the predicted output in robot
    left_motor.set(output_of_NN)
    right_motor.set(output_of_NN)
    """
    
    """obstacle avoidance algorithm"""
    # Read values from four distance sensors and calibrate.
    outerLeftSensorValue = outerLeftSensor.getValue() / distanceSensorCalibrationConstant
    centralLeftSensorValue = centralLeftSensor.getValue() / distanceSensorCalibrationConstant
    centralSensorValue = centralSensor.getValue() / distanceSensorCalibrationConstant
    centralRightSensorValue = centralRightSensor.getValue() / distanceSensorCalibrationConstant
    outerRightSensorValue = outerRightSensor.getValue() / distanceSensorCalibrationConstant

    # Set wheel velocities based on sensor values, prefer right turns if the central sensor is triggered.
    left_motor.setVelocity(velocity - (centralRightSensorValue + outerRightSensorValue) / 2)
    right_motor.setVelocity(velocity - (centralLeftSensorValue + outerLeftSensorValue) / 2 - centralSensorValue)

# Enter here exit cleanup code.
