from controller import Motor, Supervisor, Node, Emitter, Receiver
#from robot.neural_network import NeuralNetwork
from population import Population
import json

input_size = 1
output_size = 1
time_for_scoring = 10  # in Sekunden

supervisor = Supervisor()
emitter = supervisor.getDevice("emitter")
timeStep = int(supervisor.getBasicTimeStep())
robot = supervisor.getFromDef("Robot")

# nodes for translation and rotation field
trans_field = robot.getField("translation")
rotation_field = robot.getField("rotation")

param_right1= supervisor.getFromDef("right_arm1")
axis_right1= param_right1.getField("axis")
param_right2= supervisor.getFromDef("right_arm2")
axis_right2= param_right2.getField("axis")
position_right1= param_right1.getField("position")
position_right2= param_right2.getField("position")


param_left1 = supervisor.getFromDef("left_arm1")
axis_left1= param_left1.getField("axis")
param_left2 = supervisor.getFromDef("left_arm2")
axis_left2= param_left2.getField("axis")
position_left1= param_left1.getField("position")
position_left2= param_left2.getField("position")
#axis_right.setSFVec3f([0.0,0.0,1.0])
#axis_right.getSFVec3f()


# get initial start position for reset method
start_rotation = rotation_field.getSFRotation()
start_position = robot.getPosition()


# reset robot to intial point
def reset_robot():
	trans_field.setSFVec3f(start_position)
	rotation_field.setSFRotation(start_rotation)
	trans_field.setSFVec3f(start_position)
	rotation_field.setSFRotation(start_rotation)


def fitness_function(weight):
	# weight is a single weight matrix of one individual
	weight_json = json.dumps(weight.tolist())
	emitter.send(weight_json)

	# start timer
	start_timer = supervisor.getTime()
	timer = 0.000

	while supervisor.step(timeStep) != -1:
		timer = supervisor.getTime() - start_timer

		if timer > time_for_scoring:
			break

	position_difference = calc_difference()

	# TODO: write fitness scoring
	return position_difference / 0.7


def calc_difference():
	current_pos = robot.getPosition()
	return current_pos[0] - start_position[0]


def main():
	new_population = Population(output_size, input_size, fitness_function)
	print(new_population)




main()
