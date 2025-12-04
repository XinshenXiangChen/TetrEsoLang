from Interpreter import Interpreter
from BitParser import BitParser
from tetris_game import TetrisGame

if __name__ == "__main__":
    with open("test_bitcode", "r") as f:
        code = f.read()

    game = TetrisGame()
    cleared_lines = game.run()
