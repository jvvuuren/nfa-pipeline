import sys

pipelinePath = "<PIPELINE ROOT>" 

sys.path.append(pipelinePath +  "PythonModules")
import NfaLog as log

logger = log.nfaLog().getLogger("ShotgunUploader")
logger.info("Started Uploader")

import shotgun_api3
sg = shotgun_api3.Shotgun("<SHOTGUN URL>",script_name="uploadtoshotgun",api_key="<SCRIPT KEY>")

sgproject = {}

from Deadline.Scripting import *


writeLocation = "<WRITE ROOT DIR>"


def __main__( *args ):
	deadlinePlugin = args[0]
	job = deadlinePlugin.GetJob()

	rootDirName = job.get_JobExtraInfo0().split("_")
	projectCode = rootDirName[0]


	logger.info("Projectcode is " + projectCode)
	
	filters = [['sg_projectcode', 'is', projectCode]]
	sgproject = sg.find_one('Project', filters)

	logger.info(sgproject)

	jobName = str(job)
	jobName = jobName.replace("Preview_","")

	logger.info(jobName)

	jobSplit = jobName.split("_")

	version = jobSplit[3]

	logger.info(jobSplit)

	shotcode = jobSplit[1] + "_" + jobSplit[2]

	logger.info (shotcode)


	videoLoc = writeLocation + "_".join(rootDirName) + "\\" + jobSplit[0] + "_" + shotcode + "\\previews\\" + jobName +  ".mp4"

	logger.info(videoLoc)

	comment = job.get_JobExtraInfo6().replace(";;","\n")

	logger.info(comment)

	#search for the job user
	user = job.JobUserName

	logger.info(user)
	

	#search shotgun for the user

	filters = [['sg_machineusername',"is",user]]
	sgUser = sg.find_one("HumanUser",filters)

	logger.info(sgUser)



	#CHECK IF WE HAVE FOOUND IN SHOTGUN
	filters = [['project', 'is',sgproject],['code','is',shotcode]]
	sgShot = sg.find_one("Shot",filters)

	logger.info(sgShot)
	
	if not sgShot == None:

		versiondata = {
		'project' : sgproject,
		'entity':sgShot,
		'code':jobName,
		'description': comment,
		'user':sgUser
		}

		result = sg.create("Version",versiondata)

		logger.info(result)

		sg.upload("Version",result["id"],videoLoc,field_name="sg_uploaded_movie")



		logger.info("Done Uploading")

