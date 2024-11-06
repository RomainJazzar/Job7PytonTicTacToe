import tkinter as tk
from tkinter import messagebox
import random

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Tic Tac Toe")

# Variables globales
board = [" " for _ in range(9)]  # Plateau vide
current_player = "X"  # Le joueur "X" commence
buttons = []
difficulty = tk.StringVar(value="Facile")  # Niveau de difficulté par défaut

# Fonction pour vérifier le gagnant
def check_winner(board, sign):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Lignes
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colonnes
        [0, 4, 8], [2, 4, 6]              # Diagonales
    ]
    return any(all(board[i] == sign for i in condition) for condition in win_conditions)

# Fonction pour vérifier si le plateau est plein
def is_full(board):
    return all(cell != " " for cell in board)

# Fonction pour l'intelligence artificielle
def ia(board, sign, level):
    opponent = "O" if sign == "X" else "X"
    
    # Niveau Facile : l'IA joue de façon aléatoire
    if level == "Facile":
        empty_cells = [i for i, cell in enumerate(board) if cell == " "]
        return random.choice(empty_cells) if empty_cells else False
    
    # Niveau Moyen : l'IA bloque l'adversaire et joue pour gagner
    elif level == "Moyen":
        # Vérifie si l'IA peut gagner en un coup
        for i in range(9):
            if board[i] == " ":
                board[i] = sign
                if check_winner(board, sign):
                    return i
                board[i] = " "
        
        # Bloque l'adversaire s'il est sur le point de gagner
        for i in range(9):
            if board[i] == " ":
                board[i] = opponent
                if check_winner(board, opponent):
                    board[i] = " "
                    return i
                board[i] = " "
        
        # Sinon, jouer aléatoirement
        empty_cells = [i for i, cell in enumerate(board) if cell == " "]
        return random.choice(empty_cells) if empty_cells else False
    
    # Niveau Difficile : l'IA utilise la stratégie minimax pour jouer parfaitement
    else:
        return minimax(board, sign)["position"]

# Fonction Minimax pour l'IA niveau Difficile
def minimax(board, sign):
    opponent = "O" if sign == "X" else "X"
    
    # Vérifie les conditions de fin de jeu
    if check_winner(board, "X"):
        return {"score": 1}
    elif check_winner(board, "O"):
        return {"score": -1}
    elif is_full(board):
        return {"score": 0}
    
    # Liste des mouvements possibles
    moves = []
    
    # Parcours des cases vides et évaluation de chaque coup possible
    for i in range(9):
        if board[i] == " ":
            board[i] = sign
            result = minimax(board, opponent)
            moves.append({"position": i, "score": result["score"]})
            board[i] = " "
    
    # Choisir le meilleur mouvement en fonction du joueur
    if sign == "X":
        best_move = max(moves, key=lambda x: x["score"])
    else:
        best_move = min(moves, key=lambda x: x["score"])
    
    return best_move

# Fonction pour gérer le clic sur un bouton
def on_click(index):
    global current_player
    
    if board[index] == " ":
        board[index] = current_player
        buttons[index].config(text=current_player)
        
        if check_winner(board, current_player):
            messagebox.showinfo("Fin du jeu", f"Le joueur {current_player} a gagné !")
            reset_board()
            return
        elif is_full(board):
            messagebox.showinfo("Fin du jeu", "Match nul !")
            reset_board()
            return
        
        # Changement de joueur
        current_player = "O" if current_player == "X" else "X"
        
        # Tour de l'IA si le joueur est seul
        if current_player == "O" and difficulty.get() != "Deux Joueurs":
            ia_move = ia(board, current_player, difficulty.get())
            if ia_move is not False:
                board[ia_move] = current_player
                buttons[ia_move].config(text=current_player)
                
                if check_winner(board, current_player):
                    messagebox.showinfo("Fin du jeu", f"L'IA ({current_player}) a gagné !")
                    reset_board()
                    return
                elif is_full(board):
                    messagebox.showinfo("Fin du jeu", "Match nul !")
                    reset_board()
                    return
                
                # Repasser à l'autre joueur
                current_player = "X"

# Fonction pour réinitialiser le plateau
def reset_board():
    global board, current_player
    board = [" " for _ in range(9)]
    current_player = "X"
    for button in buttons:
        button.config(text=" ")

# Création de l'interface graphique
for i in range(9):
    button = tk.Button(root, text=" ", width=10, height=3, command=lambda i=i: on_click(i))
    button.grid(row=i // 3, column=i % 3)
    buttons.append(button)

# Menu de sélection de la difficulté
frame = tk.Frame(root)
frame.grid(row=3, column=0, columnspan=3)
tk.Label(frame, text="Niveau de difficulté :").pack(side=tk.LEFT)
tk.OptionMenu(frame, difficulty, "Facile", "Moyen", "Difficile", "Deux Joueurs").pack(side=tk.LEFT)

# Lancer la fenêtre principale
root.mainloop()
