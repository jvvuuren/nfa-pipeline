import os, sys
import shutil

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('pipelineConfig.cfg')

pipelinePath = config.get('Directories', 'pipelinePath')
rootDir = config.get('Directories', 'rootDir')
writeRootDir = config.get('Directories', 'writeRootDir')

shotgun_url = config.get('Shotgun', 'shotgun_url')
sg_api_key = config.get('Shotgun', 'api_key')

sys.path.append(pipelinePath +  "\\PythonModules")

import NfaLog as log
logger = log.nfaLog().getLogger("ShotEditor")

import shotgun_api3
sg = shotgun_api3.Shotgun(shotgun_url,script_name="shoteditor",api_key=sg_api_key)

sgproject = {}

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

	print "Retrieving shotgun project info"
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

	scenenr = scenenr.zfill(3)
	shotnr = shotnr.zfill(3)	

	dirname = selectedProject.lower() + "_" + scenenr + "_" + shotnr

	os.chdir("03_source")
	print "Creating source"
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	os.chdir(projectDir +"\\workfiles\\shots")
	print "Creating workfiles"
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		os.chdir(dirname)

		shutil.copytree(projectDir + "\\_pipeline\\templates\\Nuke",projectDir+ "\\setup\\" + dirname + "\\Nuke")
		os.chdir("Nuke")
		os.rename("nuke.nk", dirname+"_v001"+".nk")

		os.chdir("../")

		shutil.copytree(projectDir + "\\_pipeline\\templates\\Houdini",projectDir+ "\\setup\\" + dirname + "\\Houdini")
		os.chdir("Houdini")
		os.rename("houdini.hipnc", dirname+"_v001"+".hipnc")


		os.chdir("../")

		shutil.copytree(projectDir + "\\_pipeline\\templates\\Maya",projectDir+ "\\setup\\" + dirname + "\\Maya")
		os.chdir("Maya/scenes")
		os.rename("maya.ma", dirname+".0001"+".ma")

		print "Done creating setup folders"





	print "Creating folder on write server"

	os.chdir(writeRootDir + "\\" + projectDirName + "\\01_cgrenders")
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		os.chdir(dirname)

	os.chdir(writeRootDir + "\\" + projectDirName + "\\03_compp")
	if not os.path.exists(dirname):
		os.makedirs(dirname)
		os.chdir(dirname)

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

