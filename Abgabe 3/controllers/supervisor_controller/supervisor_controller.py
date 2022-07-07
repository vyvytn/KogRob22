from controller import Motor, Supervisor, Node, Emitter, Receiver
from Generation import Generation
import json

#calc difference of x values from robot.getPosition
def fitness_function():
    fitness=0
    cur_pos=robot.getPosition()
    return cur_pos[0]-start_pos[0]

#reset robot to intial point
def reset_robot():
    trans_field.setSFVec3f(start_pos)
    rot_field.setSFRotation(start_rot)
    trans_field.setSFVec3f(start_pos)
    rot_field.setSFRotation(start_rot)


"""
fitness function has several tasks
1: calc fitness score based on x value of robot.position within 10 sec
2: emit SINGLE weight matrix of calculated fitness of individual to walking.py (individual robot controller)

this function will be passed to Generation/Poupulation class
"""
def calc_fitness_weight(weight):

    #weight is a single weight matrix of one individual
    weightJSON = json.dumps(weight.tolist())
    emitter.send(weightJSON)
    
    #start 10 sec timer
    start_timer = supervisor.getTime()
    timer = 0.000

    fitness=0
    individual_fitness=0

    #robot loop
    while supervisor.step(timestep) != -1:
        timer= supervisor.getTime() - start_timer

        #let robot walk for just 10 sec and then break
        if timer >10:
            break

        #walked distance of robot
        individual_fitness=fitness_function()

        #score walked distance
        if individual_fitness >0.7:
                fitness+=4
        elif individual_fitness > 0.5:
                fitness+=3        
        elif individual_fitness > 0.3:
                fitness+=2    
        elif individual_fitness < 0.1:
                fitness+=0    

    return fitness

def main():

    #intialize Generation/population class; pass fitness function from above
    gen=Generation(calc_fitness_weight)

    """
    TODO: returns best weight matrix
    best_weight_matrix=gen.reproduce()
    """

    """
    TODO: 
    f = open('weights', 'w')
    weightsJSON = json.dumps(best_weights.tolist())
    f.write(weightsJSON)
    emitter.send(weightsJSON)
    """

    #tidy up
    reset_robot()


# create the Robot instance and emitter
supervisor = Supervisor()
emitter=supervisor.getDevice("emitter")
timestep = int(supervisor.getBasicTimeStep())
robot= supervisor.getFromDef("Robot")

# nodes for translation and rotation field
trans_field=robot.getField("translation")
rot_field = robot.getField("rotation")

#get initial start position for reset method
start_rot = rot_field.getSFRotation()
start_pos=robot.getPosition()
    
        
main()