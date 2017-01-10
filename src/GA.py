import random
import math
from kung import getDominantSet

class Design:
    
    def __init__(self, genNum, desNum, id):
        self.genNum = genNum
        self.desNum = desNum
        self.id = id
        self.inputs = []
        self.objectives = []
        self.feasible = True
        self.penalty = 0
        self.rank = 0

    def get_id(self):
        return self.id

    def get_genNum(self):
        return self.genNum

    def get_desNum(self):
        return self.desNum
    
    def set_inputs(self, inputs):
        self.inputs = inputs

    def get_inputs(self):
        return self.inputs

    def set_outputs(self, outputs, outputsDef, usingConstraints):
        if usingConstraints:
            for i,_o in enumerate(outputs):
                if outputsDef[i]["type"] == "objective":
                    self.objectives.append(_o)
                elif outputsDef[i]["type"] == "constraint":
                    goal = outputsDef[i]["goal"].split(" ")
                    goal_def = " ".join(goal[:-1])
                    goal_val = float(goal[-1])

                    if goal_def == "less than":
                        if _o > goal_val:
                            self.penalty += 1
                            self.feasible = False
                    elif goal_def == "greater than":
                        if _o < goal_val:
                            self.penalty += 1
                            self.feasible = False
                    elif goal_def == "equals":
                        if _o != goal_val:
                            self.penalty += 1
                            self.feasible = False
        else:
            self.objectives = outputs

    def get_objectives(self):
        return self.objectives

    def get_feasibility(self):
        return self.feasible

    def get_penalty(self):
        return self.penalty

    def update_rank(self, var):
        self.rank = var

    def get_rank(self):
        return self.rank
    
    def crossover(self, partner, inputsDef, genNum, desNum, idNum):
        child = Design(genNum, desNum, idNum)

        childInputs = []
        
        for i in range(len(self.inputs)):
            if inputsDef[i]["type"] == "continuous":
                # random in between
                fac = random.random()
                childInputs.append( ( (partner.get_inputs()[i] - self.get_inputs()[i]) * fac) + self.get_inputs()[i] )
            elif inputsDef[i]["type"] == "categorical":
                # coin flip
                childInputs.append( self.get_inputs()[i] if random.random() > 0.5 else partner.get_inputs()[i] )
            elif inputsDef[i]["type"] == "sequence":
                # coin flip on each value of sequence
                a = self.get_inputs()[i]
                b = partner.get_inputs()[i]
                newSequence = [a[j] if random.random() > 0.5 else b[j] for j in range(len(a))]
                childInputs.append( newSequence )

        child.set_inputs(childInputs)
        
        return child
    
    def mutate(self, inputsDef, mutationRate):
        for i in range(len(self.inputs)):
            # mutation based on probability
            if random.random() < mutationRate:
                if inputsDef[i]["type"] == "continuous":
                    # jitter input based on normal distribution
                    mutation = self.inputs[i] + random.gauss(0,.1)
                elif inputsDef[i]["type"] == "categorical":
                    # random assignment
                    mutation = int(math.floor(random.random() * inputsDef[i]["num"]))
                elif inputsDef[i]["type"] == "sequence":
                    # random assignment for randomly chosen value in sequence
                    newSequence = list(self.inputs[i])
                    for j in range(len(newSequence)):
                        if random.random() < inputsDef[i]["mutationRate"]:
                            newSequence[j] = int(math.floor(random.random() * inputsDef[i]["depth"]))
                    mutation = newSequence

                print "mutation : ", self.desNum, "/", str(i), ":", self.inputs[i], "->", mutation
                self.inputs[i] = mutation


def rank(population, outputsDef, g, numGenerations, usingConstraints):

    designs = []
    for i, des in enumerate(population):
        designs.append({'id': i, 'scores': des.get_objectives()})

    objectiveGoals = [x["goal"] for x in outputsDef if x["type"] == "objective"]

    validSet = [x for x in designs if len(x['scores']) == len(objectiveGoals)]

    dom = []
    ranking = []

    P = validSet

    while len(P) > 0:
        ranking.append([x['id'] for x in getDominantSet(P, objectiveGoals)])
        dom = dom + ranking[-1]
        P = [x for x in validSet if x['id'] not in dom]

    ranking.reverse()

    constraintPenalties = [( ( (numGenerations - g) / float(numGenerations) ) ** x.get_penalty() ) for x in population]

    if usingConstraints:
        print "Constraint penalties:", constraintPenalties

    rankingOut = [0] * len(designs)
    for i, ids in enumerate(ranking):
        for id in ids:
            rankingOut[id] = int(round( (i + 1) * constraintPenalties[id] ) )

    return rankingOut


def testRanking():

    outputsDef = [
        { "name": "y1", "type": "min"},
        { "name": "y2", "type": "min"}
        ]

    performance = [
        {'id': 0, 'scores': [0, 4]},
        {'id': 1, 'scores': [1, 4]},
        {'id': 2, 'scores': [2, 4]},
        {'id': 3, 'scores': [4, 4]},
        {'id': 4, 'scores': [1, 3]},
        {'id': 5, 'scores': [2, 3]},
        {'id': 6, 'scores': [3, 3]},
        {'id': 7, 'scores': [2, 2]},
        {'id': 8, 'scores': [3, 2]},
        {'id': 9, 'scores': [4, 2]},
        {'id': 10, 'scores': [3, 1]},
        {'id': 11, 'scores': [4, 1]},
        {'id': 12, 'scores': [4, 0]},
        ]

    print rank(performance, outputsDef)

# testRanking()