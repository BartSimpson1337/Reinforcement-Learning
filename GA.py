import numpy as np
import pandas as pd   
import subprocess
import re


max_population = 5
max_generations = 2
max_parents = 2
max_offspring = max_population - max_parents


def Population():
    global max_population

    population = []

    i = 0
    while i < max_population:
        chromosome = []
        #Setting chromosome genes 
        chromosome.append(round(np.random.random(),2)) #epsilon
        chromosome.append(round(np.random.random(),2)) #alpha
        chromosome.append(round(np.random.random(),2)) #gamma
        population.append(chromosome)
        i += 1
    return population


def Fitness(population):
    global max_population

    accuracys = []
    i = 0
    while i < max_population:
        parameters = population[i]
        
        cmd_parameters = "-a epsilon="+str(parameters[0])+",alpha="+str(parameters[1])+",gamma="+str(parameters[2])
        byteOutput = subprocess.check_output("python pacman.py -q -p PacmanQAgent -x 2000 -n 2010 -l smallGrid "+cmd_parameters, shell=True)
        strOutput = byteOutput.decode('UTF-8').rstrip()
        match = re.search(r"\(([0-9]\.[0-9][0-9])\)", strOutput)  #Regular expression to extract the accuracy from command output
        accuracy = match.group(1)
        accuracys.append(float(accuracy))

        i += 1

    return accuracys


def Parents(population, fitness):
    global max_parents

    parents = []

    i = 0
    while i < max_parents:
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]

        chromosome = []
        chromosome.append(population[max_fitness_idx][0])
        chromosome.append(population[max_fitness_idx][1])
        chromosome.append(population[max_fitness_idx][2])
        parents.append(chromosome)

        fitness = np.delete(fitness, max_fitness_idx, 0)
        i += 1

    return parents


def Crossover(parents):
    global max_offspring

    crossover_point = len(parents[0])/2

    offsprings = []

    i = 0
    while i < max_offspring:
        #selecting parents to crossover 
        parent1  = parents[i%len(parents)]
        parent2 = parents[i%len(parents)]

        offspring = []
        for gene in range(len(parents[0])):
            
            if gene <= crossover_point:
                offspring.append(parent1[gene])
            else:
                offspring.append(parent2[gene])

        offsprings.append(offspring)
        i += 1
    return offsprings



def Mutation(crossover):

    for i in range(len(crossover)):
         #Generating a gene id to be mutated.
        gene_idx = np.random.randint(0, len(crossover[0]))
        #Saving current gene value
        current_value = crossover[i][gene_idx]

        while(True):
            new_value = round(np.random.random(),2)
            if current_value != new_value:
                break

            crossover[i][gene_idx] = new_value

    return crossover 



def NewPopulation(parents, offspring_mutation):
    
    population = []
    for i in range(len(parents)):
        population.append(parents[i])

    for i in range(len(offspring_mutation)):
        population.append(offspring_mutation[i])
    
    return population


def main():
    global max_generations
    global max_parents

    population = Population()

    #Current solution variables.
    score = None
    solution = None #Variable to keep in track the previous fitness value.

    i = 0
    while i < max_generations:
        fitness = Fitness(population)

         #--------------Final Solution variables---------------------
        score = max(fitness)

        for idx in range(len(fitness)):
            if fitness[idx] == score:
                solution = population[idx]
                break
        #--------------END-------------------------------------------

        parents = Parents(population, fitness)

        offspring_crossover = Crossover(parents)

        offspring_mutation = Mutation(offspring_crossover)
        
        #generating a new population.
        population = NewPopulation(parents, offspring_mutation)

        if score >= 0.80:
            break
        else:
            i += 1 

    print("Parameters: epsilon=%.2f, alpha=%.2f, gamma=%.2f" % (solution[0], solution[1], solution[2]))
    print("Accuracy: "+"{:.2f} %".format(score*100))
    print("Generation: %d" % (i))

main()
