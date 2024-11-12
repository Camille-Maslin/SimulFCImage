from LogicLayer.Factory.CreateSimulating import ICreateSimulator 
from LogicLayer.Factory.Simulating import BandChoiceSimulating
from LogicLayer import ImageMS

class CreateBandChoiceSimulator(ICreateSimulator):

    def create_simulator(self, image_ms : ImageMS, bands_number : tuple = ()):
        return BandChoiceSimulating(image_ms, bands_number)
