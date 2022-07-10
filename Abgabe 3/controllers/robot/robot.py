from controller import Robot, Motor, Emitter, Receiver, Supervisor
from neural_network import NeuralNetwork
import numpy as np
import json

# create the Robot instance.
robot = Robot()
receiver = robot.getDevice("receiver")

NN = NeuralNetwork(1, 1)

# get the time step of the current world.
timeStep = int(robot.getBasicTimeStep())

maxMotorVelocity = 6
velocity = 0.7 * maxMotorVelocity  # [rad/s]
distanceSensorCalibrationConstant = 360

hgnames = ['shoulderright', 'shoulderleft']
right_motor = robot.getDevice(hgnames[0])
left_motor = robot.getDevice(hgnames[1])

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

outerLeftSensor.enable(timeStep)
centralLeftSensor.enable(timeStep)
centralSensor.enable(timeStep)
centralRightSensor.enable(timeStep)
outerRightSensor.enable(timeStep)

receiver.enable(timeStep)

while robot.step(timeStep) != -1:

    NN_input = np.array([left_motor.getVelocity(),
                         right_motor.getVelocity(),
                         outerLeftSensorValue.getValue(),
                         centralLeftSensor.getValue(),
                         centralSensor.getValue(),
                         centralRightSensor.getValue(),
                         outerRightSensor.getValue()])

    # receive Data from emitter
    if receiver.getQueueLength() > 0:
        data = receiver.getData()
        receiver.nextPacket()
        weights = np.array(json.loads(data))
        NN.setWeights(weights)

        output = NN.forward(NN_input)

        # TODO: take output and set values of robot

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
