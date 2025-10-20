#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 14/10/2025
# But : Classe représentant les bonus et malus du casse-brique
#----------------------------------------------------------------------------#

import tkinter as tk
import random

class Bonus:
    def __init__(self, canvas, x, y, type_bonus, jeu):
        """
        Initialise un bonus/malus tombant :
        - type_bonus : "agrandir", "multi", "reduire", "ralentir"
        """
        self.canvas = canvas
        self.jeu = jeu
        self.type_bonus = type_bonus
        self.vy = 3.6  # vitesse de chute (+20% plus rapide que 3)
        self.actif = True

        # Couleur selon le type (bleu = bonus, rouge = malus)
        couleur = "blue" if type_bonus in ("agrandir", "multi") else "red"

        # Création graphique du cercle représentant le bonus/malus
        self.id = canvas.create_oval(
            x - 8, y - 8, x + 8, y + 8,
            fill=couleur, outline=""
        )

        # Démarre la chute
        self._chuter()

    def _chuter(self):
        # Fait tomber le bonus/malus jusqu'à ce qu'il soit attrapé ou disparaisse
        if not self.actif:
            return

        self.canvas.move(self.id, 0, self.vy)
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        hauteur = self.canvas.winfo_height()

        # Si le bonus touche la raquette
        rx1, ry1, rx2, ry2 = self.jeu.raquette.position()
        if y2 >= ry1 and y1 <= ry2 and x2 >= rx1 and x1 <= rx2:
            self._activer_effet()
            return

        # Si le bonus sort du canvas (non attrapé)
        if y1 > hauteur:
            self.canvas.delete(self.id)
            self.actif = False
            return

        # Continue la chute (toutes les 20 ms)
        self.canvas.after(20, self._chuter)

    def _activer_effet(self):
        # Applique l’effet du bonus ou du malus
        self.canvas.delete(self.id)
        self.actif = False

        if self.type_bonus == "agrandir":
            self.jeu.modifier_taille_raquette(2.0, duree=5000)
        elif self.type_bonus == "multi":
            self.jeu.ajouter_balles_temp(2, duree=8000)
        elif self.type_bonus == "reduire":
            self.jeu.modifier_taille_raquette(0.5, duree=5000)
        elif self.type_bonus == "ralentir":
            self.jeu.modifier_vitesse_raquette(0.5, duree=5000)
