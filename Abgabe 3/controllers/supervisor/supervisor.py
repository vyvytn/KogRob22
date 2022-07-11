import numpy as np
import struct
from controller import Motor, Supervisor, Node, Emitter, Receiver
from neural_network import NeuralNetwork
from population import Population
import json
import torch
from os.path import exists

input_size = 25
output_size = 20
time_for_scoring = 5  # in Sekunden

# NN = NeuralNetwork(input_size, output_size)

supervisor = Supervisor()
timeStep = int(supervisor.getBasicTimeStep())

emitter = supervisor.getDevice("emitter")
receiver = supervisor.getDevice("receiver")
robot = supervisor.getFromDef("Robot")
receiver.enable(timeStep)

# nodes for translation and rotation field
trans_field = robot.getField("translation")
rotation_field = robot.getField("rotation")

param_right1 = supervisor.getFromDef("right_arm1")
axis_right1 = param_right1.getField("axis")
position_right1 = param_right1.getField("position")

param_right2 = supervisor.getFromDef("right_arm2")
axis_right2 = param_right2.getField("axis")
position_right2 = param_right2.getField("position")

param_left1 = supervisor.getFromDef("left_arm1")
axis_left1 = param_left1.getField("axis")
position_left1 = param_left1.getField("position")

param_left2 = supervisor.getFromDef("left_arm2")
axis_left2 = param_left2.getField("axis")
position_left2 = param_left2.getField("position")

# axis_right.setSFVec3f([0.0,0.0,1.0])
# axis_right.getSFVec3f()

# Get frontal distance sensors.
outerLeftSensor = supervisor.getFromDef("dsleft")
centralLeftSensor = supervisor.getFromDef("dsfrontleft")
centralSensor = supervisor.getFromDef("dsfrontmiddle")
centralRightSensor = supervisor.getFromDef("dsfrontright")
outerRightSensor = supervisor.getFromDef("dsright")

# get initial start position for reset method
start_rotation = rotation_field.getSFRotation()
start_position = robot.getPosition()


# reset robot to intial point
def reset_robot():
	trans_field.setSFVec3f(start_position)
	rotation_field.setSFRotation(start_rotation)
	trans_field.setSFVec3f(start_position)
	rotation_field.setSFRotation(start_rotation)


def run_robot(nn):
	if receiver.getQueueLength() > 0:
		receivedData = receiver.getData().decode("utf-8")
		sensor_data = eval(receivedData)
		receiver.nextPacket()

		nn_input = np.array([axis_right1.getSFVec3f()[0],
							 axis_right1.getSFVec3f()[1],
							 axis_right1.getSFVec3f()[2],

							 position_right1.getSFFloat(),

							 axis_right2.getSFVec3f()[0],
							 axis_right2.getSFVec3f()[1],
							 axis_right2.getSFVec3f()[2],

							 position_right2.getSFFloat(),

							 axis_left1.getSFVec3f()[0],
							 axis_left1.getSFVec3f()[1],
							 axis_left1.getSFVec3f()[2],

							 position_left1.getSFFloat(),

							 axis_left2.getSFVec3f()[0],
							 axis_left2.getSFVec3f()[1],
							 axis_left2.getSFVec3f()[2],
							 position_left2.getSFFloat(),

							 sensor_data[0],
							 sensor_data[1],
							 sensor_data[2],
							 sensor_data[3],
							 sensor_data[4],
							 sensor_data[5],
							 sensor_data[6],
							 sensor_data[7],
							 sensor_data[8]
							 ])

		output = nn.forward(nn_input).cpu().detach().numpy()

		axis_right1.setSFVec3f([output[0], output[1], output[2]])
		position_right1.setSFFloat(float(output[3]))
		axis_right2.setSFVec3f([output[4], output[5], output[6]])
		position_right2.setSFFloat(float(output[7]))
		axis_left1.setSFVec3f([output[8], output[9], output[10]])
		position_left1.setSFFloat(float(output[11]))
		axis_left2.setSFVec3f([output[12], output[13], output[14]])
		position_left2.setSFFloat(float(output[15]))

		# get velocity for roboter
		velocity = np.array([output[-7], output[-6], output[-5], output[-4]])

		# send velocity to supervisor fpr NN
		string_message = np.array2string(velocity, separator=',')
		string_message = string_message.encode("utf-8")
		emitter.send(string_message)


def fitness_function(weight):
	tensor_weight = torch.tensor(weight.astype(np.float32), requires_grad=False)
	nn = NeuralNetwork(input_size, output_size, tensor_weight)

	# start timer
	start_timer = supervisor.getTime()
	timer = 0.000

	while supervisor.step(timeStep) != -1:
		timer = supervisor.getTime() - start_timer

		run_robot(nn)

		if timer > time_for_scoring:
			break

	position_difference = calc_difference()
	reset_robot()
	# TODO: write fitness scoring
	return position_difference / 0.4


def calc_difference():
	current_pos = robot.getPosition()
	return abs(current_pos[0] - start_position[0])


def run_only_simulation(weight_matrix):
	tensor_weight = torch.tensor(weight_matrix.astype(np.float32), requires_grad=False)
	nn = NeuralNetwork(input_size, output_size, tensor_weight)

	while supervisor.step(timeStep) != -1:
		run_robot(nn)


def main():
	if not exists("weights.csv"):
		new_population = Population(output_size, input_size, fitness_function)
		best = new_population.run()

		np.savetxt("weights.csv", best.weight_matrix, delimiter=',')
	else:
		weight_matrix = np.loadtxt("weights.csv", delimiter=',')

		run_only_simulation(weight_matrix)


main()
