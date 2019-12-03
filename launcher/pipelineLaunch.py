#IMPORT PYTHON MODULES PATH
import sys, os
import subprocess
import getpass
import webbrowser

pipelinePath = "<PIPELINE ROOT>" 

sys.path.append(pipelinePath +  "PythonModules")

import NfaLog as log

logger = log.nfaLog().getLogger("Launcher")




from PySide.QtGui import *

from PySide.QtCore import *

import launcherUi

from launcherUi import Ui_MainWindow as mainWindow









class MainWindow(QMainWindow,mainWindow):
	def __init__(self):
		super(MainWindow,self).__init__()

		self.rootDir = "<PIPELINE PROJECTS PATH>"
		self.writeRootDir = "<PROJECTS RENDER PATH>"
	

		self.projects = {}

		self.currentProject = ""
		self.currentShot = ""









		self.setupUi(self)
		self.loadProjects()
		self.assignWidgets()
		self.setup()
		self.show()
		logger.info("Launcher Loaded")

	def setup(self):

		folderIcon = QPixmap(self.rootDir + "\\Pipeline\\launcher\\icons\\folder-icon.png");
		self.folderButton.setIcon(QIcon(folderIcon))
		

		nukeIcon = QPixmap(self.rootDir + "\\Pipeline\\launcher\\icons\\nuke-icon.png");
		self.nukeButton.setIcon(QIcon(nukeIcon))

		mayaIcon = QPixmap(self.rootDir + "\\Pipeline\\launcher\\icons\\maya-icon.png");
		self.mayaButton.setIcon(QIcon(mayaIcon))

		houdiniIcon = QPixmap(self.rootDir + "\\Pipeline\\launcher\\icons\\houdini-icon.png");
		self.houdiniButton.setIcon(QIcon(houdiniIcon))


		inputIcon = QPixmap(self.rootDir + "\\Pipeline\\launcher\\icons\\input-icon.png");
		self.inputButton.setIcon(QIcon(inputIcon))

		outputIcon = QPixmap(self.rootDir + "\\Pipeline\\launcher\\icons\\output-icon.png");
		self.outputButton.setIcon(QIcon(outputIcon))


		self.actionGroupBox.setEnabled(False)



	def assignWidgets(self):


		self.shotListWidget.itemSelectionChanged.connect(self.onShotSelect)
		self.projectListWidget.itemSelectionChanged.connect(self.onProjectSelect)	

		self.folderButton.clicked.connect(self.folderButtonClick)
		self.inputButton.clicked.connect(self.inputButtonClick)
		self.outputButton.clicked.connect(self.outputButtonClick)

		self.nukeButton.clicked.connect(self.nukeClicked)
		self.mayaButton.clicked.connect(self.mayaClicked)

		openShotgunAction = QAction("Open Shotgun", self)
		openShotgunAction.triggered.connect(self.openShotgun)

		self.menubar.addAction(openShotgunAction)


	#handlers

	def openShotgun(self):

		webbrowser.open("<SHOTUGN URL>/projects/")
		

	def onShotSelect(self):
		
		self.currentShot = self.shotListWidget.currentItem().text()

		self.actionGroupBox.setEnabled(True)
		logger.info("Shot Selected " + self.currentShot)

	def onProjectSelect(self):
	
		self.currentProject = self. projectListWidget.currentItem().projCode
		logger.info("Selected project " + self.currentProject) 
		self.loadShots()
		self.actionGroupBox.setEnabled(False)

	def folderButtonClick(self):
		subprocess.Popen('explorer "' + self.rootDir + "\\" + self.projects[self.currentProject][2] + "\\setup\\" + self.currentShot + '"')
	
	def inputButtonClick(self):
		subprocess.Popen('explorer "' + self.rootDir + "\\" + self.projects[self.currentProject][2] + "\\input\\" + self.currentShot + '"')

	def outputButtonClick(self):
		subprocess.Popen('explorer "' + self.writeRootDir + "\\" + self.projects[self.currentProject][2] + "\\" + self.currentShot + '"')

 	

	def nukeClicked(self):
		
		filepath = self.rootDir + "\\" + self.projects[self.currentProject][2] + "\\setup\\" + self.currentShot + "\\Nuke"
		filename =  self.currentShot + "_v"
		
		totalPath = filepath + "\\" + filename + self.getLatestVersion(filepath,filename,3) + ".nk"
		
		
		os.environ["NUKE_PATH"] = pipelinePath + "ApplicationScripts\\NukePipe"
	
		logger.info("Opening nuke...")
		subprocess.Popen("C:\\Program Files\\Nuke11.2v3\\Nuke11.2.exe --nukex " + totalPath)

		
		
	def mayaClicked(self):
		
		filepath = self.rootDir + "\\" + self.projects[self.currentProject][2] + "\\setup\\" + self.currentShot + "\\Maya\\scenes"
		projectpath = self.rootDir + "\\" + self.projects[self.currentProject][2] + "\\setup\\" + self.currentShot + "\\Maya"
		scriptpath = self.rootDir + "\\" + self.projects[self.currentProject][2] + "\\setup\\" + self.currentShot + "\\Maya\\scripts"
		imagespath = self.writeRootDir + "\\" + self.projects[self.currentProject][2] + "\\" + self.currentShot + "\\cg"

		filename =  self.currentShot + "."

		filename = filename + self.getLatestVersion(filepath,filename,4)
		
		scriptpath = scriptpath+"/"+filename + ".mel"

		totalPath = filepath + "\\" + filename + ".ma"
		
		f = open(scriptpath,"w+")
		f.write('setProject( "{0}");\n'.format(projectpath.replace("\\","/")))
		f.write('file -o "{0}";\n'.format(totalPath.replace("\\","/")))
		f.write('workspace -fr "images" "{0}";'.format(imagespath.replace("\\","/")))
		f.close()
	

		launchCmd =  "C:\\Program Files\\Autodesk\\Maya2018\\bin\\maya.exe -command " + '"eval( \\"' + ' source \\\\"\\"' + scriptpath.replace("\\","/") + '\\\\' +'\\"' + '\\"' + ')"'



		
		logger.info("Opening maya...")
		subprocess.Popen(launchCmd )

		



	#general functions

	def loadProjects(self):

		for path in os.listdir(self.rootDir):

			if os.path.isdir(self.rootDir + "\\" + path):
				if "_" in path:
					parts = path.split("_")
					if len(parts[0]) == 3:
						self.projects[parts[0]] = [parts[0],parts[1],path ]

						item = QListWidgetItem(parts[1])
						item.projCode = parts[0]
						self.projectListWidget.addItem(item)

		logger.info("Loaded projects " + str(self.projects))


	def loadShots(self):

		self.shotListWidget.clear()

		for path in os.listdir(self.rootDir + "\\" + self.projects[self.currentProject][2] + "\\setup"):
			logger.info("Found shot " + path)
			item = QListWidgetItem(path)
			self.shotListWidget.addItem(item)

	def getLatestVersion(self,path,filename,digits=3):
		currentVersion = 0

		for filepath in os.listdir(path):
			if os.path.isdir(filepath) == False:
				if filepath.startswith(filename):
		
					versionString = filepath.replace(filename,"")
					versionString = versionString.split(".")[0]
					versionNumber = int(versionString)

					if versionNumber > currentVersion:
						currentVersion = versionNumber
		
		return str(currentVersion).zfill(digits)
			
		







if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyle("Windows")
	

	mainWin = MainWindow()
	ret = app.exec_()
	sys.exit(ret)

