import numpy as np
import objFunction

class gaIndividual:
    '''
    individual of genetic algorithm
    个体的遗传算法
    '''
    def __init__(self, variableDimension, boudaries):
        self.vardim = variableDimension
        self.bound = boudaries
        self.fitness = 0.

    def generate(self):
        '''
        generate a random chromsome for genetic algorithm
        为遗传算法生成一个随机染色体
        '''
        len = self.vardim
        rnd = np.random.random(size = len)
        self.chrom = np.zeros(len)
        for i in range(0, len):
            self.chrom[i] = self.bound[0, i]+(self.bound[1,i]-self.bound[0,i]*rnd[i])
    
    def calculateFitness(self):
        '''
        calculate the fitness of the chromsome
        计算染色体的适应性
        '''
        self.fitness = objFunction.grieFunc(self.vardim, self.chrom, self.bound)