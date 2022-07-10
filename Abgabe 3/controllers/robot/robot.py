from controller import Robot, Motor, Emitter, Receiver, Supervisor
import numpy as np
import json
import struct

# create the Robot instance.

robot = Robot()
# get the time step of the current world.
timeStep = int(robot.getBasicTimeStep())

receiver = robot.getDevice("receiver")
emitter = robot.getDevice("emitter")
receiver.enable(timeStep)
maxMotorVelocity = 6
velocity_left = 0.7 * maxMotorVelocity  # [rad/s]
velocity_right= 0.7 * maxMotorVelocity  # [rad/s]

distanceSensorCalibrationConstant = 360

hgnames = ['shoulderright', 'shoulderleft', 'shoulderright2', 'shoulderleft2']
right_motor = robot.getDevice(hgnames[0])
left_motor = robot.getDevice(hgnames[1])
right_motor_2 = robot.getDevice(hgnames[2])
left_motor_2 = robot.getDevice(hgnames[3])

left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
right_motor_2.setPosition(float('inf'))
left_motor_2.setPosition(float('inf'))

left_motor.setVelocity(velocity_left)
left_motor_2.setVelocity(velocity_left)
right_motor.setVelocity(velocity_right)
right_motor_2.setVelocity(velocity_right)

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
    left_motor_2.getVelocity(),
    right_motor_2.getVelocity(),
    outerLeftSensor.getValue(),
    centralLeftSensor.getValue(),
    centralSensor.getValue(),
    centralRightSensor.getValue(),
    outerRightSensor.getValue()])

    #send sensordata to supervisor fpr NN
    string_message = np.array2string(NN_input,separator=',')
    string_message = string_message.encode("utf-8")
    emitter.send(string_message)
    
    if receiver.getQueueLength() > 0:
            receivedData = receiver.getData().decode("utf-8")
            output= eval(receivedData)
            velocity_left=output[0]
            velocity_right=output[1]
            velocity_left2=output[2]
            velocity_right2=output[3]

            left_motor.setVelocity(velocity_left)
            left_motor_2.setVelocity(velocity_left2)
            right_motor.setVelocity(velocity_right)
            right_motor_2.setVelocity(velocity_right2)
            receiver.nextPacket()

   
    #TODO: take output and set values of robot
    #obstacle avoidance algorithm
    #Read values from four distance sensors and calibrate.
    outerLeftSensorValue = outerLeftSensor.getValue() / distanceSensorCalibrationConstant
    centralLeftSensorValue = centralLeftSensor.getValue() / distanceSensorCalibrationConstant
    centralSensorValue = centralSensor.getValue() / distanceSensorCalibrationConstant
    centralRightSensorValue = centralRightSensor.getValue() / distanceSensorCalibrationConstant
    outerRightSensorValue = outerRightSensor.getValue() / distanceSensorCalibrationConstant

    # Set wheel velocities based on sensor values, prefer right turns if the central sensor is triggered.
    left_motor.setVelocity(velocity_left - (centralRightSensorValue + outerRightSensorValue) / 2)
    right_motor.setVelocity(velocity_right - (centralLeftSensorValue + outerLeftSensorValue) / 2 - centralSensorValue)

# Enter here exit cleanup code.
