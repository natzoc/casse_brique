#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 14/10/2025
# But : Classe représentant les bonus et malus du casse-brique
#----------------------------------------------------------------------------#

import tkinter as tk
"""
Classe gérant les bonus et malus du casse-brique :
elle crée leur apparence, gère leur chute automatique,
détecte leur collision avec la raquette et applique leurs effets temporaires sur le jeu.
"""

class Bonus:
    def __init__(self, canvas, x, y, type_bonus, jeu):
        # Initialise un bonus/malus tombant
        # Définit les propriétés et crée l’élément graphique
        self.canvas = canvas
        self.jeu = jeu
        self.type_bonus = type_bonus
        self.vy = 3.6  # vitesse de chute (+20% plus rapide que 3)
        self.actif = True

        # Couleur selon type : bleu = bonus, rouge = malus
        couleur = "blue" if type_bonus in ("agrandir", "multi") else "red"

        # Création du cercle représentant le bonus sur le canevas
        self.id = canvas.create_oval(
            x - 8, y - 8, x + 8, y + 8,
            fill=couleur, outline=""
        )

        # Lance la chute automatique du bonus
        self._chuter()

    def _chuter(self):
        # Fait descendre le bonus et gère collisions
        if not self.actif:
            return

        # Déplacement du bonus vers le bas
        self.canvas.move(self.id, 0, self.vy)
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        hauteur = self.canvas.winfo_height()

        # Récupère la position de la raquette
        rx1, ry1, rx2, ry2 = self.jeu.raquette.position()
        # Vérifie collision avec la raquette
        if y2 >= ry1 and y1 <= ry2 and x2 >= rx1 and x1 <= rx2:
            # Si le bonus touche la raquette, on active son effet correspondant
            self._activer_effet()
            return

        # Supprime le bonus s’il sort de l’écran
        if y1 > hauteur:
            self.canvas.delete(self.id)
            self.actif = False
            return

        # Rappelle la fonction après 20ms pour continuer la chute
        self.canvas.after(20, self._chuter)

    def _activer_effet(self):
        # Applique l’effet du bonus/malus sur le jeu
        # Supprime le bonus et le rend inactif
        self.canvas.delete(self.id)
        self.actif = False

        # Selon le type, applique l’effet correspondant
        if self.type_bonus == "agrandir":  # Bonus : agrandit la raquette pendant 5 secondes
            self.jeu.modifier_taille_raquette(2.0, duree=5000)
        elif self.type_bonus == "multi":
            # Double le rayon de la balle principale pendant 8 secondes
            balle = self.jeu.balle
            if balle:
                ancien_rayon = balle.rayon
                balle.rayon *= 2
                x1, y1, x2, y2 = self.jeu.canvas.coords(balle.id)
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                balle.canvas.coords(
                    balle.id,
                    cx - balle.rayon, cy - balle.rayon,
                    cx + balle.rayon, cy + balle.rayon
                )
                # Réinitialise le rayon après 8 secondes
                self.jeu.fenetre.after(8000, lambda: self._reinitialiser_rayon(balle, ancien_rayon))
        elif self.type_bonus == "reduire":   # Malus : réduit la raquette pendant 5 secondes 
            self.jeu.modifier_taille_raquette(0.5, duree=5000)
        elif self.type_bonus == "ralentir":  # Malus : ralentit la raquette pendant 5 secondes
            self.jeu.modifier_vitesse_raquette(0.5, duree=5000)

    def _reinitialiser_rayon(self, balle, ancien_rayon):
        # Remet le rayon de la balle à sa valeur initiale
        balle.rayon = ancien_rayon
        x1, y1, x2, y2 = balle.canvas.coords(balle.id)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        # Met à jour les coordonnées du cercle de la balle
        balle.canvas.coords(
            balle.id,
            cx - balle.rayon, cy - balle.rayon,
            cx + balle.rayon, cy + balle.rayon
        )