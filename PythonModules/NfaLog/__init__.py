#!/usr/bin/env python3

import logging
import sys
import getpass

import ConfigParser
config = ConfigParser.RawConfigParser()
config.read('pipelineConfig.cfg')

pipelinePath = config.get('Directories', 'pipelinePath')

class nfaLog():
    def getLogger(self,name="unkown"):
        logger = logging.getLogger("root")
        logger.setLevel(logging.DEBUG)

        logpath  = pipelinePath + "\\logs"

        # create file handler which logs even debug messages
        fh = logging.FileHandler(logpath  + name +  "_"+ getpass.getuser() + ".log")
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(module)s - %(funcName)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger
