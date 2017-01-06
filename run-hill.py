from job import run

run(jobName = "hill",
	inputs = [
		["x", [0,10] ], 
		["y", [0,10] ]
		],
	outputs = [
		["height", "max"]
		],
	numGenerations = 5,
	numPopulation = 5,
	algo = "GA")