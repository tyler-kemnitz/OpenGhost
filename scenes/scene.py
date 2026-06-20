from abc import ABC, abstractmethod

class Scene(ABC):
    """
    Base class for OpenGhost scenes. A scene owns every entity rendered by one sketch
    and exposes the same three-method sequence mirroring py5's sketch lifecycle.
    """

    @abstractmethod
    def setup(self):
        """One-time setup for the scene's entities. Call from py5.setup()"""
        raise NotImplementedError

    @abstractmethod
    def update(self):
        """Advance every owned entity by one frame. Call from py5.draw()"""
        raise NotImplementedError

    @abstractmethod
    def display(self):
        """Render every owned entity. Call from py5.draw()"""
        raise NotImplementedError
