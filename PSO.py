import random
import numpy as np 
import subprocess
import re
"""
    Initial PSO Attributes
"""
#This parameter affects the movement propagation given by the last velocity value.
W = 0.5 

#Accelaration coeficients 
c1 = 0.5    #C1 value gives the importance of personal best value
c2 = 0.9    #C2 is the importance of social best value.

target_error = 0.9  #Threshold accuracy 

n_iteractions = 5   #Number of iterations during the otimization
n_particles = 3    #Number of particles that will try to optimize the problem

#initial particle positions
particle_position_vector = np.random.random((n_particles,3)).round(decimals=2)

pbest_position = particle_position_vector   #initial pbest positions of each particles
pbest_fitness_value = np.zeros((n_particles,), dtype=float)

gbest_fitness_value = 0.0  #initial global best fitness within all particles 
gbest_position = np.zeros((3,), dtype=float)

velocity_vector = np.zeros((n_particles, 3), dtype=float)

def fitness(position):

    parameters = "-a epsilon="+str(position[0])+",alpha="+str(position[1])+",gamma="+str(position[2])
    byteOutput = subprocess.check_output("python pacman.py -q -p PacmanQAgent -x 2000 -n 2010 -l smallGrid "+parameters, shell=True)
    strOutput = byteOutput.decode('UTF-8').rstrip()
    match = re.search(r"\(([0-9]\.[0-9][0-9])\)", strOutput)  #Regular expression to extract the accuracy from command output
    accuracy = match.group(1)
    return float(accuracy)

interaction = 0
while interaction < n_iteractions:

    print("Interaction: %d" % (interaction))

    for i in range(n_particles):
        particle_fitness = fitness(particle_position_vector[i])

        print("Particle: %d, fitness %.2f%%, epsilon: %.2f, alpha: %.2f, gamma: %.2f" % (i, particle_fitness*100, particle_position_vector[i][0],particle_position_vector[i][1], particle_position_vector[i][2]))

        if(pbest_fitness_value[i] < particle_fitness):
            pbest_fitness_value[i] = particle_fitness
            pbest_position[i] = particle_position_vector[i]

        if(gbest_fitness_value < particle_fitness):
            gbest_fitness_value = particle_fitness
            gbest_position = particle_position_vector[i]
        
    if(gbest_fitness_value >= target_error):
        break

    for i in range(n_particles):
        #rand1 and rand2 are random numbers between 0 and 1, and they control the influence of each value: Social and individual
        rand1 = random.random()
        rand2 = random.random()

        #calculating the new position and the new velocity
        new_velocity = (W*velocity_vector[i]) + (c1*rand1) * (pbest_position[i] - particle_position_vector[i]) + (c2*rand2) * (gbest_position-particle_position_vector[i])
        
        new_position = new_velocity + particle_position_vector[i]

        for p in range(len(new_position)):
            #Setting border limits between 0 and 1 
            if (new_position[p] > 1):
                new_position[p] = 1 
            if (new_position[p] < 0):
                new_position[p] = 0
    
        #Updating velocities and positions vector
        velocity_vector[i] = new_velocity.round(decimals=2)
        particle_position_vector[i] = new_position.round(decimals=2)
 
    interaction = interaction + 1

print("Best parameters: epsilon=%.2f, alpha=%.2f, gamma=%.2f with an accuracy of: %.2f%%" % (gbest_position[0], gbest_position[1], gbest_position[2], gbest_fitness_value*100))
