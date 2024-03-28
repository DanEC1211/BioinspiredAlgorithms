import numpy as np
import random
import bisect

knapsackCapacity = 30
numProducts = 7
populationSize = 10
generations = 50
crossoverProbability = 0.85
mutationProbability = 0.1

#Name products order [Love Potion, Skiving Snackbox, Extendable Ears, Decoy Detonators, Fever fudge, Puking Pastilles, Nosebleed Nougat]
productsWeights = [2, 5, 5, 4, 2, 1.5, 1]
productsCosts = [8, 6, 12, 10, 3, 2, 2]
#Maximum number of each available products 
productsMax =[10,10,10,10,10,10,10]
#Minimum number of each available products
productsMin = [3,2,0,0,0,0,0]

def generateChromosomes(numProducts, productsWeights, knapsackCapacity, productsMin, productsMax):
    chromosomes = []
    for _ in range(populationSize):
        while True:
            chromosome = [random.randint(productsMin[i], productsMax[i]) for i in range(numProducts)]
            totalWeight = sum(gene * weight for gene, weight in zip(chromosome, productsWeights))
            if totalWeight <= knapsackCapacity:
                break
        chromosomes.append(chromosome)
    return chromosomes

def selectChromosomes(chromosomes, accumulatedPercentages):
    selected = []
    while len(selected) < populationSize:
        direction = np.sign(np.random.uniform(-1, 1)) # Generate a random number between -1 and 1
        if direction >= 0: # If the direction is positive or zero, iterate from the start of the list
            r = random.random()
        else: # If the direction is negative, iterate from the end of the list
            r = 1 - random.random()
        # Use binary search to find the index
        index = bisect.bisect_left(accumulatedPercentages, r)
        if chromosomes[index] not in selected:
            selected.append(chromosomes[index])
    # Group the selected chromosomes into pairs
    pairs = [(selected[i], selected[i+1]) for i in range(0, len(selected), 2)]
    return pairs

def evaluateChromosomes(chromosomes, productsCosts):
    benefits = [sum([a*b for a,b in zip(chromosomes[i], productsCosts)]) for i in range(populationSize)]
    totalBenefit = sum(benefits)
    percentages = []
    accumulatedPercentages = []
    accumulatedPercentage = 0
    for benefit in benefits:
        percentage = benefit / totalBenefit
        percentages.append(percentage)
        accumulatedPercentage += percentage
        accumulatedPercentages.append(accumulatedPercentage)
    return accumulatedPercentages ,benefits#, percentages



chromosomes = generateChromosomes(numProducts, productsWeights, knapsackCapacity, productsMin, productsMax)
#print(chromosomes, results)

accumulatedPercentages, benefits = evaluateChromosomes(chromosomes, productsCosts)
print(chromosomes)
print(benefits)
print(selectChromosomes(chromosomes, accumulatedPercentages))
