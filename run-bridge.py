from src import job

jobDescription = {
	"jobName": "bridge",
	"inputsDef": [
		# { "name": "curvePoint1", "type": "continuous", "range": [0,10]},
		# { "name": "curvePoint2", "type": "continuous", "range": [0,10]},
		{ "name": "height1", "type": "continuous", "range": [0,5]},
		{ "name": "height2", "type": "continuous", "range": [0,5]},
		{ "name": "height3", "type": "continuous", "range": [0,5]},
		{ "name": "height4", "type": "continuous", "range": [0,5]},
		{ "name": "height5", "type": "continuous", "range": [0,5]},
		{ "name": "height6", "type": "continuous", "range": [0,5]},
		{ "name": "type1", "type": "categorical", "num": 4},
		{ "name": "type2", "type": "categorical", "num": 4},
		{ "name": "type3", "type": "categorical", "num": 4},
		{ "name": "type4", "type": "categorical", "num": 4},
		{ "name": "type5", "type": "categorical", "num": 4}
		],
	"outputsDef": [
		{ "name": "displacement", "type": "objective", "goal": "min"},
		{ "name": "material", "type": "objective", "goal": "min"},
		# { "name": "stress", "type": "min"},
		{ "name": "displacement", "type": "constraint", "goal": "less than 0.005" }
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 100,
		"numPopulation": 100,
		"mutationRate": 0.05,
		"saveElites": 4
		},
	"jobOptions": {
		"screenshots": True
		}
	}

# job.createInputFile(jobDescription)
job.run(jobDescription)