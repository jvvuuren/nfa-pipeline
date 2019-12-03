import os, sys, nuke

import re

pipelinePath = "<PIPELINE ROOT>" 
sys.path.append(pipelinePath +  "PythonModules")
import NfaLog as log

logger = log.nfaLog().getLogger("Nuke")
logger.info("Started Nuke")


readRootDir = "<PROJECTS ROOT LOCATION>"
writeRootDir = "<PROJECTS RENDER LOCATION>"

filename = ""
fileNameSplit = []

dirname = ""
projectPath = ""
projectName = ""

fileVersion = ""

def getFrameNumber(path):
	parts = path.split("_")
	withoutExt = parts[len(parts)-1].split(".")
	withoutExt.pop()
	#return 
	return re.sub("\D", "", "".join(withoutExt)) 



def createWritenode(name,path,lowrespath,xpos=0,ypos=0):
	node = nuke.createNode( "PipeWriter" )
	node["highresfile"].setValue(path)
	node["lowresfile"].setValue(lowrespath)
	node["name"].setValue(name)
	#node["create_directories"].setValue(True)
	node["tile_color"].setValue(3811839)
	#node["compression"].setValue("PIZ Wavelet (32 scanlines)")
	node.setXpos(xpos)
	node.setYpos(ypos)
	#node["name"] = name

def nukifyPath(path):
	parts = path.split("_")

	parts[len(parts)-1] = re.sub('\d',"#",parts[len(parts)-1]) 

	return "_".join(parts)

def convertPoundToThing(path):
	
	occ = path.count("#")

	patt = "#"*occ

	path = path.replace(patt, "%0{0}d".format(str(occ)))

	return path



def checkWriteNodes():
	################### first check for the pipe writer #########################
	writePath = writeRootDir + "\\" + projectName + "\\" + dirname + "\\comp\\" + fileVersion + "\\"
	writePath = writePath.replace("\\","/")

	writeFileName = dirname + "_" + fileVersion + "_####.exr"

	writeLowRes = writeRootDir + "\\" + projectName + "\\" + dirname + "\\previews\\" + fileVersion + "\\" + dirname + "_" + fileVersion + "_####.jpeg"  

	writeLowRes = writeLowRes.replace("\\","/")


	node = nuke.toNode( "PipeWriter" )
	
	if not node == None:
		if node.knob("highresfile"):
			
			node["highresfile"].setValue(writePath+writeFileName)
			node["lowresfile"].setValue(writeLowRes)
		else:
			print "old"
			nuke.message('Verouderde pipewriter gedetecteerd, verwijder pipewriter in dit bestand!')
		#node["compression"].setValue("PIZ Wavelet (32 scanlines)")
	    
	else:

	    createWritenode("PipeWriter",writePath+writeFileName,writeLowRes,0,120)

	################### check for the preview writer ######################### 
	'''
	writePath = writeRootDir + "\\" + projectName + "\\" + dirname + "\\preview\\" + fileVersion + "\\"
	writePath = writePath.replace("\\","/")

	writeFileName = dirname + "_" + fileVersion + "_####.exr"



	node = nuke.toNode( "PipeWriter" )
	
	if not node == None:
		node["file"].setValue(writePath+writeFileName)
	    
	else:

	    createWritenode("PipeWriter",writePath+writeFileName)
	'''





def loadScriptVars():
	
	global filename
	global fileNameSplit
	global dirname
	global projectPath
	global projectName
	global fileVersion
	global isFirstLoad

	filename = ""
	fileNameSplit = []

	dirname = ""
	projectPath = ""
	projectName = ""

	fileVersion = ""


	#first get metadat from filename to get project/projectname, scene number, shot Number
	filename = nuke.root()["name"].value()
	fileNameSplit = os.path.basename(filename).split("_")



	for path in os.listdir(readRootDir):

		if path.startswith(fileNameSplit[0].upper() + "_"):

			projectPath += readRootDir + "\\" +path
			dirname = fileNameSplit[0] + "_" + fileNameSplit[1] + "_" + fileNameSplit[2]

			projectName = path

			fileVersion = fileNameSplit[3].replace(".nk","")

			print dirname

			print projectPath

	nuke.addFavoriteDir("Project", projectPath )
	nuke.addFavoriteDir("Inputs", projectPath + "\\input\\"+dirname +"\\")
	nuke.addFavoriteDir("Write", writeRootDir + "\\" + projectName + "\\" + dirname)



def scriptSaved():
	loadScriptVars()
	checkWriteNodes()
	#checkInputNodes()

def scriptLoaded():
	loadScriptVars()
	checkWriteNodes()
	#checkInputNodes()

nuke.addOnScriptLoad(scriptLoaded)
nuke.addOnScriptSave(scriptSaved)




