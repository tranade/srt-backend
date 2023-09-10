from dataclasses import dataclass, field

from data_classes.srt_instruction import SRTInstruction


@dataclass
class SRTProcedure:
    """
    Data class for SRTProcedure
    """
    id: int
    completionTime: str | None
    userId: int
    userName: str
    userEmail: str
    instructions: list[SRTInstruction] = field(default_factory=list)

    @classmethod
    def from_dict(cls, _id: int, completionTime: str | None, userId: int, userName: str, userEmail: str,
                  instructions: dict[str, dict]):
        SRT_instructions = []
        for step, instruction_data in instructions.items():
            command_name = instruction_data.get('commandName', '')
            param1 = instruction_data.get('param1', None)
            param2 = instruction_data.get('param2', None)

            instruction = SRTInstruction.from_dict(int(step), command_name, param1, param2)
            SRT_instructions.append(instruction)
            SRT_instructions.sort(key=lambda x: x.step)

        return cls(_id, completionTime, userId, userName, userEmail, SRT_instructions)

    def generate_instruction_str_list(self) -> list[str]:
        """
        Generates the list of strings to write to the run file for the srt process to read from

        :return: the list of strings to write to the run file
        """
        # Add the first few instructions
        instruction_str_list = [f': {SRTInstruction.Commands.CLEARINT.value}', f': {SRTInstruction.Commands.RECORD.value}']
        for instruction in self.instructions:
            command = instruction.command
            if command == SRTInstruction.Commands.VPLOTCLEAR.value:
                instruction_str_list.append(f': {SRTInstruction.Commands.VPLOT.value}')
                instruction_str_list.append(f': {SRTInstruction.Commands.CLEARINT.value}')
            else:
                instruction_str_list.append(instruction.command)

        # Add the last few instructions
        if instruction_str_list[-1] != f': {SRTInstruction.Commands.CLEARINT.value}':
            instruction_str_list.append(f': {SRTInstruction.Commands.VPLOT.value}')
            instruction_str_list.append(f': {SRTInstruction.Commands.CLEARINT.value}')

        instruction_str_list.append(f': {SRTInstruction.Commands.RECORDSTOP.value}')
        instruction_str_list.append(f': {SRTInstruction.Commands.STOW.value}')
        instruction_str_list.append(f': {SRTInstruction.Commands.QUIT.value}')

        return instruction_str_list
