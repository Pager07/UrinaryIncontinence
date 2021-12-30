from fluidevent import FluidEvent
from fluideventhistory import FluidEventHistory
print('event handler')
class EventHandler:
    def __init__(self) -> None:
        self.liveEvents = []
        self.deadEvents = []
        self.currentBladderFillingLevel,self.currentBodyStorage, self.currentWorkoutLoss = 0,0,0
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
        
        pass
    
    
    


if __name__ == '__main__':
    pass