# Tic Tac Toe Game without graphics

def print_board(board):
    # Function to display the board
    for i in range(3):
        print(" | ".join(board[i*3:(i+1)*3]))
        if i < 2:
            print("---------")

def check_winner(board, sign):
    # Check if the player with the given sign has won
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == sign for i in condition):
            return True
    return False

def ia(board, sign):
    # Basic AI to choose the best move
    opponent = 'O' if sign == 'X' else 'X'
    
    # Check if AI can win in one move
    for i in range(9):
        if board[i] == " ":
            board[i] = sign
            if check_winner(board, sign):
                return i
            board[i] = " "
    
    # Block opponent if they're about to win
    for i in range(9):
        if board[i] == " ":
            board[i] = opponent
            if check_winner(board, opponent):
                board[i] = " "
                return i
            board[i] = " "
    
    # Choose first available cell
    for i in range(9):
        if board[i] == " ":
            return i
    
    return False  # If no move is possible

def play_game():
    # Main function to play the game
    board = [" "] * 9  # Empty board
    current_sign = "X"
    player_choice = input("Do you want to play against the computer? (yes/no): ").lower()
    vs_ai = player_choice == "yes"
    
    for turn in range(9):
        print_board(board)
        if current_sign == "X" or not vs_ai:
            # Human player's turn
            move = int(input(f"Player {current_sign}, choose a cell (0-8): "))
        else:
            # AI's turn
            print("AI's turn...")
            move = ia(board, current_sign)
            if move is False:
                print("AI error.")
                return
        
        if board[move] == " ":
            board[move] = current_sign
            if check_winner(board, current_sign):
                print_board(board)
                print(f"Player {current_sign} wins!")
                return
            current_sign = "O" if current_sign == "X" else "X"  # Switch player
        else:
            print("Cell already taken, choose another one.")
    
    print_board(board)
    print("It's a tie!")

# Start the game
play_game()
