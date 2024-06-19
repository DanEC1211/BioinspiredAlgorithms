import numpy as np
from colorama import Fore, init

init() 

def objective_function(x, y):
    return x**2 + y**2 + 25 * (np.sin(x) + np.sin(y))

def initialize_bees(swarm_size, lower_bound, upper_bound):
    return np.random.uniform(lower_bound, upper_bound, (swarm_size, 2))

def evaluate_bees(bees):
    return np.array([objective_function(x, y) for x, y in bees])

def update_bee_position(bee, lower_bound, upper_bound):
    new_bee = bee + np.random.uniform(-1, 1, bee.shape)
    new_bee = np.clip(new_bee, lower_bound, upper_bound)
    return new_bee

def calculate_selection_probabilities(fitness):
    normalized_fitness = np.zeros_like(fitness)
    for i in range(len(fitness)):
        if fitness[i] >= 0:
            normalized_fitness[i] = 1 / (1 + np.abs(fitness[i]))
        else:
            normalized_fitness[i] = 1 + np.abs(fitness[i])
    total_fitness = np.sum(normalized_fitness)
    probabilities = normalized_fitness / total_fitness
    return probabilities

def run_algorithm(swarm_size=40, worker_bees=20, observer_bees=20, limit_scout=5, limit_convergence=10, iterations=50, lower_bound=-5, upper_bound=5, log=False):
    swarm = initialize_bees(swarm_size, lower_bound, upper_bound)
    fitness = evaluate_bees(swarm)
    
    trial_counters = np.zeros(swarm_size, dtype=int)  
    convergence_counter = 0  

    for iteration in range(iterations):
        improved_bees = 0

        for i in range(worker_bees):
            new_bee = update_bee_position(swarm[i], lower_bound, upper_bound)
            new_fitness = objective_function(new_bee[0], new_bee[1])
            if new_fitness < fitness[i]:
                swarm[i] = new_bee
                fitness[i] = new_fitness
                improved_bees += 1
                trial_counters[i] = 0  
            else:
                trial_counters[i] += 1  
        probabilities = calculate_selection_probabilities(fitness[:worker_bees])
        for _ in range(observer_bees):
            selected_index = np.random.choice(worker_bees, p=probabilities)
            selected_bee = swarm[selected_index]
            new_bee = update_bee_position(selected_bee, lower_bound, upper_bound)
            new_fitness = objective_function(new_bee[0], new_bee[1])

            if new_fitness < fitness[selected_index]:
                swarm[selected_index] = new_bee
                fitness[selected_index] = new_fitness
                improved_bees += 1
                trial_counters[selected_index] = 0 
            else:
                trial_counters[selected_index] += 1 

        for i in range(swarm_size): 
            if trial_counters[i] >= limit_scout:
                swarm[i] = initialize_bees(1, lower_bound, upper_bound)[0]  
                fitness[i] = objective_function(swarm[i][0], swarm[i][1])
                trial_counters[i] = 0  

        if improved_bees == 0:  
            convergence_counter += 1
        else:
            convergence_counter = 0

        if log:
            if improved_bees > 0:
                print(Fore.GREEN + f"[Iteración {iteration+1}] Estado: Mejora" + Fore.RESET)
            else:
                print(Fore.YELLOW + f"[Iteración {iteration+1}] Estado: Sin cambios" + Fore.RESET)
            print("------------------------------------------------")
            print(Fore.CYAN + "Balance:" + Fore.RESET + f" {Fore.RED}{improved_bees}{Fore.RESET} abejas mejoraron su posición")
            if improved_bees > 0:
                improved_bee_indices = np.where(np.array(trial_counters) == 0)[0]  # Índices de abejas que mejoraron
                print(Fore.CYAN + "Detalle:" + Fore.RESET + f" Abejas {Fore.RED}{', '.join(str(i+1) for i in improved_bee_indices)}{Fore.RESET} mejoraron su posición")
            print("------------------------------------------------")

        if convergence_counter >= limit_convergence:
            if log:
                print(Fore.BLUE + f"Convergencia detectada en la iteración {iteration+1} después de {limit_convergence} iteraciones sin mejoras consecutivas." + Fore.RESET)
            break

    best_bee = swarm[np.argmin(fitness)]
    best_fitness = np.min(fitness)

    print(Fore.CYAN + "Mejor posición:" + Fore.RESET + f" {Fore.RED}{best_bee}{Fore.RESET}")
    print(Fore.CYAN + "Mejor fitness:" + Fore.RESET + f" {Fore.RED}{best_fitness}{Fore.RESET}")

run_algorithm(log=True)
 