from LogicLayer.Factory.CreateSimulating.ICreateSimulator import ICreateSimulator 
from LogicLayer.Factory.Simulating.BandChoiceSimulating import BandChoiceSimulating
from LogicLayer import ImageMS

class CreateBandChoiceSimulator(ICreateSimulator):

    def create_simulator(self, image_ms: ImageMS, bands_number: tuple = ()):
        if not bands_number:
            raise ValueError("Band numbers are required for RGB simulation")
        return BandChoiceSimulating(image_ms, bands_number)
