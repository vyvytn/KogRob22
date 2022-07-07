from controller import Motor, Supervisor, Node
from Generation import Generation, Genotype
# create the Robot instance.

#Generation = Generation(Genotype(40))
supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())
#emitter = supervisor.getEmitter("emitter")
robot= supervisor.getFromDef("Robot")
trans_field=robot.getField("translation")
rot_field = robot.getField("rotation")
start_rot = rot_field.getSFRotation()
start_pos=robot.getPosition()
#start_rot=robot.getRotation()

def fitness_function():
    fitness=0
    cur_pos=robot.getPosition()

def reset_robot():
    trans_field.setSFVec3f(start_pos)
    rot_field.setSFRotation(start_rot)
    trans_field.setSFVec3f(start_pos)
    rot_field.setSFRotation(start_rot)
def open_file(file):

    pass
    
def start_loop():
    i=0
    while supervisor.step(timestep) != -1:
        i+=1
        print('POSITION',robot.getPosition())
    
       
       
        
start_loop()    
# Enter here exit cleanup code.
