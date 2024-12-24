from Bot.state_machine.state import State, StateBundle
from aiogram.types import Message

class StateTree():
    def __init__(self, user: 'User') -> None:
        self.user = user
        self.states = []
        self.current_state = 0

    def add_state(self, state: State) -> None:
        self.states.append(state)

    async def set_state_by_name(self, name: str, bundle: StateBundle = None) -> None:
        for i in range(len(self.states)):
            if self.states[i].name == name:
                await self.states[i].disable()
                self.current_state = i
                await self.states[i].enable(bundle)
                return
        
        raise ValueError(f"No such state in tree with name: {name}.")
    
    async def execute_current_state(self, message: Message) -> None:
        await self.states[self.current_state].process_message(message)

    def clear(self):
        self.current_state = 0
        self.states.clear()
