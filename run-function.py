from src import job

job.run(
	jobName = "function",
	inputs = [
		{ "name": "x1", "type": "continuous", "range": [0,5] }, 
		{ "name": "x2", "type": "continuous", "range": [0,3] }
		],
	outputs = [
		{ "name": "y1", "type": "min"},
		{ "name": "y2", "type": "min"}
		],
	algo = "GA",
	options = {
		"numGenerations": 5,
		"numPopulation": 5
		}
	)