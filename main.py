from scrabble_game import ScrabbleGame

def main():
    print("Welcome to Simple Scrabble!")
    game = ScrabbleGame()

    # Add players
    num_players = 2 # For simplicity, hardcode 2 players for now
    for i in range(num_players):
        player_name = input(f"Enter name for Player {i+1}: ")
        game.add_player(player_name)

    current_player_index = 0
    # Simple game loop for a few turns
    for turn in range(5): # Let's run for 5 turns to demonstrate
        player = game.players[current_player_index]
        print(f"""
--- Turn {turn + 1} ---""")
        print(f"It's {player.name}'s turn.")
        print(player) # Show player's current rack and score
        game.display_board()

        word_to_play = input("Enter word to play: ").upper()
        row = int(input("Enter starting row (0-14): "))
        col = int(input("Enter starting column (0-14): "))
        direction = input("Enter direction (H for Horizontal, V for Vertical): ").upper()

        if game.place_word(player, word_to_play, row, col, direction):
            print(f"Successfully played {word_to_play}!")
        else:
            print(f"Could not play {word_to_play}. Please try again.")
        
        # Move to the next player
        current_player_index = (current_player_index + 1) % num_players

    print("""
--- Game End (Demonstration) ---""")
    print("Final Scores:")
    for player in game.players:
        print(f"{player.name}: {player.score} points")
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
