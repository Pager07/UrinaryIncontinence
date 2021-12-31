import numpy as np 
import matplotlib.pyplot as plt
from dataclasses import dataclass

from scipy.integrate import quad
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np

from eventhistory import FluidEventHistory
'''
Suggested sigma:3-6 mins
Suggested mu: 40-60 mins

'''
@dataclass
class ModelParameters:
    mu: int  = 50 #suggested [40-60] min
    sigma: int = 4.6 #suggested [3-6] min
    maxFillingRate: int = 5 #suggest [4-8]ml/min


modelParameters = ModelParameters(mu=50,sigma=4)

def gaussian(x,sigma=4,mu=50):
    dim = np.sqrt(2*np.pi) * sigma
    exp = -0.5*((x-mu)/sigma)**2
    num = np.exp(exp)
    return num/dim

def normal_distribution_function(x,mu=50,sigma=4):
    value = scipy.stats.norm.pdf(x,mu,sigma)
    return value

class FluidEvent:
    def __init__(self, intake:float) -> None:
        global modelParameters
        self.intake = intake
        self.start = modelParameters.mu-(3*modelParameters.sigma)
        self.workoutIntensity = 0

        self.currentBladderFillingLevel,self.currentBodyStorage, self.currentWorkoutLoss = 0,0,0
        self.currentEventMins = 0
        self.eventHistory = FluidEventHistory()
        pass

    def bladderFilling(self,t:int)->float:
        """Returns amount of liquid entering the bladder at time t

        Args:
            t (int): time in minutes after frist taking the fluid

        Returns:
            [float]: Aount of liquied entering the bladder at time t
        """
        if t <=self.start:
            fillingAmount = 0
        else:
            area,err = quad(gaussian,t-1,t)
            # bladderFillingRate = gaussian(t,modelParameters.sigma,modelParameters.mu)
            fillingAmount = (self.intake*area)
        return fillingAmount
    
    def body(self,t:int)->float:
        """Returns amount of liquid stored in the body per minute

        Args:
            t (int): time in minutes after first taking the fluid 

        Retuns:
            float: amount of liquid stored in the body. Currently, 0.4ml/min
        """
        if t <=self.start:
            storedInBody = 0
        else:
            storedInBody = 0.4
        return storedInBody
    
    def workout(self,workoutIntensity:int)->float:
        """Returns the amount of liquid lost during workout per min
        Args:
            workoutIntensity (int): Intensity level in range [0-3]. (No-workout,low,mid,high)
        Returns:
            float: [description]
        """
        workoutLiquidLoss = [1e-3,5,17.5,30] #gotten from paper 
        return workoutLiquidLoss[workoutIntensity]
    
    def updateCurrentBodyStorage(self,t:int):
        """Find the total amount of liquid stored in the body.
        """
        if self.getTotalLiquidLoss() + self.body(t) <= self.intake:
            self.currentBodyStorage += self.body(t)
        else:
            self.currentBodyStorage += max(0,self.intake - self.getTotalLiquidLoss())

    def updateCurrentBladderFillingLevels(self,t:int):
        """Find the total amount of liquid accumulated in the bladder at time t.

        Args:
            t (int):  Time in minutes after the drinking the liquid. AKA time after fluidevent started.

        """
        if self.getTotalLiquidLoss() + self.bladderFilling(t) <= self.intake:
            self.currentBladderFillingLevel += self.bladderFilling(t)
        else:
            self.currentBladderFillingLevel += max(0,self.intake - self.getTotalLiquidLoss())
        
    def updateCurrentWorkoutLoss(self,intensityLevel:int=0):
        """Find the total amount of water lost in workout.

        Args:
            intensityLevel (int, optional): Exercise intensity level. Defaults to 0.
        """
        if self.getTotalLiquidLoss() + self.workout(intensityLevel) <= self.intake:
            self.currentWorkoutLoss += self.workout(intensityLevel)
        else:
            self.currentWorkoutLoss += max(0,self.intake - self.getTotalLiquidLoss())
            
    def getTotalLiquidLoss(self)->float:
        """Get the total amount of fluid taken out by body so far

        Returns:
            float: The total amount of fluid take out by body so far
        """
        return self.currentBladderFillingLevel + self.currentBodyStorage + self.currentWorkoutLoss

    def isFluidEventFinished(self)->bool:
        """Returns True if body has finished processing the fluid.

        Returns:
            bool: True if the body has finished processing the fluid
        """
        return self.getTotalLiquidLoss() >= self.intake
    
    def updateEventHistory(self):
        """Updates the event history after time t
        """
        self.eventHistory.bladderFillingLevels = np.append(self.eventHistory.bladderFillingLevels,
                                                   self.currentBladderFillingLevel)
        self.eventHistory.bodyStorage = np.append(self.eventHistory.bodyStorage,self.currentBodyStorage)
        self.eventHistory.workoutLoss = np.append(self.eventHistory.workoutLoss,self.currentWorkoutLoss)
        self.eventHistory.totalLiquidLoss = np.append(self.eventHistory.totalLiquidLoss,self.getTotalLiquidLoss())
        self.eventHistory.isFinished = self.isFluidEventFinished()

    def forward(self)->FluidEventHistory:
        """Process the FluidEvent for a single mintue.
           Returns FluidEvent history
        Returns:
            (FluidEventHistory): EventHistory containing the log of fluidEvent.
        """
        self.currentEventMins += 1
        self.updateCurrentBodyStorage(self.currentEventMins)

        self.updateCurrentBladderFillingLevels(self.currentEventMins)

        self.updateCurrentWorkoutLoss(self.workoutIntensity)

        self.updateEventHistory()
        
        return self.eventHistory



    
        



if '__main__' == __name__:
    # print(gaussian(1,1,1))
    event = FluidEvent(100)
    bladderFillings = []
    totalFillings  = []
    for t in range(1440):
        eventHistory = event.forward()
        if eventHistory.isFinished:
            print(f'finished:{t}')
            break
    # fig,axes = plt.subplots(4,1)
    # axes[0].plot(eventHistory.totalLiquidLoss[:60])
    # axes[1].plot(eventHistory.bladderFillingLevels[:60])
    # axes[2].plot(eventHistory.workoutLoss[:60])
    # axes[3].plot(eventHistory.bodyStorage[:60])
    # plt.savefig('test.png')
    print(eventHistory.totalLiquidLoss[-1])
    print(eventHistory.bladderFillingLevels[-1])
    print(eventHistory.workoutLoss[-1])
    print(eventHistory.bodyStorage[-1])
    # print(eventHistory.isEventFinished)
    # print(eventHistory.bladderFillingLevels.tolist())
    
    pass
    