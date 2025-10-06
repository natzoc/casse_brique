#----------------------------------------------------------------------------#
# Auteur : Loup Viornery                                                     #
# Date : 06/10/2025                                                          #
# But :                          #
# ToDo :                                                                     #
#----------------------------------------------------------------------------#

import tkinter as tk

class BoutonsJeu:
    def __init__(self, parent, couleur_fond="#001f3f", action_jouer=None):
        self.parent = parent
        self.action_jouer = action_jouer

        self.frame = tk.Frame(parent, bg=couleur_fond)
        self.frame.pack(expand=True)

        # Bouton "Jouer"
        self.bouton_jouer = tk.Button(
            self.frame,
            text="▶️ Jouer",
            font=("Arial", 16, "bold"),
            bg="white",
            fg=couleur_fond,
            width=15,
            height=2,
            command=self.lancer_jeu
        )
        self.bouton_jouer.pack(pady=20)

        # Bouton "Quitter"
        self.bouton_quitter = tk.Button(
            self.frame,
            text="❌ Quitter",
            font=("Arial", 14),
            bg="white",
            fg=couleur_fond,
            width=15,
            height=2,
            command=parent.destroy
        )
        self.bouton_quitter.pack(pady=10)

    def lancer_jeu(self):
        if self.action_jouer:
            self.frame.destroy()  # Supprime le menu
            self.action_jouer()

