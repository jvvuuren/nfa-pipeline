import os, sys
import shutil


pipelinePath = "<INSERT PATH TO PIPELINE>" 

sys.path.append(pipelinePath +  "PythonModules")

import NfaLog as log

logger = log.nfaLog().getLogger("AssetEditor")


import shotgun_api3
sg = shotgun_api3.Shotgun("<SHOTGUN URL>",script_name="asseteditor",api_key="<SCRIPT KEY>")

sgproject = {}



rootDir = "<READ ROOT DIR>"

writeRootDir =  "<WRITE ROOT DIR>"

clear = lambda: os.system('cls')

projects = {}

selectedProject = ""


def loadProjects():
	global projects
	for path in os.listdir(rootDir):



		if os.path.isdir(rootDir + "\\" + path):
			if "_" in path:
				parts = path.split("_")
				if len(parts[0]) == 3:
					projects[parts[0]] = parts[1]


def start():
	loadProjects()


	print "Select Project: \n"
	for key, value in projects.iteritems():
		print "[" + key + "] " + value

	print ""
	selection = raw_input("3 letter code: ").upper()

	if selection in projects:
		 
		global selectedProject
		selectedProject = selection

		editor()



	else:
		clear()
		print "Project not found"

	start()


def editor():
	clear()
	global selectedProject
	global sgproject

	print "Retreving shotgun project info"
	filters = [['sg_projectcode', 'is', selectedProject]]
	sgproject = sg.find_one('Project', filters)




	print "Asseteditor for " + projects[selectedProject]

	editOrNew = raw_input("(E)dit or (N)ew? ")
	if (editOrNew.upper() == "E"):
		edit()

	elif (editOrNew.upper() == "N"):
		new()

	editor()



def edit():
	print "Edit it"

def new():
	global selectedProject
	global sgproject
	projectDirName = selectedProject+ "_" +projects[selectedProject]
	projectDir = rootDir + "\\" + projectDirName




	curversion = 0

	for file in os.listdir(projectDir + "\\asset"):
		if "_" in file: 
			parts = file.split("_")
			version = parts[1].replace("a","") 
			version = int(version)
			if version > curversion:   
				curversion = version 

	logger.info("Current version is " + str(curversion))


	prefix = selectedProject.lower() + "_a" + str(curversion+1).zfill(3)+"_"
	filename = raw_input(prefix)

	logger.info(prefix+filename)

	os.chdir(projectDir + "\\asset")
	os.makedirs(prefix + filename)
	os.chdir(prefix  + filename)
	os.makedirs("publish")
	os.makedirs("work")
	#make all the dirs in the publish folder
	software = ["Houdini","Mari","Maya","Nuke","Photoshop","SpeedTree","Substance","Zbrush"]
	
	os.chdir("publish")
	for soft in software:
		os.makedirs(soft)

	os.chdir("../work")
	for soft in software:
		if soft == "Maya":
			continue
		os.makedirs(soft)

	#software specific operations
	
	#HOUDINI
	logger.info("Creating houdini direcotiresz")
	os.chdir("Houdini")
	os.makedirs("cache")
	os.makedirs("flip")
	os.makedirs("textures")

	#MAYA	
	logger.info("Creating maya asset")
	shutil.copytree(projectDir + "\\template\\Maya",projectDir+ "\\asset\\" + prefix+filename + "\\work\\Maya")
	os.chdir("../Maya/scenes")
	os.rename("maya.ma", prefix+filename+".0001"+".ma")



	logger.info("Writing asset to shotgun")


	sgdata = {
	'project':sgproject,
	'code': prefix+filename

	}
	result = sg.create("Asset",sgdata)

	logger.info(result)
start()

