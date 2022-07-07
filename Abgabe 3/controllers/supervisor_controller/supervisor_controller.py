from controller import Motor, Supervisor, Node, Emitter, Receiver
from Generation import Generation
from Genotype import Genotype
import json
def fitness_function():
    fitness=0
    cur_pos=robot.getPosition()
    return cur_pos[0]-start_pos[0]

def reset_robot():
    trans_field.setSFVec3f(start_pos)
    rot_field.setSFRotation(start_rot)
    trans_field.setSFVec3f(start_pos)
    rot_field.setSFRotation(start_rot)
    
def open_file(file):
    pass
    
def calc_fitness_weights(weights):

    weightsJSON = json.dumps(weights.tolist())
    emitter.send(weightsJSON)
    
    #start 10 sec timer
    start_timer = supervisor.getTime()
    timer = 0.000
    
    individual_fitness=0
    #robo loop
    while supervisor.step(timestep) != -1:
        timer= supervisor.getTime() - start_timer
        
        #let robo walk for just 10 sec
        if timer >10:
            break
        individual_fitness=fitness_function()
    return individual_fitness
       
def main():
    #run generation and get best weight out of it
    best_weights =  gen.reproduce()
    #emit best weight to Neural Network 
    f = open('weights', 'w')
    weightsJSON = json.dumps(best_weights.tolist())
    f.write(weightsJSON)
    emitter.send(weightsJSON)

    #tidy up
    reset_robot()

emitter=Emitter
genotype=Genotype(40)
gen=Generation(genotype, calc_fitness_weights)
gen.init_gen()
# create the Robot instance.
supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())
#emitter = supervisor.getEmitter("emitter")
robot= supervisor.getFromDef("Robot")
trans_field=robot.getField("translation")
rot_field = robot.getField("rotation")
start_rot = rot_field.getSFRotation()
start_pos=robot.getPosition()
    
        
main()