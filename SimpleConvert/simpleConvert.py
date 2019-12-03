
import os
import sys
import subprocess


import getpass

pipelinePath = "<PIPELINE ROOT>" 


sys.path.append(pipelinePath +  "PythonModules")

import NfaLog as log

logger = log.nfaLog().getLogger("simpleConvert")

inputPath = raw_input("Input File: ")
outputPath = raw_input("Output Path: ")
outputExtension = raw_input("Extension: ")

filename = os.path.splitext(os.path.basename(inputPath))[0]

logger.info(inputPath)
logger.info(outputPath)
logger.info(outputExtension)

logger.info("Generating submission path ")

ffmpegPath = "<PATH TO FFMPEG>"
argumentsString = r"-i {0} {1}/{2}_%04d.{3}".format(inputPath,outputPath,filename,outputExtension)

jobname = "Convert " + filename
jobuser = getpass.getuser()
 
logger.info(argumentsString) 
    
subprocess.Popen('C:\\Program Files\\Thinkbox\\Deadline10\\bin\\deadlinecommand.exe -SubmitCommandLineJob -executable "{0}" -arguments "{1}" -name "{2}"  -priority 45 -prop "UserName={3}"'.format(ffmpegPath,argumentsString,jobname,jobuser))




