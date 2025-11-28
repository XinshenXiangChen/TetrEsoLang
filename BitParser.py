import utils

class BitParser:

    def parse(self, bitcode):

        instructions = []

        for instruction in bitcode.split("\n"):
            line = instruction.split(" ")
            full_instruction = utils.values[utils.get_value_from_bits(line[0])]

            for i in range(1, len(full_instruction)):
                full_instruction[i] = full_instruction[i] + str(utils.get_value_from_bits(line[i]))

            instructions.append(full_instruction)

        return instructions


