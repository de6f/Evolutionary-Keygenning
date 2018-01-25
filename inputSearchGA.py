#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import string
import time
from random import randint
from random import choice
from random import seed
from sys import stdout
from math import ceil
from sys import maxint

class BasicBlock:
    def __init__(self, name, nextBlocks=None, isVulnAPI=None):
        self.name = name
        self.nextBlocks = dict.fromkeys(nextBlocks, 0) if nextBlocks else None
        self.isVulnAPI = isVulnAPI
        self.isReached = 0

    def reached(self):
        self.isReached = 1

class gramEvol:
    def __init__(self, rep):
        self.grammar = dict()
        self.rep = rep
    def add(self, nonterm, rule):
        self.grammar.update({nonterm:rule})
    def generateStr(self, val):
        tmpList = list(self.rep)
        i = 0
        j = 0
        tmpStr = ''
        while i != (len(tmpList)) and j != (len(val)):
            if tmpList[i] in self.grammar:
                tmpRule = self.grammar[tmpList[i]]
                try:
                                        tmpList[i] = tmpRule[int(val[j]) % len(tmpRule)]
                except:
                    tmpList.append(tmpRule[int(val[j]) % len(tmpRule)])
                j += 1
            else:
                i += 1
            tmpStr = ''.join(tmpList)
            tmpList = list(tmpStr)
        return tmpStr

class InputGenerateGA(gramEvol):
    def init_population(self, popSize, passSize):
        tmpPop = []
        for g in range(popSize):
            tmpPop.append([randint(0,25) for p in range(passSize * 2)])
        return tmpPop

    def __init__(self, progName, passSize, bblocks,
                 mutationRate, crossingOverRate, popSize):
        gramEvol.__init__(self, 'S' * passSize)
        self.progName = progName
        self.passSize = passSize
        self.bblocks = bblocks
        self.mnum = mutationRate * passSize * 2 * popSize
        self.cnum = crossingOverRate * popSize
        self.population = self.init_population(popSize, passSize)
        self.popSize = popSize
        self.generation = 1
        self.lastStage = 0
        self.path = []

    def findStage(self, key):
        for b in self.bblocks:
            if b.name == key:
                return b

    def addStageBranch(self, stage):
        for s in self.bblocks:
            if s.name == stage.name:
                s = stage
                break

    def calcFitness(self):
        for genNum in range(len(self.population)):
            stagesNum = self.genomeOutput[genNum]
            currStage = self.findStage(stagesNum[0])
            tmpFitness = 1.0
            i = 1
            while i != len(stagesNum):
                if stagesNum[i] in currStage.nextBlocks:
                    tmpDiv = float(currStage.nextBlocks[stagesNum[i]])
                    tmpFitness *= 1.5/tmpDiv
                    currStage = self.findStage(stagesNum[i])
                i += 1
            self.fitnessList.append(tmpFitness)

    def applyPopulation(self):
        for genNum in range(len(self.population)):
            genome = self.population[genNum]
            serial = self.generateStr(genome)
            p = subprocess.Popen('./%s %s'% (self.progName, serial),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out, err = p.communicate()

            stdout.write("\rGirdi denemesi: %s "% serial)
            stdout.flush()

            lines = []
            for line in out.splitlines():
                lines.append(line.split(' ')[1].rstrip())
                retval = p.wait()
            p.stdout.close()

            self.genomeOutput[genNum] = lines

            i = 0
            stage = self.bblocks[0]
            while i+1 != len(lines):
                if stage.name == lines[i]:
                    i += 1
                    for key, value in stage.nextBlocks.iteritems():
                        if key == lines[i]:
                            stage.nextBlocks[key] += 1
                            self.addStageBranch(stage)
                            stage = self.findStage(key)

            for s in self.bblocks:
                if s.nextBlocks == None: continue
                tmpSum = 0
                for n in s.nextBlocks:
                    tmpSum += s.nextBlocks[n]
                if tmpSum == 0: continue
                for n in s.nextBlocks:
                    s.nextBlocks[n] /= float(tmpSum)

    def reproduceNextGen(self):
        getMaxFit = lambda: self.fitnessList.index(max(self.fitnessList))
        print '%d. nesil en iyi girdi: ( %s , %f )'% (self.generation,
                    self.generateStr(self.population[getMaxFit()]), max(self.fitnessList))

        # Yeni bireylerin seçimi
        rouletteWheel = []
        newPop = [self.population[getMaxFit()][:]]
        sumFitness = sum(self.fitnessList)
        for i in range(len(self.fitnessList)):
           if self.fitnessList[i] > 500: self.fitnessList[i] = 500
           rouletteWheel += [i] * int(round(self.fitnessList[i]))
        for i in range(self.popSize-1):
           newPop.append(self.population[choice(rouletteWheel)][:])

        # Çaprazlama - Tek noktadan
        for i in range(int(ceil(self.cnum))):
            a = randint(1, self.popSize-1)
            b = randint(1, self.popSize-1)
            c = randint(0, self.passSize*2-1)
            newPop[a][c:], newPop[b][c:] = newPop[b][c:], newPop[a][c:]

        # Mutasyon
        for i in range(int(ceil(self.mnum))):
            a = randint(1, self.popSize-1)
            b = randint(0, self.passSize*2-1)
            newPop[a][b] = randint(0,25)

        self.population[:] = newPop[:]

    def __call__(self):
        self.add('S', ['I', 'L', 'U'])
        self.add('U', list(string.ascii_uppercase))
        self.add('L', list(string.ascii_lowercase))
        self.add('I', list(string.digits))

        while True:
            seed(self.bblocks[0].nextBlocks.values()[0])
            for b in self.bblocks:
                if b.nextBlocks == None: break
                for n in b.nextBlocks:
                    b.nextBlocks[n] = 0

            self.genomeOutput = [None] * self.popSize
            self.fitnessList = []

            print ''
            self.applyPopulation()

            for genNum in range(self.popSize):
                progOutput = self.genomeOutput[genNum]
                if progOutput == None: continue
                for line in progOutput:
                    if line in self.path:
                        continue
                    else:
                        self.path.append(line)
            print '\nKeşfedilen bloklar: %s'% ' | '.join(self.path)

            if len(self.path) == len(self.bblocks):
                return

            self.calcFitness()
            self.reproduceNextGen()
            self.generation += 1



if __name__ == '__main__':
    progName = 'cr4ckm3'

    s0 = BasicBlock('0', ['1.1'])
    s11 = BasicBlock('1.1', ['2.1', '2.2'])
    s21 = BasicBlock('2.1', ['3.1'])
    s22 = BasicBlock('2.2', ['2.1', '3.2'])
    s31 = BasicBlock('3.1', ['4.1', '4.2', '4.3'])
    s32 = BasicBlock('3.2', ['4.4'])
    s41 = BasicBlock('4.1')
    s42 = BasicBlock('4.2', ['5.1'])
    s43 = BasicBlock('4.3', ['5.2'])
    s44 = BasicBlock('4.4', ['5.2'])
    s51 = BasicBlock('5.1')
    s52 = BasicBlock('5.2')
    bblocks = [s0, s11, s21, s22, s31, s32, s41, s42, s43, s44, s51, s52]

    mutationRate = 0.45
    crossingOverRate = 0.75
    popSize = 2000
    ga = InputGenerateGA(progName, 10, bblocks,
                    mutationRate, crossingOverRate, popSize)
    r = time.time()
    t = time.clock()
    ga()
    t = time.clock() - t
    r = time.time() - r
    print 'Çalışma süresi: %f sn'% r
    print 'Gerçek çalışma süresi: %f sn\n'% t
