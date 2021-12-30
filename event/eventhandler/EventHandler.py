from fluidevent import FluidEvent
from fluideventhistory import FluidEventHistory
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
    
    def handleSingleEvent(self,fluidEvent:FluidEventHistory):
        """Given a single fluid event, it will update the liquid loss

        Args:
            fluidEvent (FluidEventHistory): 
        """
        eventHistory = fluidEvent.forward()
        self.currentBladderFillingLevel += eventHistory.bladderFillingLevels[-1]
        self.currentBodyStorage += eventHistory.currentBodyStorage[-1]
        self.currentWorkoutLoss += eventHistory.currentWorkoutLoss[-1]
        self.totalLiquidLoss += eventHistory.totalLiquidLoss
        
        if self.eventHistory.isEventFinished:
            self.deadEvents.append(fluidEvent)
            self.liveEvents.remove(fluidEvent)
        
    def forward():
        pass

if __name__ == '__main__':
    pass
    
    
    


if __name__ == '__main__':
    pass