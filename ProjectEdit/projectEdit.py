
import os
import sys
import shutil

import getpass

pipelinePath = "<PROJECT ROOT>" 


sys.path.append(pipelinePath +  "PythonModules")

import NfaLog as log

logger = log.nfaLog().getLogger("ProjectEditor")


import shotgun_api3
sg = shotgun_api3.Shotgun("<SHOTGUN URL>",script_name="projectedit",api_key="<SCRIPT KEY>")





logger.info("Loaded")

clear = lambda: os.system('cls')

rootDir = "<PROJECTS ROOT LOCATION>"

writeRootDir =  "<PROJECTS RENDER LOCATION>"

#list of usernames for the personal folders in the project
usernames = ["John Doe","Jane Doe"]



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

	print "Done. \n Creating Subdirectories.....\n"

	os.chdir(rootDirName)


	os.makedirs("asset")
	print "Made /asset"

	os.makedirs("input")
	print "Made /input"

	os.makedirs("pre")
	print "Made /pre"

	os.makedirs("ref")
	print "Made /ref"

	os.makedirs("setup")
	print "Made /setup"

	os.makedirs("user")
	print "Made /user"

	os.makedirs("template")
	print "Made /template"

	print "Done made subdirs \n\n"

	print "Filling template folder...\n\n"

	os.chdir("template")

	print "Copying nuke files"
	shutil.copytree("<PATH TO NUKE TEMPLATES>",rootDir + "\\" +rootDirName + "\\template\\Nuke")

	print "Copying houdini files"
	shutil.copytree("<PATH TO MAYA TEMPLATE>",rootDir + "\\" +rootDirName + "\\template\\Maya")

	print "Copying maya files"
	shutil.copytree("<PATH TO HOUDINI TEMPLATE>",rootDir + "\\" +rootDirName + "\\template\\Houdini")

	print "Done coyping files."
	
	os.chdir("../")
	os.chdir("user")
	print "Making user dirs\n"
	

	for uname in usernames:
		print "\t/" + uname
		os.makedirs(uname)


	print "\n\nMaking folder on write server..."

	os.chdir(writeRootDir)

	os.makedirs(rootDirName)

	print "\n\nGoging to create shotgun project"
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

