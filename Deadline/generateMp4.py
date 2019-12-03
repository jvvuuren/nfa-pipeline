import re
import subprocess

import sys

pipelinePath = "<PIPELINE ROOT>" 

sys.path.append(pipelinePath +  "PythonModules")
import NfaLog as log

logger = log.nfaLog().getLogger("GenerateMp4")
logger.info("Generating mp4 job")

from System.IO import *
from Deadline.Scripting import *

def __main__( *args ):
    deadlinePlugin = args[0]
    job = deadlinePlugin.GetJob()
    paths = job.get_JobExtraInfo9().split(",")

    logger.info(str(job))

    frameRange = job.get_JobExtraInfo1().split("_")

    ffmpegPath = "<PATH TO FFMPEG>"
    argumentsString = "-y -start_number {2} -i {0} -b 5000k {1}.mp4".format(paths[0],paths[1],frameRange[0])

 
    projectName = job.get_JobExtraInfo0()
    postAction = job.get_JobExtraInfo7()

    append = ""
    
    if postAction == "PublishToShotgun":

        append = append + '-prop "PostJobScript=<PATH TO UPLOAD TO SHOTHGUN SCRIPT>" '

        append = append + '-prop "ExtraInfo6={0}"'.format(job.get_JobExtraInfo6())

    	
    logger.info(append)

    subprocess.Popen('C:\\Program Files\\Thinkbox\\Deadline10\\bin\\deadlinecommand.exe -SubmitCommandLineJob -executable "{0}" -arguments "{1}" -name "{2}"  -priority 40 -prop "UserName={3}" -prop "ExtraInfo0={4}" -prop "ExtraInfo9={5}" {6}'.format(ffmpegPath,argumentsString,"Preview_"+str(job),job.JobUserName,projectName,paths[0],append))

