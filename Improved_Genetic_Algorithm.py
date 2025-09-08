from CNF_Creator import *
import random, time
import numpy as np

START_TIME = time.time()
NO_OF_VARIABLES = 50
POPULATION_SIZE = 20
END_TIME = 45
MUTATION_RATE = 0.1
POINT_MUTATION_RATE = 0.1
ELITISM_RATE = 0.60
LAST_CHANCE = 40000

cnf_c = CNF_Creator(n = NO_OF_VARIABLES)

#NO_OF_CLAUSES = 175
#random_sentence = cnf_c.CreateRandomSentence(m = NO_OF_CLAUSES)

random_sentence = cnf_c.ReadCNFfromCSVfile()
NO_OF_CLAUSES = len(random_sentence)

fitness_cache = {}

def time_remaining():
    
    right_now = time.time() - START_TIME
    return right_now < END_TIME

def fitness(state):
    
    key = tuple(state)
    satisfied = 0
    
    if key in fitness_cache:
        return fitness_cache[key]
    
    for clause in random_sentence:
        
        if any(((literal > 0 and state[literal - 1]) or (literal < 0 and not state[-literal - 1])) for literal in clause):
            
            satisfied += 1
    
    score = (satisfied / NO_OF_CLAUSES) * 100
    fitness_cache[key] = score
    return score

def local_search_bit_flipping(individual):
    
    current_individual = individual.copy()
    current_fitness = fitness(current_individual)
    improved = True
    
    while improved:
        
        improved = False
        
        for i in range(NO_OF_VARIABLES):
            
            current_individual[i] = 1 - current_individual[i]
            new_fitness = fitness(current_individual)
            
            if new_fitness > current_fitness:
        
                current_fitness = new_fitness
                improved = True
                
            else:
                
                current_individual[i] = 1 - current_individual[i]
    
    return current_individual

def reproduce(parent1, parent2):
    
    n = len(parent1)
    c = random.randint(1, n - 1)
    return parent1[:c] + parent2[c:]

def mutate(individual, rate_of_mutation):
    
    for i in range(NO_OF_VARIABLES):
        
        if random.random() < rate_of_mutation:
            
            individual[i] = random.randint(0, 1)
            
    return individual

def weighted_random_choices(population, weights, k = 2):
    
    return random.choices(population, weights = weights, k = k)

def progress_stopped(best_fitness_history, max_iterations = LAST_CHANCE):
    
    if len(best_fitness_history) < max_iterations:
        
        return False
    
    past_fitness = best_fitness_history[-max_iterations]
    current_fitness = best_fitness_history[-1]
    
    return current_fitness <= past_fitness

def genetic_algorithm(population):
    
    no_of_iterations = 0
    best_fitness_history = []
    
    while time_remaining():
        
        no_of_iterations += 1
        fitness_scores = [fitness(ind) for ind in population]
        
        sorted_pop_with_fitness = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
        sorted_population = [ind for ind, _ in sorted_pop_with_fitness]
        sorted_fitness = [fit for _, fit in sorted_pop_with_fitness]
        
        elite_count = int(POPULATION_SIZE * ELITISM_RATE)
        next_population = sorted_population[:elite_count].copy()
        
        for i in range(min(3, elite_count)):
            
            next_population[i] = local_search_bit_flipping(next_population[i])
        
        remaining_count = POPULATION_SIZE - elite_count
        
        for i in range(remaining_count):
    
            state_1, state_2 = weighted_random_choices(sorted_population, sorted_fitness, k = 2)
            new_state = reproduce(state_1, state_2)
            
            if random.random() < MUTATION_RATE:
                
                new_state = mutate(new_state, POINT_MUTATION_RATE)
            
            next_population.append(new_state)
        
        population = next_population
        best_state = max(population, key=fitness)
        best_score = fitness(best_state)
        
        best_fitness_history.append(best_score)
        
        #if no_of_iterations % 1000 == 0:
            
            #print(f"Iteration {no_of_iterations}: Best fitness = {best_score:.2f}%")
            
        if progress_stopped(best_fitness_history, max_iterations = LAST_CHANCE):
            
            #print(f"No improvement in last 10000 iterations. Stopping at iteration {no_of_iterations}")
            #print(f"Best fitness achieved: {best_score:.2f}%")
            return best_state
        
        if best_score == 100:
            
            #print(f"Number of iterations: {no_of_iterations}")
            return best_state
    
    #print(f"Number of iterations: {no_of_iterations}")
    return best_state

def random_population(size, variables):
    
    return np.random.randint(0, 2, size = (size, variables)).tolist()

def main():
    
    population = random_population(size = POPULATION_SIZE, variables = NO_OF_VARIABLES)
    good_state = genetic_algorithm(population)
    
    ans = fitness(good_state)
    #print(f"Fitness value of best model: {ans:.2f}%")
    
    current_time = time.time() - START_TIME
    #print(f"Time taken: {current_time:.2f} seconds")
    
    best_model = []
    
    for i in range(0, NO_OF_VARIABLES):
        
        best_model.append((i + 1) if good_state[i] == 1 else -1 * (i + 1))
    
    print('Number of clauses in CSV file : ',NO_OF_CLAUSES)
    print('Best model : ', best_model)
    print('Fitness value of best model :', ans)
    print(f"Time taken: {current_time:.2f} seconds")

if __name__=='__main__':
    
    main()