from job import run

run(jobName = "box",
	inputs = [
		["length", [0,10] ], 
		["width", [0,10] ], 
		["height", [0,10] ]
		],
	outputs = [
		["surface area", "min"],
		["volume",  "max"]
		],
	numGenerations = 5,
	numPopulation = 5,
	algo = "GA")