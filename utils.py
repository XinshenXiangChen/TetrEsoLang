instruction_set_util = {
    "ADD": ["ADD", "Reg", "Reg", "Reg"],
    "SUB": ["SUB", "Reg", "Reg", "Reg"],
    "BRZ": ["BRZ", "", "Reg"],
    "SET": ["SET", "Reg", ""],
    "MVE": ["MVE", "Reg", "Reg"],
    "PR": ["PR", "Reg"],
}

values = list(instruction_set_util.values())

def get_value_from_bits(bits):
    result = 0
    for i in range(0, len(bits)):
        result += int(bits[len(bits)-i-1]) * 2**i
    return result