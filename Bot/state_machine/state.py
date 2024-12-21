from abc import abstractmethod
from aiogram.types import Message
#from state_machine.state_tree import StateTree

class StateBundle():
    code: int = None

class State():
    def __init__(self, name: str, tree: 'StateTree') -> None:
        self.name = name
        self.tree: 'StateTree' = tree

    @abstractmethod
    async def enable(self, bundle: StateBundle = None) -> None:
        pass

    @abstractmethod
    async def disable(self) -> None:
        pass

    @abstractmethod
    async def process_message(self, message: Message) -> None:
        pass