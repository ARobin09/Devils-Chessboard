import sys
import math
import random

class board:    
    def __init__(self, lgSize: int = 6, mode: str = None):       
        if(lgSize < 0):
            print("Invalid board size")
            sys.exit()
        if mode is not None and (mode != "H" and mode != "T"):
            print("Invalid mode")
            sys.exit()
        self.checks = lgSize
        self.code = 0
        self.board_size = int(math.pow(2, self.checks))
        self.__set_squares(mode)
        self.__check_tests()
        self.searching = False
        self.current_key = 0
        self.n = math.ceil(math.sqrt(self.board_size))

    def __set_squares(self, mode: str):
        if mode is None:
            self.board = [random.choice(["H", "T"]) for _ in range(self.board_size)]
        elif mode == "H":
            self.board = ["H" for _ in range(self.board_size)]
        else:
            self.board = ["T" for _ in range(self.board_size)]

    def __check(self, bit: int) -> int:
        x = 0
        for i in range(self.board_size):
            if (i >> bit) & 1 == 1:
                if self.board[i] == "H":
                    x ^= 1
                else:
                    x ^= 0
        return x
    
    def __check_tests(self):
  
        for i in range(self.checks - 1, -1, -1):
            r = self.__check(i)
            if r == 1:
                self.code |= (1 << i)
            else:
                self.code &= ~(1 << i)
        
            
    
    def flip(self, pos: int):
        self.board[pos] = "H" if self.board[pos] == "T" else "T"
        self.__check_tests()
        

    def hide_key(self, x: int, y: int):
        key = self.n * (y-1) + (x-1)

        if(key < 0 or key >= self.board_size):
            print("Invalid key")
            return
        if(self.searching):
            print("Cannot hide key while searching for key")
            return

        self.current_key = key
        
        flip = self.code ^ self.current_key

        flip_x = flip % self.n + 1
        flip_y = flip // self.n + 1
        print(f"Encoding...\nHiding key at ({x},{y})\nFlipping coin at position ({flip_x},{flip_y})")
        # print("Before flip:")
        
        # print(str(self))
        self.flip(flip)
        # print("After flip:")
        # print(str(self))
        self.searching = True
    
    def find_key(self):
        if(not self.searching):
            print("\nNo key hidden")
            return
        self.searching = False
        assert self.current_key == self.code, "\nKey is incorrect"
        print("\nSearching for key...")
        code_x = self.code % self.n + 1
        code_y = self.code // self.n + 1
        print(f"Key is at ({code_x},{code_y})")


    def __str__(self):
        n = math.ceil(math.sqrt(self.board_size))  # Number of rows and columns

        for i in range(0, self.board_size, n):  # Iterate in steps of `n`
            print("|".join([str(self.board[j]) for j in range(i, min(i + n, self.board_size))]))
            if (i + n + 1 <= self.board_size): print("\u2014 " * n)  # Print a horizontal line

        return ""  # Return an empty string to avoid additional `None` being printed

    def get_board(self):
        return self.board
    
    def get_board_size(self):
        return self.board_size
    
    def get_checks(self):
        return self.checks
    
    def get_square(self, index: int):
        return self.board[index]
    
    def set_square(self, index: int, value: str):
        self.board[index] = value
    
    def get_code(self):
        return format(self.code, '06b')
def play_game():
    print("Welcome to The Devil's Chessboard Puzzle!")
    lgSize = int(input("Enter the board size (lgSize, e.g., 6 for a 2^6 = 64 square board): "))
    mode = input("Enter the mode ('H' for all heads, 'T' for all tails, or leave blank for random): ").strip() or None

    # Initialize the board
    game_board = board(lgSize, mode)

    while True:
        print("\nCurrent Board:")
        print(game_board)

        print("\nChoose an action:")
        print("1. Hide a key")
        print("2. Find the key")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            try:
                x = int(input("\nEnter the x-coordinate of the key (L->R, starting at 1): "))
                y = int(input("Enter the y-coordinate of the key (T->B, starting at 1): "))
                game_board.hide_key(x, y)
                print("\nCurrent Board:")
                print(game_board)
            except ValueError:
                print("\nInvalid input. Please enter valid integers for coordinates.")
        elif choice == "2":
            game_board.find_key()
        elif choice == "3":
            print("\nThanks for playing!")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")

# Start the game
play_game()