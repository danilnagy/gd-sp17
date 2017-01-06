import os, time, random, math, pickle
from shutil import copyfile


def remap(value, min1, max1, min2, max2):
    return float(min2) + (float(value) - float(min1)) * (float(max2) - float(min2)) / (float(max1) - float(min1))

def getPaths(jobID):
    paths = {}

    paths["local"] = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-1]) + "\\"

    paths["input"] = paths["local"] + "inputs.txt"
    paths["output"] = paths["local"] + "outputs.txt"
    paths["meta"] = paths["local"] + "meta.file"

    paths["job"] = paths["local"] + jobID + "\\"
    paths["results"] = paths["job"] + "results.csv"

    return paths

def init(jobName):

    jobID = "_" + jobName + "_" + time.strftime("%y%m%d_%H%M%S", time.localtime())
    print "Session started:", jobID

    paths = getPaths(jobID)

    cleanup(paths["local"])

    os.makedirs(jobID)
    os.makedirs(paths["job"] + "images")
    os.makedirs(paths["job"] + "lib")

    for f in ["explorer.sh", "index.html", "lib\\d3.v3.js", "lib\\kung.js"]:
        copyfile(paths["local"] + "src\\" + f, paths["job"] + f)

    meta = {"jobID": jobID}

    with open(paths["meta"], 'wb') as f:
        pickle.dump(meta, f)

    return (paths, meta)

def cleanup(folder):
    for f in ["meta.file", "inputs.txt", "outputs.txt", "gh.ping", "python.ping"]:
        try:
            os.remove(folder + f)
            print f, "cleaned up"
        except WindowsError:
            continue

def printFormat(data, inputsDef):
    formatted = []

    for i, d in enumerate(data):

        if type(d) is list:
            value = 0
            for j in range(len(d)):
                value += d[j] * inputsDef[i]["depth"] ** j
            formatted.append(value)
        else:
            formatted.append(d)

    return formatted

def create_input(inputsDef):

    if inputsDef["type"] == "continuous":
        return remap(random.random(), 0, 1, inputsDef["range"][0], inputsDef["range"][1])

    elif inputsDef["type"] == "categorical":
        return int(math.floor(random.random() * inputsDef["num"]))

    elif inputsDef["type"] == "sequence":
        return [int(math.floor(random.random() * inputsDef["depth"])) for x in range(inputsDef["length"])]

def createInputFile(jobDescription):
    paths = getPaths("None")

    inputs = []
    for _i in jobDescription["inputsDef"]:
        inputs.append(create_input(_i))

    with open(paths["input"], 'w') as f:
        f.write('\n'.join([str(x) for x in inputs]))

def defaultOption(name, defaultValue):
    print name, "not specified, using default value(s):", defaultValue
    return defaultValue

def checkJobDescription(jobDescription):

    # substitute defaults for non-specified options

    try:
        jobName = jobDescription["jobName"]
    except KeyError:
        jobName = defaultOption("jobName", "untitled")
    try:
        inputsDef = jobDescription["inputsDef"]
    except KeyError:
        print "error: inputs not specified"
        return
    try:
        outputsDef = jobDescription["outputsDef"]
    except KeyError:
        print "error: outputs not specified"
        return
    try:
        algo = jobDescription["algo"]
    except KeyError:
        algo = defaultOption("algo", "GA")
    try:
        jobOptions = jobDescription["jobOptions"]
    except KeyError:
        jobOptions = defaultOption("jobOptions", {"screenshots": True})


    # test for input types
    for _i in inputsDef:
        try:
            if _i["type"] not in ["continuous", "categorical", "sequence"]:
                print "error:", _i["type"], "input type not supported"
                return
        except KeyError:
            print "error: please specify input type(s)"
            return

    # test for output types
    for _o in outputsDef:
        try:
            if _o["type"] not in ["min", "max"]:
                print "error:", _o["type"], "output type not supported"
                return
        except KeyError:
            print "error: please specify output type(s)"
            return

    # test if chosen algorithm is supported
    if algo not in ["GA", "random"]:
        print "error:", algo, "algorithm not supported"
        return

    algoOptions = checkAlgoOptions(algo, jobDescription)

    return jobName, inputsDef, outputsDef, algo, algoOptions, jobOptions

def checkAlgoOptions(algo, jobDescription):
    if algo == "GA":

        try:
            algoOptions = jobDescription["algoOptions"]
        except KeyError:
            algoOptions = defaultOption("algoOptions", {"numGenerations": 5, "numPopulation": 5, "mutationRate": 0.01, "saveElites": 1})
        try:
            numGenerations = algoOptions["numGenerations"]
        except KeyError:
            algoOptions["numGenerations"] = defaultOption("numGenerations", 5)
        try:
            numPopulation = algoOptions["numPopulation"]
        except KeyError:
            algoOptions["numPopulation"] = defaultOption("numPopulation", 5)
        try:
            mutationRate = algoOptions["mutationRate"]
        except KeyError:
            algoOptions["mutationRate"] = defaultOption("mutationRate", 0.01)
        try:
            saveElites = algoOptions["saveElites"]
        except KeyError:
            algoOptions["saveElites"] = defaultOption("saveElites", 1)

        return algoOptions

    elif algo == "random":

        try:
            algoOptions = jobDescription["algoOptions"]
        except KeyError:
            algoOptions = defaultOption("algoOptions", {"numPopulation": 10})
        try:
            numPopulation = algoOptions["numPopulation"]
        except KeyError:
            algoOptions["numPopulation"] = defaultOption("numPopulation", 10)

        return algoOptions




def computeDesign(idNum, inputs, jobOptions, paths, meta):

    with open(paths["input"], 'w') as f:
        f.write('\n'.join([str(x) for x in inputs]))

    start_time = time.time()
    while not os.path.exists(paths["output"]):
        time.sleep(.1)
        if time.time() - start_time > 10.0:
            return meta, None

    if os.path.isfile(paths["output"]):
        with open(paths["output"], 'r') as f:
            outputs = [float(x.strip()) for x in f.readlines()]

        waiting = True
        while waiting:
            try:
                os.remove(paths["output"])
                waiting = False
            except WindowsError:
                time.sleep(.1)
    else:
        raise ValueError("%s isn't a file!" % file_path)

    if jobOptions["screenshots"]:
        ping = pingGH(paths["local"], idNum)
        if ping is None:
            return meta, None

    return meta, outputs

def pingGH(localFolder, idNum):
    with open(localFolder + "gh.ping", 'wb') as f:
        f.write(str(idNum))

    start_time = time.time()
    while not os.path.exists(localFolder + "python.ping"):
        time.sleep(.1)
        if time.time() - start_time > 10.0:
            return None

    waiting = True
    while waiting:
        try:
            os.remove(localFolder + "python.ping")
            waiting = False
        except WindowsError:
            time.sleep(.1)

    return 1