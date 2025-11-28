class Interpreter:

    class Memory:
        def __init__(self):
            self.registers = {
                "Reg0": 0,
                "Reg1": 0,
                "Reg2": 0,
                "Reg3": 0,
                "Reg4": 0,
                "Reg5": 0,
                "Reg6": 0,
                "Reg7": 0,
                "Reg8": 0,
            }

        def add(self, register, register1, register2):
            self.registers[register] = self.get_register(register1) + self.get_register(register2)

        def subtract(self, register, register1, register2):
            self.registers[register] = self.get_register(register1) - self.get_register(register2)

        def get_register(self, register):
            return self.registers[register]

        def set_register(self, register, value):
            self.registers[register] = value

        def move_register(self, register1, register2):
            self.registers[register1] = self.get_register(register2)

    def __init__(self):

        self.memory = Interpreter.Memory()

    def parse(self, code):
        return [line.split(" ") for line in code.split("\n")]

    def interpret(self, code):

        i = 0
        while i < len(code):
            instruction = code[i]
            match instruction[0]:
                case "ADD":
                    self.memory.add(instruction[1], instruction[2], instruction[3])

                case "SUB":
                    self.memory.add(instruction[1], instruction[2], instruction[3])

                case "SET":
                    self.memory.set_register(instruction[1], float(instruction[2]))

                case "MVE":
                    self.memory.move_register(instruction[1], instruction[2])

                case "BRZ":
                    if int(instruction[2]) == 0:
                        i = instruction[1]

                case "PR":
                    print(self.memory.get_register(instruction[1]))


            print(self.memory.registers)
            i = i + 1

