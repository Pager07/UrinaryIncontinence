from event import FluidEvent
import numpy as np
import event
from eventhistory import FluidEventHistory
print('event handler')
class EventHandler:
    def __init__(self) -> None:
        self.liveEvents = []
        self.deadEvents = []
        self.currentBladderFillingLevel,self.currentBodyStorage, self.currentWorkoutLoss = 0,0,0
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
        return self.getTotalLiquidLoss() >= self.intake

    def updateEventHistory(self):
        """Updates the event history after time t
        """
        self.eventHistory.bladderFillingLevels = np.append(self.eventHistory.bladderFillingLevels,
                                                   self.currentBladderFillingLevel)
        self.eventHistory.bodyStorage = np.append(self.eventHistory.bodyStorage,self.currentBodyStorage)
        self.eventHistory.workoutLoss = np.append(self.eventHistory.workoutLoss,self.currentWorkoutLoss)
        self.eventHistory.totalLiquidLoss = np.append(self.eventHistory.totalLiquidLoss,self.getTotalLiquidLoss())
        self.eventHistory.isEventFinished = self.isFluidEventFinished()

    def updateBladderCurrentFillingLevels(self,eventHistory:FluidEventHistory):
        if len(eventHistory.bladderFillingLevels)>1:
            delta = eventHistory.bladderFillingLevels[-1] - eventHistory.bladderFillingLevels[-2]
            self.currentBladderFillingLevel += delta 
        else:
            delta = eventHistory.bladderFillingLevels[-1] - 0
            self.currentBladderFillingLevel +=  delta
        
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

    def updateTotalLiquidLoss(self,eventHistory:FluidEventHistory):
        if len(eventHistory.totalLiquidLoss)>1:
            delta = eventHistory.totalLiquidLoss[-1] - eventHistory.totalLiquidLoss[-2]
            self.totalLiquidLoss += delta 
        else:
            delta = eventHistory.totalLiquidLoss[-1] - 0
            self.totalLiquidLoss +=  delta
    
    def handleSingleEvent(self,fluidEvent:FluidEventHistory):
        """Given a single fluid event, it will update the liquid loss

        Args:
            fluidEvent (FluidEventHistory): 
        """
        eventHistory = fluidEvent.forward()
        self.updateBladderCurrentFillingLevels(eventHistory)
        self.updateBodyStorage(eventHistory)
        self.updateWorkoutLoss(eventHistory)
        self.updateTotalLiquidLoss(eventHistory)
        
        if self.eventHistory.isEventFinished:
            self.deadEvents.append(fluidEvent)
            self.liveEvents.remove(fluidEvent)
     
       
    def forward(self):
        for event in self.liveEvents:
            self.handleSingleEvent(event)

    

if __name__ == '__main__':
    handler = EventHandler()
    fluidEvent = FluidEvent(100)
    fluidEvent2 = FluidEvent(100)
    handler.addEvent(fluidEvent)
    handler.addEvent(fluidEvent2)
    
    # handler.forward()
    # for t in range(1440):
    #     eventHistory = handler.forward(t)
    #     if eventHistory.isEventFinished:
    #         print(f'finished:{t}')
    #         break
     
    # fig,axes = plt.subplots(4,1)
    # axes[0].plot(eventHistory.totalLiquidLoss[:60])
    # axes[1].plot(eventHistory.bladderFillingLevels[:60])
    # axes[2].plot(eventHistory.workoutLoss[:60])
    # axes[3].plot(eventHistory.bodyStorage[:60])
    for t in range(1440):
        handler.forward()
        print(f'{t},{handler.liveEvents[0].eventHistory.isEventFinished},{handler.currentBladderFillingLevel},{handler.currentWorkoutLoss},{handler.currentBodyStorage}')
        # if not handler.liveEvents:
        if  handler.liveEvents[0].eventHistory.isEventFinished:
            print('ther are not live events')
            break
    