import random

# Define letter values as per Scrabble rules
LETTER_SCORES = {
    'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
    'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
    'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10, ' ': 0 # Space for blank tiles
}

# Define the number of tiles for each letter
TILE_DISTRIBUTION = {
    'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2, 'G': 3, 'H': 2, 'I': 9,
    'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 6, 'O': 8, 'P': 2, 'Q': 1, 'R': 6,
    'S': 4, 'T': 6, 'U': 4, 'V': 2, 'W': 2, 'X': 1, 'Y': 2, 'Z': 1, ' ': 2  # 2 blank tiles
}

# Define bonus squares on a standard Scrabble board (simplified for initial implementation)
# Coordinates are (row, col)
BONUS_SQUARES = {
    # Triple Word Score (TW) - Red
    (0, 0): 'TW', (0, 7): 'TW', (0, 14): 'TW',
    (7, 0): 'TW', (7, 14): 'TW', (14, 0): 'TW',
    (14, 7): 'TW', (14, 14): 'TW',

    # Double Word Score (DW) - Pink
    (1, 1): 'DW', (2, 2): 'DW', (3, 3): 'DW', (4, 4): 'DW',
    (1, 13): 'DW', (2, 12): 'DW', (3, 11): 'DW', (4, 10): 'DW',
    (13, 1): 'DW', (12, 2): 'DW', (11, 3): 'DW', (10, 4): 'DW',
    (13, 13): 'DW', (12, 12): 'DW', (11, 11): 'DW', (10, 10): 'DW',
    (7, 7): 'DW', # Start square

    # Triple Letter Score (TL) - Dark Blue
    (1, 5): 'TL', (1, 9): 'TL', (5, 1): 'TL', (5, 5): 'TL',
    (5, 9): 'TL', (5, 13): 'TL', (9, 1): 'TL', (9, 5): 'TL',
    (9, 9): 'TL', (9, 13): 'TL', (13, 5): 'TL', (13, 9): 'TL',

    # Double Letter Score (DL) - Light Blue
    (0, 3): 'DL', (0, 11): 'DL', (2, 6): 'DL', (2, 8): 'DL',
    (3, 0): 'DL', (3, 7): 'DL', (3, 14): 'DL', (6, 2): 'DL',
    (6, 6): 'DL', (6, 8): 'DL', (6, 12): 'DL', (7, 3): 'DL',
    (7, 11): 'DL', (8, 2): 'DL', (8, 6): 'DL', (8, 8): 'DL',
    (8, 12): 'DL', (11, 0): 'DL', (11, 7): 'DL', (11, 14): 'DL',
    (12, 6): 'DL', (12, 8): 'DL', (14, 3): 'DL', (14, 11): 'DL',
}


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.rack = [] # Tiles the player currently holds

    def __str__(self):
        return f"{self.name} (Score: {self.score}, Rack: {', '.join(self.rack)})"

class ScrabbleGame:
    BOARD_SIZE = 15 # Scrabble board is 15x15

    def __init__(self):
        self.tile_bag = self._initialize_tile_bag()
        self.players = [] # Changed to a list to maintain order of play
        self.board = self._initialize_board() # Initialize the board here

    def _initialize_tile_bag(self):
        """Initializes the tile bag with all Scrabble tiles."""
        bag = []
        for letter, count in TILE_DISTRIBUTION.items():
            bag.extend([letter] * count)
        random.shuffle(bag)
        return bag

    def _initialize_board(self):
        """Initializes an empty 15x15 Scrabble board."""
        # Represents empty squares with a space ' '
        # Or, we could represent them with ' ' and bonus squares with their types
        board = [[' ' for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        # For display purposes, let's mark bonus squares with their type initially.
        # This will be overwritten by actual letters when placed.
        for (r, c), bonus_type in BONUS_SQUARES.items():
            board[r][c] = bonus_type[0] # Using first letter, e.g., 'T' for TW, 'D' for DW, etc.
        return board


    def display_board(self):
        """Prints the current state of the Scrabble board."""
        # Print column numbers
        print("   " + " ".join([str(i % 10) for i in range(self.BOARD_SIZE)]))
        print("  " + "-" * (self.BOARD_SIZE * 2 + 1))
        for r_idx, row in enumerate(self.board):
            # Print row number and then the row content
            print(f"{r_idx:2d}|" + " ".join(row) + "|")
        print("  " + "-" * (self.BOARD_SIZE * 2 + 1))


    def draw_tiles(self, num_tiles):
        """Draws a specified number of tiles from the bag."""
        drawn_tiles = []
        for _ in range(num_tiles):
            if self.tile_bag:
                drawn_tiles.append(self.tile_bag.pop())
            else:
                print("Tile bag is empty!")
                break
        return drawn_tiles

    def add_player(self, name):
        """Adds a new player to the game."""
        player = Player(name)
        self.players.append(player)
        # Give the player their initial rack of 7 tiles
        player.rack.extend(self.draw_tiles(7))
        print(f"{name} joined the game. Initial rack: {player.rack}")
        return player

    def calculate_word_score(self, word, row, col, direction):
        """
        Calculates the score of a word placed on the board, considering bonus squares.
        This is a simplified version and does not check for validity of placement or
        words formed perpendicularly.
        """
        word_score = 0
        word_multiplier = 1 # Applies to the entire word (e.g., Double Word, Triple Word)
        
        # We don\'t need a temp_board here as we are just calculating score, not placing.
        # This function should only read from the board (to check bonus squares)

        for i, letter in enumerate(word):
            current_row, current_col = row, col
            if direction == 'H': # Horizontal
                current_col += i
            elif direction == 'V': # Vertical
                current_row += i

            # Basic boundary check (more robust checks needed in actual play_word)
            if not (0 <= current_row < self.BOARD_SIZE and 0 <= current_col < self.BOARD_SIZE):
                return -1 # Indicate invalid placement for now (out of bounds)

            # Get letter score, converting to upper for consistency
            letter_score = LETTER_SCORES.get(letter.upper(), 0)

            # Check for bonus on the original board before any letters are placed.
            # This logic assumes bonuses are "used" up after a word is placed,
            # which for simplicity we are not implementing yet (i.e. bonus squares don\'t disappear)
            bonus = BONUS_SQUARES.get((current_row, current_col), None)

            if bonus == 'DL':
                letter_score *= 2
            elif bonus == 'TL':
                letter_score *= 3
            elif bonus == 'DW':
                word_multiplier *= 2
            elif bonus == 'TW':
                word_multiplier *= 3
            
            word_score += letter_score
            # No modification to board here, this is for score calculation only.

        final_score = word_score * word_multiplier
        return final_score


    def place_word(self, player, word, row, col, direction):
        """
        Attempts to place a word on the board.
        This simplified version assumes the word fits and doesn\'t check for existing letters
        or if the word connects to other words.
        It also removes tiles from the player\'s rack.
        """
        # First, check if the player has the required tiles
        player_rack_copy = list(player.rack) # Work with a copy to revert if placement fails
        tiles_to_use = []

        for letter in word.upper():
            if letter in player_rack_copy:
                player_rack_copy.remove(letter)
                tiles_to_use.append(letter)
            elif ' ' in player_rack_copy: # Use a blank tile if specific letter not found
                player_rack_copy.remove(' ')
                tiles_to_use.append(' ') # Track that a blank was used
            else:
                print(f"Error: {player.name} does not have the necessary tiles to play '{word}'. Missing '{letter}'.")
                return False
        
        # Calculate score first, before actual board modification
        score = self.calculate_word_score(word, row, col, direction)
        if score == -1: # Out of bounds check from calculate_word_score
            print("Error: Word placement out of bounds.")
            return False

        # If tiles are available and placement is within bounds, proceed with actual placement
        for i, letter in enumerate(word.upper()):
            current_row, current_col = row, col
            if direction == 'H':
                current_col += i
            elif direction == 'V':
                current_row += i # Changed from col to row here
            
            # Place the letter. This will overwrite any bonus markers.
            self.board[current_row][current_col] = letter
        
        player.score += score
        player.rack = player_rack_copy # Update player's rack after using tiles
        print(f"{player.name} placed '{word}' for {score} points.")
        
        # Draw new tiles to refill the rack (up to 7)
        tiles_drawn = self.draw_tiles(7 - len(player.rack))
        player.rack.extend(tiles_drawn)
        print(f"{player.name} drew {tiles_drawn} tiles to refill their rack.")
        
        return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    game = ScrabbleGame()
    print(f"Initial tile bag size: {len(game.tile_bag)}")

    player1 = game.add_player("Alice")
    player2 = game.add_player("Bob")

    print(f"""
Current Player States:""")
    for player in game.players:
        print(player)

    print(f"""
Remaining tile bag size: {len(game.tile_bag)}""")
    print("""
Initial Board (with bonus markers):""")
    game.display_board()

    # --- Test placing a word ---
    print("""
--- Testing Word Placement ---""")
    
    # Manually give Alice tiles to form "HELLO" horizontally at (7,7)
    # Ensuring the rack contains exactly the letters needed and some extra
    player1.rack = ['H', 'E', 'L', 'L', 'O', 'A', 'Z'] # Ensure Alice has HELLO and others
    print(f"""
{player1.name}'s rack before play: {player1.rack}""")
    
    # Try to place "HELLO" at (7,7) horizontally (central square is DW)
    # H (7,7 DW) E (7,8) L (7,9) L (7,10) O (7,11)
    # Score calculation for "HELLO":
    # H: 4, E: 1, L: 1, L: 1, O: 1. Total (base): 8
    # (7,7) is DW, so word_multiplier starts at 2
    # Score should be (4+1+1+1+1) * 2 = 8 * 2 = 16
    
    game.place_word(player1, "HELLO", 7, 7, 'H')
    print("""
Board after placing HELLO:""")
    game.display_board()
    print(f"""
{player1.name}'s rack after play: {player1.rack}""")
    print(f"{player1.name}'s score: {player1.score}")
    print(f"Remaining tile bag size: {len(game.tile_bag)}")


    # Manually give Bob tiles to form "WORLD" vertically at (0, 1)
    player2.rack = ['W', 'O', 'R', 'L', 'D', 'K', 'J'] # Ensure Bob has WORLD and others
    print(f"""
{player2.name}'s rack before play: {player2.rack}""")
    
    # Try to place "WORLD" at (0, 1) vertically
    # W (0,1) O (1,1 DW) R (2,1) L (3,1) D (4,1)
    # Score for WORLD:
    # W: 4, O: 1, R: 1, L: 1, D: 2. Total (base): 9
    # (1,1) is DW, so word_multiplier starts at 2
    # Score should be (4 + (1*2) + 1 + 1 + 2) * 2 = (4+2+1+1+2) * 2 = 10 * 2 = 20
    
    game.place_word(player2, "WORLD", 0, 1, 'V')
    print("""
Board after placing WORLD:""")
    game.display_board()
    print(f"""
{player2.name}'s rack after play: {player2.rack}""")
    print(f"{player2.name}'s score: {player2.score}")
    print(f"Remaining tile bag size: {len(game.tile_bag)}")

    # Test placing a word with a blank tile
    print("""
--- Testing Word Placement with Blank Tile ---""")
    player1.rack = ['B', 'L', 'A', 'N', 'K', ' ', 'S'] # Alice has a blank
    print(f"""
{player1.name}'s rack before play: {player1.rack}""")
    # Place "BLANK" at (14, 8) horizontally (no bonuses, near TW)
    game.place_word(player1, "BLANK", 14, 8, 'H')
    print("""
Board after placing BLANK:""")
    game.display_board()
    print(f"""
{player1.name}'s rack after play: {player1.rack}""")
    print(f"{player1.name}'s score: {player1.score}")
    print(f"Remaining tile bag size: {len(game.tile_bag)}")
