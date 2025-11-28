class BitParser:
    def __init__(self, bitcode):
        self.bitcode = bitcode

    def get_value_from_bits(self, bits):
        result = 0
        for i in range(0, len(bits)):
            result += int(bits[len(bits)-i-1]) * 2**i
        return result

    def parse(self):

        instructions = []
        for instruction in self.bitcode.split("\n"):
            for atom in instruction.split(" "):
                print(atom)



if __name__ == "__main__":
    with open("test_bitcode", "r") as f:
        code = f.read()

    print(code)

    parser = BitParser(code)
    parser.parse()