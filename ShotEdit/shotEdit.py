import os, sys
import shutil


pipelinePath = "<PIPELINE ROOT>" 

sys.path.append(pipelinePath +  "PythonModules")

import NfaLog as log

logger = log.nfaLog().getLogger("ShotEditor")


import shotgun_api3
sg = shotgun_api3.Shotgun("<SHOTGUN URL>",script_name="shoteditor",api_key="<SHOTGUN SCRIPT KEY>")

sgproject = {}



rootDir = "<PROJECTS LOCATION>"

writeRootDir =  "<PROJECTS RENDER LOCATION>"

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




	print "Shoteditor for " + projects[selectedProject]

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

	os.chdir(projectDir)

	scenenr = raw_input("Scene nr: ")
	shotnr = raw_input("Shot nr: ")

	scenenr = scenenr.zfill(4)
	shotnr = shotnr.zfill(4)	

	dirname = selectedProject.lower() + "_" + scenenr + "_" + shotnr

	os.chdir("input")
	print "Creating input"
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		os.chdir(dirname)

		os.makedirs("cg")
		os.makedirs("matchmove")
		os.makedirs("plate")
		os.makedirs("shot")
		os.makedirs("sim")
		os.makedirs("mattepainting")
		os.makedirs("denoise")

	os.chdir(projectDir +"\\setup")

	print "Creating setup"
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		os.chdir(dirname)

		shutil.copytree(projectDir + "\\template\\Nuke",projectDir+ "\\setup\\" + dirname + "\\Nuke")
		os.chdir("Nuke")
		os.rename("nuke.nk", dirname+"_v001"+".nk")

		os.chdir("../")

		shutil.copytree(projectDir + "\\template\\Houdini",projectDir+ "\\setup\\" + dirname + "\\Houdini")
		os.chdir("Houdini")
		os.rename("houdini.hipnc", dirname+"_v001"+".hipnc")


		os.chdir("../")

		shutil.copytree(projectDir + "\\template\\Maya",projectDir+ "\\setup\\" + dirname + "\\Maya")
		os.chdir("Maya/scenes")
		os.rename("maya.ma", dirname+".0001"+".ma")

		print "Done creating setup folders"





	print "Creating folder on write server"

	os.chdir(writeRootDir + "\\" + projectDirName)
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		os.chdir(dirname)
		os.makedirs("cg")
		os.makedirs("comp")
		os.makedirs("rewrite")
		os.makedirs("previews")

	logger.info("Writing shot to shotgun")
	filters = [['project', 'is', sgproject],['code','is',scenenr]]
	sgSequence = sg.find_one('Sequence',filters)
	logger.info(sgSequence)
	if(sgSequence == None):
		sgSeqData = {
		'project': sgproject,
		'code':scenenr
		}
		sgSequence = sg.create("Sequence",sgSeqData)
		logger.info(sgSequence)

	sgdata = {
	'project':sgproject,
	'code': scenenr + "_" + shotnr,
	'sg_status_list':'rdy',
	'sg_sequence':sgSequence
	}
	result = sg.create("Shot",sgdata)

	logger.info(result)



start()

