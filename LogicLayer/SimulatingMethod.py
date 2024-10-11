from abc import ABC, abstractmethod

class SimulateMethod(ABC):
    """
    Classe abstraite pour définir une méthode de simulation.
    """

    def __init__(self, image_ms):
        """
        Constructeur pour initialiser l'image multispectrale.

        Args:
            image_ms: Un objet ImageMS représentant l'image multispectrale à simuler.
        """
        self.image_ms = image_ms

    @abstractmethod
    def simulate(self):
        """
        Méthode abstraite pour simuler une image.

        Returns:
            Les données de l'image simulée.
        """
        pass
