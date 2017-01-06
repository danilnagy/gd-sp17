from src import job

job.run(
	jobName = "grid",
	inputsDef = [
		{ "name": "code", "type": "sequence", "length": 25, "depth": 3, "mutationRate": 0.5}
		],
	outputsDef = [
		{ "name": "target", "type": "min"}
		],
	algo = "GA",
	algoOptions = {
		"numGenerations": 25,
		"numPopulation": 25,
		"mutationRate": 0.1,
		"saveElites": 1
		},
	options = {
		"screenshots": True
		}
	)