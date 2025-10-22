#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 12/10/2025
# But : Affichage du score, vies et meilleur score
#----------------------------------------------------------------------------#

import tkinter as tk

class RulesAffichage:
    def __init__(self, parent, jeu=None):
        # Initialise l'affichage des informations du jeu : score, vies, meilleur score
        self.parent = parent
        self.jeu = jeu  # Référence pour mettre à jour le meilleur score à la fin
        self.score = 0
        self.vies = 3
        self.meilleur_score = 0  # Le meilleur score enregistré jusqu'à présent

        # Frame en bas pour afficher score et vies
        self.frame_info = tk.Frame(parent, bg="#001f3f")
        self.frame_info.pack(side="bottom", fill="x")

        # Label du meilleur score
        self.meilleur_label = tk.Label(
            self.frame_info,
            text=f"Meilleur score : {self.meilleur_score}",
            font=("Arial", 12, "bold"),
            fg="gold",
            bg="#001f3f"
        )
        self.meilleur_label.pack(side="top", pady=(5,0))

        # Label du score actuel
        self.score_label = tk.Label(
            self.frame_info,
            text=f"Score : {self.score}",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#001f3f"
        )
        self.score_label.pack(side="left", padx=20, pady=5)

        # Label du nombre de vies
        self.vies_label = tk.Label(
            self.frame_info,
            text=f"Vies : {self.vies}",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#001f3f"
        )
        self.vies_label.pack(side="right", padx=20, pady=5)

    # METTRE À JOUR LE SCORE EN COURS DE PARTIE
    def maj_score(self, points):
        # Ajoute des points au score actuel
        self.score += points
        self.score_label.config(text=f"Score : {self.score}")
        # Ne change pas le meilleur score ici : il sera mis à jour seulement à la fin de la partie

    # PERTE D'UNE VIE
    def perdre_vie(self):
        # Décrémente le nombre de vies
        self.vies -= 1
        self.vies_label.config(text=f"Vies : {self.vies}")
        # Si plus de vies, déclenche la fin de partie
        if self.vies <= 0 and self.jeu:
            # Met à jour le meilleur score seulement à la fin de la partie
            if self.score > self.meilleur_score:
                self.meilleur_score = self.score
            self.jeu.meilleur_score = self.meilleur_score
            self.jeu.game_over()

    # MÉTHODE À APPELER À LA FIN D'UNE VICTOIRE
    def fin_partie_victoire(self):
        # Met à jour le meilleur score uniquement à la fin de la partie
        if self.score > self.meilleur_score:
            self.meilleur_score = self.score
        if self.jeu:
            self.jeu.meilleur_score = self.meilleur_score
