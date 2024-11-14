from typing import Dict, List
from LogicLayer.Factory.CreateSimulating.ICreateSimulator import ICreateSimulator
from LogicLayer.Factory.Simulating import SimulatingMethod

class SimulatorFactory:
    """
    Singleton class to manage the creation of simulators.

    Attributes:
        _instance: Unique instance of the SimulatorFactory class.
        _builders: Dictionary mapping simulator names to their constructors.

    Methods:
        instance: Returns the unique instance of SimulatorFactory.
        simulators: Returns a list of registered simulator names.
        create: Creates a simulator using the registered constructor for the given name.
        register: Registers a new simulator constructor under a given name.
    """
    
    __instance = None
    __builders: Dict[str, ICreateSimulator] = {}

    @staticmethod
    def instance():
        """
        Returns the unique instance of SimulatorFactory.

        Returns:
            SimulatorFactory: The unique instance of the class.
        """
        if SimulatorFactory.__instance is None:
            SimulatorFactory.__instance = SimulatorFactory()
        return SimulatorFactory.__instance

    @property
    def simulators(self) -> List[str]:
        """
        Returns a list of registered simulator names.

        Returns:
            List[str]: List of simulator names.
        """
        return list(self.__builders.keys())

    def create(self, name: str, image_ms) -> SimulatingMethod:
        """
        Creates a simulator using the registered constructor for the given name.

        Args:
            name (str): The name of the simulator to create.
            image_ms: An ImageMS object representing the multispectral image.

        Returns:
            SimulatingMethod: An instance of the created simulator.

        Raises:
            ValueError: If the simulator is not registered.
        """
        builder = self.__builders.get(name)
        if not builder:
            raise ValueError(f"Simulator '{name}' not registered.")
        return builder.create_simulator(image_ms)

    def register(self, name: str, builder: ICreateSimulator) -> None:
        """
        Registers a new simulator constructor under a given name.

        Args:
            name (str): The name of the simulator.
            builder (ICreateSimulator): The simulator's constructor.
        """
        self.__builders[name] = builder
