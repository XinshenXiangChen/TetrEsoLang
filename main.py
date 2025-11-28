from Interpreter import Interpreter
from BitParser import BitParser


if __name__ == "__main__":
    with open("test_bitcode", "r") as f:
        code = f.read()

    parser = BitParser()
    code = parser.parse(code)
    print(code)
    instructions = Interpreter()
    instructions.interpret(code)
