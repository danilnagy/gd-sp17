from GA import Design, rank
from util import *


def run(jobDescription):

	try:
		jobName, inputsDef, outputsDef, algo, algoOptions, jobOptions = checkJobDescription(jobDescription)
	except TypeError:
		print "error loading job description"
		return

	paths, meta = init(jobName)

	print "Starting", algo, "algorithm..."

	if algo == "GA":
		error = runGA(inputsDef, outputsDef, algoOptions, jobOptions, paths, meta)
		if error is not None:
			print "error:", error

	elif algo == "random":
		error = runRandom(inputsDef, outputsDef, algoOptions, jobOptions, paths, meta)
		if error is not None:
			print "error:", error

	cleanup(paths["local"])


def runGA(inputsDef, outputsDef, algoOptions, jobOptions, paths, meta):

	# create results file header
	header = []
	header.append("id")
	header.append("generation")

	for _i in inputsDef:
		header.append("in_" + _i["name"])
	for _o in outputsDef:
		header.append(_o["type"] + "_" + _o["name"])

	with open(paths["results"], 'a') as f:
		f.write(",".join(header))

	# load options
	numGenerations = algoOptions["numGenerations"]
	numPopulation = algoOptions["numPopulation"]
	mutationRate = algoOptions["mutationRate"]
	saveElites = algoOptions["saveElites"]

	# initialise id
	idNum = 0

	# create initial population of designs
	population = []
	for i in range(int(numPopulation)):
		population.append(Design(0, i, idNum))
		idNum += 1

	# set random inputs for first generation
	for des in population:
		newInputs = []
		for _i in inputsDef:
			newInputs.append(create_input(_i))
		des.set_inputs(newInputs)

	for g in range(numGenerations):

		# for each design, calculate output metrics
		for des in population:

			meta, outputs = computeDesign(des.get_id(), des.get_inputs(), jobOptions, paths, meta)
			if outputs is None:
				return "model unresponsive"
			des.set_outputs(outputs)

			print des.get_genNum(), "/", des.get_desNum(), ":", outputs
			
			with open(paths["results"], 'a') as f:
				f.write("\n" + ",".join([str(x) for x in ([des.get_id(),des.get_genNum()] + printFormat(des.get_inputs(), inputsDef) + outputs)]))

		# generate performance set of id and objective values (scores)
		performance = []
		for i, des in enumerate(population):
			performance.append({'id': i, 'scores': des.get_outputs()})
		
		# compute ranking for population (higher value is better performance)
		ranking = rank(performance, outputsDef)
		print "Generation ranking:", ranking

		# add designs to mating pool based on ranking
		matingPool = []
		for i, order in enumerate(ranking):
			for j in range(order):
				matingPool.append(population[i])

		children = []

		# get elites
		elites = [i[0] for i in sorted(enumerate(ranking), key=lambda x:x[1])][-saveElites:]
		print "elite(s):", elites

		# add elites to next generation
		for i, eliteNum in enumerate(elites):
			child = Design(g+1, i, idNum)
			child.set_inputs(population[eliteNum].get_inputs())
			children.append(child)
			idNum += 1

		for i in range(len(population)-saveElites):				
			parentA = matingPool[random.choice(range(len(matingPool)))]
			parentB = matingPool[random.choice(range(len(matingPool)))]

			child = parentA.crossover(parentB, inputsDef, g+1, saveElites+i, idNum)
			child.mutate(inputsDef, mutationRate)
			children.append(child)
			idNum += 1

		population = children


def runRandom(inputsDef, outputsDef, algoOptions, jobOptions, paths, meta):

	# create results file header
	header = []
	header.append("id")

	for _i in inputsDef:
		header.append("in_" + _i["name"])
	for _o in outputsDef:
		header.append(_o["type"] + "_" + _o["name"])

	with open(paths["results"], 'a') as f:
		f.write(",".join(header))

	# load options
	numPopulation = algoOptions["numPopulation"]

	for idNum in range(numPopulation):

		newInputs = []
		for _i in inputsDef:
			newInputs.append(create_input(_i))

		meta, outputs = computeDesign(idNum, newInputs, jobOptions, paths, meta)
		if outputs is None:
			return "model unresponsive"

		print idNum, ":", outputs
		
		with open(paths["results"], 'a') as f:
			f.write("\n" + ",".join([str(x) for x in ([idNum] + printFormat(newInputs, inputsDef) + outputs)]))