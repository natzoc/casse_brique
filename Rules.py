#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato                                  #
# Date : 12/10/2025                                                          #
# But : Affichage du score, vies et meilleur score                            #
#----------------------------------------------------------------------------#

import tkinter as tk

class RulesAffichage:
    def __init__(self, parent, jeu=None):
        self.parent = parent
        self.jeu = jeu  # Référence pour mettre à jour meilleur score
        self.score = 0
        self.vies = 3
        self.meilleur_score = 0

        # Frame en bas
        self.frame_info = tk.Frame(parent, bg="#001f3f")
        self.frame_info.pack(side="bottom", fill="x")

        # Meilleur score (au-dessus du score)
        self.meilleur_label = tk.Label(
            self.frame_info,
            text=f"Meilleur score : {self.meilleur_score}",
            font=("Arial", 12, "bold"),
            fg="gold",
            bg="#001f3f"
        )
        self.meilleur_label.pack(side="top", pady=(5,0))

        # Score
        self.score_label = tk.Label(
            self.frame_info,
            text=f"Score : {self.score}",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#001f3f"
        )
        self.score_label.pack(side="left", padx=20, pady=5)

        # Vies
        self.vies_label = tk.Label(
            self.frame_info,
            text=f"Vies : {self.vies}",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#001f3f"
        )
        self.vies_label.pack(side="right", padx=20, pady=5)

    def maj_score(self, points):
        self.score += points
        self.score_label.config(text=f"Score : {self.score}")

        # Mise à jour meilleur score
        if self.score > self.meilleur_score:
            self.meilleur_score = self.score
            self.meilleur_label.config(text=f"Meilleur score : {self.meilleur_score}")
            if self.jeu:
                self.jeu.meilleur_score = self.meilleur_score

    def perdre_vie(self):
        self.vies -= 1
        self.vies_label.config(text=f"Vies : {self.vies}")
        if self.vies <= 0 and self.jeu:
            self.jeu.game_over()
