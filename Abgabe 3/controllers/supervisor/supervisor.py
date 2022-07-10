from controller import Motor, Supervisor, Node
from .population import Population

input_size = 1
output_size = 1


def calc_difference():
	current_pos = robot.getPosition()
	return current_pos[0] - start_position[0]


def main():
	new_population = Population(1, 1, calc_difference)
	print(new_population)


supervisor = Supervisor()
# emitter = supervisor.getDevice("emitter")
timestep = int(supervisor.getBasicTimeStep())
robot = supervisor.getFromDef("Robot")

# nodes for translation and rotation field
trans_field = robot.getField("translation")
rotation_field = robot.getField("rotation")

# get initial start position for reset method
start_rotation = rotation_field.getSFRotation()
start_position = robot.getPosition()

main()
