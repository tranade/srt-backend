from dataclasses import dataclass
from enum import Enum


@dataclass
class SRTInstruction:
    """
    Data class for SRTInstruction
    """
    step: int
    command: str

    class Commands(Enum):
        VPLOTCLEAR = 'vplotclear'
        AZEL = 'azel'
        X = 'x'
        GALACTIC = 'galactic'
        VPLOT = 'vplot'
        CLEARINT = 'clearint'
        RECORD = 'record'
        RECORDSTOP = 'roff'
        STOW = 'stow'
        QUIT = 'quit'

    @classmethod
    def from_dict(cls, step: int, command_name: str, param1: str | None, param2: str | None):
        if param1 is None:
            param1 = ''
        if param2 is None:
            param2 = ''
        formatted_command_name: str

        if command_name == cls.Commands.VPLOTCLEAR.value:
            formatted_command_name = f'{command_name}'.strip()
        elif command_name == cls.Commands.X.value:
            formatted_command_name = f':{command_name}'.strip()
        else:
            formatted_command_name = f': {command_name}'.strip()
        command = f'{formatted_command_name} {param1} {param2}'.strip()
        return cls(step, command)
