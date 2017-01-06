from src import job

job.run(
	jobName = "cat",
	inputsDef = [
		{ "name": "x1", "type": "continuous", "range": [0,5] }, 
		{ "name": "x2", "type": "categorical", "num": 4 }
		],
	outputsDef = [
		{ "name": "y1", "type": "min"},
		{ "name": "y2", "type": "min"}
		],
	algo = "GA",
	options = {
		"numGenerations": 15,
		"numPopulation": 15
		}
	)