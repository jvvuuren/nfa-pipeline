import os, sys
import shutil

import getpass

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('pipelineConfig.cfg')

pipelinePath = config.get('Directories', 'pipelinePath')
rootDir = config.get('Directories', 'rootDir')
writeRootDir = config.get('Directories', 'writeRootDir')

shotgun_url = config.get('Shotgun', 'shotgun_url')
sg_api_key = config.get('Shotgun', 'api_key')

sys.path.append(pipelinePath + "\\PythonModules")

import NfaLog as log
logger = log.nfaLog().getLogger("ProjectEditor")

import shotgun_api3
sg = shotgun_api3.Shotgun(shotgun_url,script_name="projectedit",api_key=sg_api_key)

#logger.info("Loaded")

clear = lambda: os.system('cls')

# Folders with their relative subfolders
rootfolders = ['01_pre', '02_ref', '03_source', '04_elements', '05_workfiles', '06_renders', '_pipeline']
_pre = ['01_script', '02_breakdown', '03_concept', '04_visie', '05_previs', '06_techvis', '07_planning']
_script = ['latest', 'archive']

_ref = ['01_setdata', '02_schematics', '03_images', '04_video', '05_anim', '06_picturelock']
_setdata = ['photogrammetry', 'reports', 'setimages', 'hdri', 'lens']

_source = ['source']

_elements = ['01_assets', '02_caches', '03_hdri', '04_mattepainting', '05_stock']
_caches = ['anim', 'sim']
_stock = ['images', 'sequences', 'models']

_workfiles = ['assets', 'shot']

_renders = ['prerender', 'cg', 'delivery']

_pipeline = ['templates']
templates = ['Nuke', 'Houdini', 'Maya']

def foldersFromList(folders):
	for i in folders:
		os.makedirs(i)
		print(i)
	return

def start():
	editOrNew = raw_input("(E)dit or (N)ew? ")
	if (editOrNew.upper() == "E"):
		edit()

	elif (editOrNew.upper() == "N"):
		new()

	start()

def edit():
	clear()
	print "edit"

def new():
	os.chdir(rootDir)
	clear()
	
	code = raw_input("Enter 3 letter code: ")
	clear()
	name = raw_input("Enter Name: ")
	clear()


	rootDirName = code.upper() + "_" + name

	print "Creating Directory: "

	print rootDir + "\\" + rootDirName

	print "\n"

	if not os.path.exists(rootDir + "\\" + rootDirName + "\\"):
		os.makedirs(rootDirName)

	else:
		clear()
		print "Failed: Directory exists."
		return

	print "\n Creating main folders...\n"

	projectRoot = rootDir + "\\" + rootDirName# + "\\"

	#Navigate to project root
	os.chdir(projectRoot)
	foldersFromList(rootfolders)

	print "\n Creating subfolders folders...\n"

	#01_pre
	os.chdir(projectRoot + '\\01_pre')
	foldersFromList(_pre)
	os.chdir(projectRoot + '\\01_pre\\01_script')
	foldersFromList(_script)

	#02_ref
	os.chdir(projectRoot + '\\02_ref')
	foldersFromList(_ref)
	os.chdir(projectRoot + '\\02_ref\\01_setdata')
	foldersFromList(_setdata)

	#03_source is empty on purpose
	
	#04_elements
	os.chdir(projectRoot + '\\04_elements')
	foldersFromList(_elements)
	os.chdir(projectRoot + '\\04_elements\\02_caches')
	foldersFromList(_caches)
	os.chdir(projectRoot + '\\04_elements\\05_stock')
	foldersFromList(_stock)

	#05_workfiles
	os.chdir(projectRoot + '\\05_workfiles')
	foldersFromList(_workfiles)

	#06_renders
	os.chdir(projectRoot + '\\06_renders')
	foldersFromList(_renders)

	#_pipeline
	os.chdir(projectRoot + '\\_pipeline')
	foldersFromList(_pipeline)
	
	print "Done made subdirs \n\n"

	print "Filling template folder...\n\n"

	os.chdir("templates")

	print "Copying nuke files"
	shutil.copytree(pipelinePath + "\\Templates\\Nuke",projectRoot + "\\_pipeline\\templates\\Nuke")

	print "Copying houdini files"
	shutil.copytree(pipelinePath + "\\Templates\\Houdini",projectRoot + "\\_pipeline\\templates\\Maya")

	print "Copying maya files"
	shutil.copytree(pipelinePath + "\\Templates\\Maya",projectRoot + "\\_pipeline\\templates\\Houdini")

	print "Done coyping files."
	
	#os.chdir("../")

	print "\n\nMaking folder on write server..."

	os.chdir(writeRootDir)

	os.makedirs(rootDirName)

	print "\n\n Going to create shotgun project"
	sgdata = {
	'name':name,
	'sg_projectcode': code,
	'sg_status':'Active'
	}
	result = sg.create("Project",sgdata)
	logger.info(result)

	print "\n\nAll Done, Bye!"


	exit()



start()

