import os
import random
import time
from shutil import copyfile
import pickle

localFolder = os.path.dirname(os.path.realpath(__file__)) + "\\"

inputFile = localFolder + "inputs.txt"
outputFile = localFolder + "outputs.txt"

jobID = "_" + time.strftime("%y%m%d_%H%M%S", time.localtime())
print "Session started:", jobID

os.makedirs(jobID)
jobFolder = localFolder + jobID + "\\"
os.makedirs(jobFolder + "images")
os.makedirs(jobFolder + "lib")

for f in ["explorer.sh", "index.html", "lib\\d3.v3.js"]:
	copyfile(localFolder + "src\\" + f, jobFolder + f)

meta = {"jobID": jobID}

resultsFile = jobFolder + "results.csv"

def run(inputs, outputs, generations, population):

	try:
		os.remove(outputFile)
	except WindowsError:
		print "output file not found"

	header = []

	header.append("id")
	header.append("generation")

	for _i in range(inputs):
		header.append("in_" + _i)
	for _o in range(numOutputs):
		header.append("out_" + _o)

	with open(resultsFile, 'a') as f:
		f.write(",".join(header))

	id = 0

	for j in range(generations):
		for i in range(population):
			runOne(j, id, numInputs)
			id += 1


def runOne(gen, id, numInputs):

	meta["designID"] = id

	with open(localFolder + "meta.file", 'wb') as f:
		pickle.dump(meta, f)

	inputs = []
	for i in range(numInputs):
		inputs.append(random.random())

	with open(inputFile, 'w') as f:
		f.write('\n'.join([str(x) for x in inputs]))

	start_time = time.time()
	while not os.path.exists(outputFile):
	    time.sleep(.01)
	    if time.time() - start_time > 5.0:
	    	print "timeout"
	    	return None

	if os.path.isfile(outputFile):
	    with open(outputFile, 'r') as f:
	    	outputs = [x.strip() for x in f.readlines()]
	    	print outputs

	    with open(resultsFile, 'a') as f:
			f.write("\n" + ",".join([str(x) for x in ([id,gen] + inputs + outputs)]))

	    waiting = True
	    while waiting:
	    	try:
	    		os.remove(outputFile)
	    		waiting = False
	    	except WindowsError:
	    		time.sleep(1)
	else:
	    raise ValueError("%s isn't a file!" % file_path)
	    return None


run(inputs = ["length", "width", "height"], 
	outputs = ["surface area", "volume"], 
	numGenerations = 100, 
	numPopulation = 100)