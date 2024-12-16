import random

# Helper function to roll a specific number of dice
def roll_specific_dice(num_dice):
    """Rolls a specific number of dice and returns the results as a list."""
    return [random.randint(1, 6) for _ in range(num_dice)]

# Function to roll three dice and return the values
def roll_dice():
    """Rolls three dice and returns the results as a list."""
    return roll_specific_dice(3)

# Function to check if there are exactly two identical dice
def has_tuple_out(dice_roll):
    """Check if there is a 'tuple out' condition (two identical dice)."""
    return len(set(dice_roll)) == 2  # If exactly two unique values exist, there's a tuple out

# Function to determine which dice are fixed and which are non-fixed
def categorize_dice(dice_roll):
    """Categorize dice into fixed (appears twice) and non-fixed (appears once)."""
    fixed = []
    non_fixed = []
    
    # Count the occurrences of each die value
    dice_count = {die: dice_roll.count(die) for die in set(dice_roll)}
    
    for die, count in dice_count.items():
        if count == 2:
            fixed.append(die)  # This die is fixed (appears twice)
        elif count == 1:
            non_fixed.append(die)  # This die is non-fixed (appears once)
    
    return fixed, non_fixed

# Function to ask the player whether to continue or stop based on the current roll
def player_turn(player_name):
    """Simulate a player's turn to roll the dice and decide what to do with them."""
    dice_roll = roll_dice()
    print(f"\n{player_name}'s turn: {dice_roll}")

    # Check for tuple out (two identical dice)
    if has_tuple_out(dice_roll):
        print(f"{player_name}: Tuple Out! Rerolling non-fixed dice...")
    else:
        print(f"{player_name}: No Tuple Out. Deciding whether to reroll or stop.")

    # Categorize dice into fixed and non-fixed
    fixed_dice, non_fixed_dice = categorize_dice(dice_roll)
    print(f"{player_name}: Fixed dice: {fixed_dice}")
    print(f"{player_name}: Non-fixed dice: {non_fixed_dice}")

    # Allow player to decide whether to reroll non-fixed dice
    reroll_decision = get_player_input(f"{player_name}, do you want to reroll non-fixed dice? (y/n): ", ["y", "n"])
    if reroll_decision == 'y' and non_fixed_dice:
        print(f"{player_name}: Rerolling non-fixed dice...")
        new_roll = roll_specific_dice(len(non_fixed_dice))
        print(f"{player_name}: New roll for non-fixed dice: {new_roll}")
        dice_roll = fixed_dice + new_roll  # Update dice roll with rerolled dice
    else:
        print(f"{player_name}: No dice to reroll, ending turn.")

    return dice_roll, fixed_dice

# Function to handle the final roll for each player
def final_roll(player_name, fixed_dice):
    """Handles the final roll phase, where non-fixed dice are rerolled."""
    print(f"\n{player_name}'s final roll:")

    # Final roll for non-fixed dice
    if len(fixed_dice) < 3:
        non_fixed_dice_needed = 3 - len(fixed_dice)
        non_fixed_dice = roll_specific_dice(non_fixed_dice_needed)
        print(f"{player_name}: Rolling non-fixed dice: {non_fixed_dice}")
        fixed_dice += non_fixed_dice  # Add the final roll to the fixed dice
    else:
        print(f"{player_name}: No dice to reroll, all dice are fixed.")

    # Calculate the final score
    final_score = sum(fixed_dice)
    print(f"{player_name}: Final score from final roll: {final_score}")
    
    return final_score

# Function to validate input from the player (e.g., asking for yes/no answers)
def get_player_input(prompt, valid_choices):
    """Prompt the player for input and ensure it's valid."""
    choice = input(prompt).strip().lower()
    while choice not in valid_choices:
        print("Invalid choice. Please try again.")
        choice = input(prompt).strip().lower()
    return choice

# Function to run the game, iterating through turns and calculating scores
def play_game(player_names, max_turns=5):
    """Simulates the full game with multiple players and turns."""
    scores = {player: 0 for player in player_names}  # Initialize scores
    fixed_dice = {player: [] for player in player_names}  # Track fixed dice for each player
    turn_count = 0

    while turn_count < max_turns:
        for player_name in player_names:
            print(f"\n{'='*10} {player_name}'s Turn {'='*10}")
            # Get the result of the player's turn
            dice_roll, player_fixed_dice = player_turn(player_name)
            # Accumulate fixed dice
            fixed_dice[player_name] += player_fixed_dice
            # Score the player's fixed dice
            turn_score = sum(player_fixed_dice)
            scores[player_name] += turn_score
            print(f"{player_name}: Turn score: {turn_score}")
            print(f"{player_name}: Total score: {scores[player_name]}")

        turn_count += 1
        print(f"\nAfter {turn_count} turns: {scores}")
        
    # After all turns, the final roll phase
    print("\nFinal roll phase:")
    final_scores = {}
    for player_name in player_names:
        final_scores[player_name] = final_roll(player_name, fixed_dice[player_name])

    # Add final roll scores to the main scores
    for player_name in player_names:
        scores[player_name] += final_scores[player_name]

    # Determine the winner based on the highest score
    winner = max(scores, key=scores.get)
    print(f"\nThe winner is {winner} with {scores[winner]} points!")

# Example of running the game with two players
player_names = ["Ewurabena", "Chaz"]
play_game(player_names, max_turns=3)

