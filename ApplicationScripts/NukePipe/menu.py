import subprocess, os
home = os.path.expanduser("~")



pipelinePath = "<PIPELINE ROOT>" 
sys.path.append(pipelinePath +  "PythonModules")
import NfaLog as log

global projectName
global dirname
global fileVersion

logger = log.nfaLog().getLogger("Nuke")
logger.info("Loaded Nuke Menu")


def convertPoundToThing(path):
	
	occ = path.count("#")

	patt = "#"*occ

	path = path.replace(patt, "%0{0}d".format(str(occ)))

	return path


def submitRender():
	logger.info("Submitting render")

	firstFrame = int(nuke.root().knob('first_frame').getValue())
	lastFrame = int(nuke.root().knob('last_frame').getValue())



	p = nuke.Panel('Submit and upload')

	p.addSingleLineInput('FrameRange', '{0}-{1}'.format(firstFrame,lastFrame))
	p.addBooleanCheckBox("Publish to shotgun?",False)

	ret = p.show()

	if ret == 0:
		return

	publishToShotgun = p.value("Publish to shotgun?")
	if publishToShotgun == True:
		c = nuke.Panel("Shotgun")
		c.addMultilineTextInput("Comment","")
		ret = c.show()



		if ret == 0:
			return

	#frameRange = nuke.getInput('FrameRange', '{0}-{1}'.format(firstFrame,lastFrame))
	frameRange = p.value("FrameRange")

	if frameRange == None:
		return

	#writeFile = writeRootDir + "\\" + projectName + "\\" + dirname + "\\comp\\" + fileVersion + "\\" + dirname + "_" + fileVersion + "_####.exr"
	writeFile = writeRootDir + "\\" + projectName + "\\" + dirname + "\\previews\\" + fileVersion + "\\" + dirname + "_" + fileVersion + "_####.jpeg"  
	previewFile =  writeRootDir + "\\" + projectName + "\\" + dirname + "\\previews\\" + dirname + "_" + fileVersion 

	writeFile = convertPoundToThing(writeFile)
	logger.info(writeFile)

	frameRange = frameRange.split("-")

	filepath = nuke.root().name()

	inFrame = int(frameRange[0])
	outFrame = int(frameRange[1])

	filename = os.path.basename(filepath)

	logger.info(filename)
	
	logger.info("Creating submission files")

	


	file = open(home + "/.jobInfo.txt","w") 
	 
	file.write("Plugin=Nuke\n") 
	file.write("Name={0}\n".format(filename.split(".")[0]))
	#file.write("ArchiveOnComplete=true\n")

	file.write("ExtraInfo0={0}\n".format(projectName))
	file.write("ExtraInfo1={0}\n".format("_".join(frameRange)))

	if publishToShotgun == True:
		file.write("ExtraInfo7=PublishToShotgun\n")
		file.write("ExtraInfo6={0}\n".format(c.value("Comment").replace("\n",";;")   ))

	file.write("ExtraInfo8=NukeCustomSubmit\n")
	file.write("ExtraInfo9={0},{1}\n".format(writeFile,previewFile))


	file.write("PostJobScript=<PATH TO POST SCRIPT GENERATE MP4>\n")

	if (outFrame - inFrame) > 2:
		file.write("Frames={0},{1},{2}-{3}".format(inFrame,outFrame,inFrame+1,outFrame-1))
	else:

		file.write("Frames={0}-{1}".format(inFrame,outFrame))
	 
	file.close() 


	
	file = open(home + "/.pluginInfo.txt","w") 
	 
	file.write("SceneFile=" + filepath + "\n")
	file.write("Version=11.2") 

	 
	file.close() 

	logger.info("Submitting to deadline")
	subprocess.Popen("C:\\Program Files\\Thinkbox\\Deadline10\\bin\\deadlinecommand.exe " + home + "/.jobInfo.txt " + home + "/.pluginInfo.txt")

	nuke.message('Submitted job to deadline!')



def checkInputNodes(): 
	logger.info("Checking inputs")

	inputPath = projectPath + "\\input\\" + dirname
	
	inputPathNuke = inputPath.replace("\\","/")
	
	foundPaths = []

	nukePaths = []

	inputShots = os.listdir(inputPath + "\\shot")

	if not len(inputShots) == 0:


		#shotFileName = os.listdir(inputPath + "\\shot\\")[0]
		shotFileName = inputShots[0]
		fileitem = []

		fileitem.append(nukifyPath(inputPathNuke + "/shot/" + shotFileName))
		fileitem.append(getFrameNumber(inputShots[0]))
		fileitem.append(getFrameNumber(inputShots[len(inputShots)-1]))
		fileitem.append("Shot")
		fileitem[0] = convertPoundToThing(fileitem[0])
		foundPaths.append(fileitem)



	'''
	if not len(os.listdir(inputPath + "\\plate")) == 0:

		for path in os.listdir(inputPath + "\\plate"):

		
			plateFiles = os.listdir(inputPath + "\\plate\\" + path)


			fileitem = []

			

			fileitem.append(nukifyPath(inputPathNuke + "/plate/" + path + "/" + plateFiles[0]))
			fileitem.append(getFrameNumber(plateFiles[0]))
			fileitem.append(getFrameNumber(plateFiles[len(plateFiles)-1]))

			

			foundPaths.append(convertPoundToThing(fileitem))

	
	'''
	for node in nuke.allNodes():
		if node.Class() == "Read":
			nodeFile = node["file"].value()
			nukePaths.append(nodeFile)


	# read node collection container
	newReads = []


	#now add them to the comp
	for path in foundPaths:
		if not path[0] in nukePaths:
			logger.info("Creating node " + path[3])
			logger.info(path)
			node = nuke.createNode( "Read" )
			node["file"].setValue(path[0])
			#print path[1]
			node["first"].setValue(int(path[1]))
			node["last"].setValue(int(path[2]))
			node["name"].setValue(path[3])

			# collect read node
			newReads.append(node)


	#ask what read node to get global frame range from (if multiple), or set global range to new read node
	newRange = [0, 0]
	if len(newReads) > 1:
		# make string for enumerator
		newReadNames = ''
		for newRead in newReads:
			newReadNames += newRead.name() + ' '
			
		enumName = 'main plate read node'

		form = nuke.Panel('Choose global range read node')
		form.addEnumerationPulldown(enumName, newReadNames)

		openForm = form.show()
		fromNodeName = openForm.value(enumName)

		fromNode = nuke.toNode(fromNodeName)

		newRange = [fromNode["first"].getValue(), fromNode["last"].getValue()]
	elif len(newReads) == 1:
		fromNode = newReads[0]
		newRange = [fromNode["first"].getValue(), fromNode["last"].getValue()]

	# set new range
	if not newRange == [0, 0]:
		nuke.knob("root.first_frame", str(newRange[0]))
		nuke.knob("root.last_frame", str(newRange[1]))



menubar=nuke.menu("Nuke")

m=menubar.addMenu("&Pipeline")

m.addCommand("&Check Input Nodes", checkInputNodes, "Ctrl+I")
m.addSeparator()
m.addCommand("&Submit comp to deadline", submitRender, "Ctrl+R", shortcutContext=2)

