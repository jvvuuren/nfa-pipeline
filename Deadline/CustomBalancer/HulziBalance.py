import math
from Deadline.Events import *
from Deadline.Scripting import *
from pprint import pprint
import json

######################################################################
## This is the function that Deadline calls to get an instance of the
## main DeadlineEventListener class.
######################################################################
def GetDeadlineEventListener():
    return ScheduledEvent()

######################################################################
## This is the function that Deadline calls when the event plugin is
## no longer in use so that it can get cleaned up.
######################################################################
def CleanupDeadlineEventListener( deadlinePlugin ):
    deadlinePlugin.Cleanup()

######################################################################
## This is the main DeadlineEventListener class for ScheduledEvent.
######################################################################
class ScheduledEvent (DeadlineEventListener):

    nowRendering = []
    avalibleSlaves = 0
    totalPrio = 0
    usedSlaves = 0

    dry = True  


    def __init__( self ):
        # Set up the event callbacks here
        self.OnHouseCleaningCallback += self.OnHouseCleaning

    def Cleanup( self ):
        del self.OnHouseCleaningCallback






    def OnHouseCleaning( self ):
        self.nowRendering = []
        self.avalibleSlaves = 0
        self.totalPrio = 0

        #5cc16c3ee0c0c1388ccbdba9
        #5cc16c92e0c0c13d5051f950

        
        remJob = RepositoryUtils.GetJob("5cc16c92e0c0c13d5051f950",True)
        print remJob
        RepositoryUtils.DeleteJob(remJob)
        return
       
        if self.dry == True:
            print "Dryrunmode ACTIVE"
       

        for jobId in RepositoryUtils.GetJobIds():
            #print jobId
            job = RepositoryUtils.GetJob(jobId,True)
            
            print job.JobStatus + " " + job.JobName + " " +job.JobId


            if job.JobStatus == "Active":
                self.nowRendering.append(job)

                self.totalPrio += job.JobPriority

                #print job.JobName + " " + str( job.JobPriority)
        
        return


        for slave in RepositoryUtils.GetSlaveInfos(True):
            if slave.SlaveIsActive == True:
                self.avalibleSlaves += 1
        
        print str(self.totalPrio) + " total piro"
        print str(self.avalibleSlaves) + " slaves avalible"



        for editJob in self.nowRendering:
            

            percent = 0.0
            percent = float(editJob.JobPriority) / float(self.totalPrio)
            
         

            noSlaves = math.ceil(percent*self.avalibleSlaves)

            if not noSlaves >0 :
                noSlaves = 1




            print editJob.JobName + " " +  str(noSlaves) + " " + editJob.SubmitUserName
            print editJob.JobId
            editJob.MachineLimit  = noSlaves
            

            self.usedSlaves += 1

            if self.dry == False:
                RepositoryUtils.SetMachineLimitMaximum(editJob.JobId,noSlaves)


        #Eerste distrubutie van de machines hierna checken of ze meer machines hebben dan dat er nog aan renderende frames zijn



        reusableSlaves = 0    
    
        skipJobs = []

        for editJob in self.nowRendering:
            framesToDo = editJob.JobRenderingTasks + editJob.JobQueuedTasks

            if framesToDo < editJob.MachineLimit:
                print "Job  " + editJob.JobName+" has more machines than tasks"
                
                reusableSlaves += editJob.MachineLimit - framesToDo
                editJob.MoreMachinesThenFrames = editJob.MachineLimit = framesToDo

                skipJobs.append(editJob)

                if self.dry == False:
                    RepositoryUtils.SetMachineLimitMaximum(editJob.JobId,framesToDo)


        print "After Frame Calculation availible: " + str(reusableSlaves )
        # nu alle overgebleven machines herdistuberen over de overige jobs
        for editJob in self.nowRendering:
            if editJob in skipJobs:
                continue

            percent = float(editJob.JobPriority) / float(self.totalPrio)

            newNoSlaves = math.ceil(percent * reusableSlaves)

            print "Adding " + str(newNoSlaves) + " extra slaves to job " + editJob.JobName


           

            if self.dry == False:
                    RepositoryUtils.SetMachineLimitMaximum(editJob.JobId,editJob.MachineLimit)










        

        # alle prios van alle jobs optellen 
        # per job eigen prio / total piro
        # totalslaves * bovengetal, afronden checken groter dan nul
        
     

def __main__( *args ):
    # Replace "pass" with code
    sched = GetDeadlineEventListener()
    sched.OnHouseCleaning()


    pass