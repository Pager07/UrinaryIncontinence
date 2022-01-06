from event import FluidEvent
import numpy as np
import event
from eventhistory import FluidEventHistory
import matplotlib.pyplot as plt
print('event handler')
class EventHandler(FluidEvent):
    def __init__(self) -> None:
        self.liveEvents = []
        self.deadEvents = []
        self.bladderLoss ,self.currentBladderFillingLevel,self.currentBodyStorage, self.currentWorkoutLoss = 0,0,0,0
        self.totalLiquidLoss = 0
        self.eventHistory = FluidEventHistory()

    def addEvent(self,fluidEvent:FluidEvent):
        self.liveEvents += [fluidEvent]
        pass
    def removeEvent(self,fluidEvent:FluidEvent):
        self.deadEvents.remove(fluidEvent)
    
    def isFluidEventFinished(self)->bool:
        """Returns True if body has finished processing the fluid.

        Returns:
            bool: True if the body has finished processing the fluid
        """
        return len(self.liveEvents) == 0
    
    def getTotalLiquidLoss(self)->float:
        """Get the total amount of fluid taken out by body so far

        Returns:
            float: The total amount of fluid take out by body so far
        """
        return self.bladderLoss + self.currentBodyStorage + self.currentWorkoutLoss

    def updateEventHistory(self):
        """Updates the event history after time t
        """
        self.eventHistory.bladderFillingLevels = np.append(self.eventHistory.bladderFillingLevels,
                                                   self.currentBladderFillingLevel)
        self.eventHistory.bladderLoss = np.append(self.eventHistory.bladderLoss,
                                                 self.bladderLoss)
        self.eventHistory.bodyStorage = np.append(self.eventHistory.bodyStorage,self.currentBodyStorage)
        self.eventHistory.workoutLoss = np.append(self.eventHistory.workoutLoss,self.currentWorkoutLoss)
        self.eventHistory.totalLiquidLoss = np.append(self.eventHistory.totalLiquidLoss,self.getTotalLiquidLoss())
        self.eventHistory.isFinished = self.isFluidEventFinished()

    def updateBladderCurrentFillingLevels(self,eventHistory:FluidEventHistory):
        if len(eventHistory.bladderFillingLevels)>1:
            delta = eventHistory.bladderFillingLevels[-1] - eventHistory.bladderFillingLevels[-2]
            self.currentBladderFillingLevel += delta 
        else:
            delta = eventHistory.bladderFillingLevels[-1] - 0
            self.currentBladderFillingLevel +=  delta
    
    def updateBladderLoss(self,eventHistory:FluidEventHistory):
        if len(eventHistory.bladderLoss)>1:
            delta = eventHistory.bladderLoss[-1] - eventHistory.bladderLoss[-2]
            self.bladderLoss += delta 
        else:
            delta = eventHistory.bladderLoss[-1] - 0
            self.bladderLoss +=  delta
    
    
    def updateBodyStorage(self,eventHistory:FluidEventHistory):
        if len(eventHistory.bodyStorage)>1:
            delta = eventHistory.bodyStorage[-1] - eventHistory.bodyStorage[-2]
            self.currentBodyStorage += delta 
        else:
            delta = eventHistory.bodyStorage[-1] - 0
            self.currentBodyStorage +=  delta
            
    def updateWorkoutLoss(self,eventHistory:FluidEventHistory):
        if len(eventHistory.workoutLoss)>1:
            delta = eventHistory.workoutLoss[-1] - eventHistory.workoutLoss[-2]
            self.currentWorkoutLoss += delta 
        else:
            delta = eventHistory.workoutLoss[-1] - 0
            self.currentWorkoutLoss +=  delta

    
    def handleSingleEvent(self,fluidEvent:FluidEventHistory,micturtion:bool = False):
        """Given a single fluid event, it will update the liquid loss

        Args:
            fluidEvent (FluidEventHistory): 
        """
        eventHistory = fluidEvent.forward(micturtion)
        self.updateBladderCurrentFillingLevels(eventHistory)
        self.updateBladderLoss(eventHistory)
        self.updateBodyStorage(eventHistory)
        self.updateWorkoutLoss(eventHistory)
        
        if eventHistory.isFinished:
            self.deadEvents.append(fluidEvent)
            self.liveEvents.remove(fluidEvent)
    
    def emptyBaldder(self,event:FluidEvent):
        
        pass 
       
    def forward(self,micturtion:bool = False)->FluidEventHistory:
        shouldUpdateEventHistory = len(self.liveEvents)
        for event in self.liveEvents:
            self.handleSingleEvent(event,micturtion=micturtion)
        #after going through the live-events once; update the event history once 
        if shouldUpdateEventHistory:
            self.updateEventHistory()
        return self.eventHistory

    

if __name__ == '__main__':
    handler = EventHandler()
    fluidEvent = FluidEvent(100)
    fluidEvent2 = FluidEvent(100)
    # handler.addEvent(fluidEvent)
    # handler.addEvent(fluidEvent2)
    
    # handler.forward()
    for t in range(1440):
        # print(t)
        if t ==0:
            handler.addEvent(fluidEvent)
        if t == 10:
            handler.addEvent(fluidEvent2)
        if t == 50:
            eventHistory = handler.forward(micturtion=True)
        else:
            eventHistory = handler.forward()
        # print(f'finished:{t},{eventHistory.totalLiquidLoss[-1]},{eventHistory.bladderFillingLevels[-1]}', {eventHistory.workoutLoss[-1]},{eventHistory.bodyStorage[-1]})

    for e in handler.deadEvents:
        print(e.eventHistory.bladderLoss[:])

    fig,axes = plt.subplots(5,1,figsize=(15,15))

    l = [eventHistory.totalLiquidLoss[:],eventHistory.bladderLoss[:],eventHistory.bladderFillingLevels[:], eventHistory.workoutLoss[:],eventHistory.bodyStorage[:]]
    title = ['Total Liquid Loss vs Time (mins)', 'Total bladder Loss vs Time (mins)' ,'Total bladder volume vs Time (mins)', 'Total workout liquid loss vs Time (mins)', 'Total liquid stored in body vs Time (mins)']
    for i, ax in enumerate(axes):
        ax.plot(l[i])
        ax.set_title(title[i])
        ax.set_ylabel('Liquid volume (ml)')
        ax.set_xlabel('Time (mins)')
        plt.tight_layout()
    
    plt.savefig('testeventhandler.png')
    
    # for t in range(1440):
    #     handler.forward()
    #     print(f'{t},{handler.liveEvents[0].eventHistory.isFinished},{handler.currentBladderFillingLevel},{handler.currentWorkoutLoss},{handler.currentBodyStorage}')
    #     # if not handler.liveEvents:
    #     if  handler.liveEvents[0].eventHistory.isFinished:
    #         print('ther are not live events')
    #         break
    