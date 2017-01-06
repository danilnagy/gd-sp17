from src import job

jobDescription = {
	"jobName": "bridge",
	"inputsDef": [
		# { "name": "curvePoint1", "type": "continuous", "range": [0,10]},
		# { "name": "curvePoint2", "type": "continuous", "range": [0,10]},
		{ "name": "height1", "type": "continuous", "range": [1,5]},
		{ "name": "height2", "type": "continuous", "range": [1,5]},
		{ "name": "height3", "type": "continuous", "range": [1,5]},
		{ "name": "height4", "type": "continuous", "range": [1,5]},
		{ "name": "height5", "type": "continuous", "range": [1,5]},
		{ "name": "height6", "type": "continuous", "range": [1,5]},
		{ "name": "type1", "type": "categorical", "num": 4},
		{ "name": "type2", "type": "categorical", "num": 4},
		{ "name": "type3", "type": "categorical", "num": 4},
		{ "name": "type4", "type": "categorical", "num": 4},
		{ "name": "type5", "type": "categorical", "num": 4}
		],
	"outputsDef": [
		{ "name": "displacement", "type": "min"},
		{ "name": "material", "type": "min"},
		# { "name": "stress", "type": "min"},
		# { "name": "obstruction", "type": "constraint", "goal": ["less than", 1] }
		],
	"algo": "GA",
	"algoOptions": {
		"numGenerations": 25,
		"numPopulation": 50,
		"mutationRate": 0.03,
		"saveElites": 3
		},
	"jobOptions": {
		"screenshots": True
		}
	}

# job.createInputFile(jobDescription)
job.run(jobDescription)