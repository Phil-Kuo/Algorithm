import numpy as np
import matplot.pyplot as pyplot
import random
import copy
from gaIndividual import gaIndividual

class geneticAlgorithm:
    '''
    The class for genetic algorithm
    '''
    def __init__(self, populationSize, variablesDimension, boundaries, maxGen, params):
        '''
        populationSize:  种群数量 60
        variablesDimension:  变量维度 25
        boundaries: boundaries of variables 变量的边界 -600 600
        maxGen: termination condition  终止条件  1000
        params: algorithm required parameters, it is a list which is consisting of crossover rate, mutation rate, alpha
        算法所需的参数，它是由交叉率，变异率，alpha组成的列表
        0.9, 0.1, 0.5
        '''
        self.popSize = populationSize
        self.MAXGEN = maxGen
        self.vardim = variablesDimension
        self.bound = boundaries
        self.params = params
        self.population = []
        self.fitness = np.zeros((self.popSize, 1))
        self.trace = np.zeros((self.MAXGEN, 2))

    def initialize(self):
        '''
        initialize the population 初始化种群
        '''
        for i in range(0, self.popSize):
            ind = gaIndividual(self.vardim, self.bound)
            ind.generate()
            self.population.append(ind)
    
    def evaluate(self):
        '''
        evaluation of the population fitnesses
        评估种群适合度
        '''
        for i in range(0, self.popSize):
            self.population[i].calculateFitness()
            self.fitness[i] = self.population[i].fitness
    def solve(self):
        '''
        evolution process of genetic algorithm
        遗传算法的演化过程
        '''
        self.t = 0
        self.initialize()
        self.evaluate()
        best = np.max(self.fitness)
        bestIndex = np.argmax(self.fitness)
        self.best = copy.deepcopy(self.population[bestIndex])

        # 这一段没看懂
        self.averageFitneess = np.mean(self.fitness)
        self.trace[self.t, 0] = (1 - self.best.fitness) / self.best.fitness
        self.trace[self.t, 1] = (1 - self.averageFitneess) / self.averageFitneess
        print("Generation  %d: optimal function value is: %f; average function value is %f" % (self.t, self.trace[self.t, 0], self.trace[self.t, 1]))
        
        while (self.t < self.MAXGEN - 1): 
            self.t += 1 
            self.selectionOperation() 
            self.crossoverOperation() 
            self.mutationOperation() 
            self.evaluate() 
            best = np.max(self.fitness) 
            bestIndex = np.argmax(self.fitness) 
            if best > self.best.fitness: 
                self.best = copy.deepcopy(self.population[bestIndex]) 
                self.averageFitneess = np.mean(self.fitness)
                self.trace[self.t, 0] = (1 - self.best.fitness) / self.best.fitness
                self.trace[self.t, 1] = (1 - self.averageFitneess) / self.averageFitneess
            print("Generation %d: optimal function value is: %f; average function value is %f" % ( self.t, self.trace[self.t, 0], self.trace[self.t, 1])) print("Optimal function value is: %f; " % self.trace[self.t, 0]) 
            print ("Optimal solution is:") 
            print (self.best.chrom) 
            self.printResult()
        
    def selectionOperation(self):
        '''
        selection operation for Genetic Algorithm
        遗传算法的选择操作
        '''
        newPopulation = []
        totalFitness = np.sum(self.fitness)
        accuFitness = np.zeros((self.popSize, 1))

        sum1 = 0.
        for i in range(0, self.popSize):
            accuFitness[i] = sum1 + self.fitness[i] / totalFitness
            sum1 = accuFitness[i]
        
        for i in range(0, self.popSize):
            r = np.random.random()
            idx = 0
            for j in range(0, self.popSize-1):
                if j == 0 and r < accuFitness[j]:
                    idx = 0
                    break
                elif r >=accuFitness[j] and r < accuFitness[j + 1]:
                    idx = j + 1
                    break
            newPopulation.append(self.population[idx])
        self.population = newPopulation
    
    def crossoverOperation(self):
        '''
        crossover operation for genetic algorithm
        交叉操作
        '''
        newPopulation = []
        for i in range(0, self.popSize, 2):
            idx1 = np.random.randint(0, self.popSize - 1)
            idx2 = np.random.randint(0, self.popSize - 1)
            while idx1 = idx2:
                idx2 = np.random.randint(0, self.popSize - 1)
            newPopulation.append(copy.deepcopy(self.population[idx1]))
            newPopulation.append(copy.deepcopy(self.population[idx2]))
            r = np.random.random()
            if r < self.params[0]:
                crossPos = np.random.randint(1, self.vardim-1)
                for j in range(crossPos, self.vardim):
                    newPopulation[i].chrom[j] = newPopulation[i].chrom[j]*self.params[2]+(1-self.params[2])*newPopulation[i+1].chrom[j]
                    newPopulation[i+1].chrom[j] = newPopulation[i+1].chrom[j]*self.params[2]+(1-self.params[2])*newPopulation[i].chrom[j]
        self.population = newPopulation

    def mutationOperation(self):
        '''
        mutation operation for genetic algorithm
        变异操作。
        '''
        newPopulation = []
        for i in range(0, self.popSize):
            newPopulation.append(copy.deepcopy(self.population[i]))
            r = np.random.random()
            if r < self.params[1]:
                mutatePos = np.random.randint(0, self.vardim-1)
                theta = np.random.random()
                if theta > 0.5:
                    newPopulation[i].chrom[mutatePos] = newPopulation[i].chrom[mutatePos] - (newPopulation[i].chrom[mutatePos] - self.bound[0,mutatePos]) * (1 - np.random.random()**(1- self.t/self.MAXGEN))
                else:
                    newPopulation[i].chrom[mutatePos] = newPopulation[i].chrom[mutatePos] + (self.bound[1, mutatePos] - newPopulation[i].chrom[mutatePos])* (1 - random.random() ** (1 - self.t / self.MAXGEN))

        self.population = newPopulation
    
    def printResult(self): '''
        plot the result of the genetic algorithm
        画出结果
        ''' 
        x = np.arange(0, self.MAXGEN) 
        y1 = self.trace[:, 0] 
        y2 = self.trace[:, 1] 
        plt.plot(x, y1, 'r', label='optimal value') 
        plt.plot(x, y2, 'g', label='average value') 
        plt.xlabel("Iteration") 
        plt.ylabel("function value") 
        plt.title("Genetic algorithm for function optimization") 
        plt.legend() 
        plt.show()

if __name__ = "__main__":
    boundaries = np.tile([[-600],[600]],25)
    ga = geneticAlgorithm(60, 25, boundaries, 1000,[0.9, 0.1, 0.5])