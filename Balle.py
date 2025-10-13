#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato                                  #
# Date : 13/10/2025                                                          #
# But : Classe représentant la balle du casse-brique                         #
#----------------------------------------------------------------------------#

import tkinter as tk
import random


class Balle:
    def __init__(self, canvas, x, y, rayon=8, couleur="red", vitesse=5, jeu=None):
        self.canvas = canvas
        self.rayon = rayon
        self.couleur = couleur 
        self.vitesse = vitesse
        self.jeu = jeu

        # Création graphique
        self.id = canvas.create_oval(
            x - rayon, y - rayon, x + rayon, y + rayon,
            fill=couleur, outline=""
        )

        # Vecteurs de déplacement
        self.vx = 0
        self.vy = 0

        # État de mouvement
        self.en_mouvement = False

        # Touche Espace pour lancer la balle
        if jeu is not None:
            jeu.fenetre.bind("<space>", self.lancer)

        # Démarrage de la boucle de mise à jour
        self._boucle()

    def lancer(self, event=None):
        # Lance la balle si elle n'est pas déjà en mouvement
        if not self.en_mouvement:
            self.en_mouvement = True
            self.vx = random.choice([-self.vitesse, self.vitesse])
            self.vy = -self.vitesse

            # ✅ Activation de la raquette au démarrage de la balle
            if self.jeu and self.jeu.raquette:
                self.jeu.raquette.actif = True

    def _boucle(self):
        # Boucle de mise à jour de la balle"
        if self.en_mouvement:
            self.deplacer()
            self._gerer_collisions()
        self.canvas.after(16, self._boucle)

    def deplacer(self):
        # Déplace la balle selon son vecteur de déplacement
        self.canvas.move(self.id, self.vx, self.vy)

    def _gerer_collisions(self):
        # Gère les collisions avec les murs, la raquette et les briques
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height()

        # Murs gauche/droite
        if x1 <= 0:
            self.vx = abs(self.vx)
        elif x2 >= largeur:
            self.vx = -abs(self.vx)

        # Mur haut
        if y1 <= 0:
            self.vy = abs(self.vy)

        # Bas = perte de vie
        if y2 >= hauteur:
            self._perdre_vie()
            return

        # Collision raquette
        if self.jeu and self.jeu.raquette:
            rx1, ry1, rx2, ry2 = self.jeu.raquette.position()
            if y2 >= ry1 and y1 <= ry2 and x2 >= rx1 and x1 <= rx2 and self.vy > 0:
                milieu_raquette = (rx1 + rx2) / 2
                distance = (x1 + self.rayon - milieu_raquette) / (self.jeu.raquette.largeur / 2)
                self.vx = self.vitesse * distance
                self.vy = -abs(self.vitesse)

        # Collision briques
        briques_a_supprimer = []
        for brique_id in self.jeu.briques:
            bx1, by1, bx2, by2 = self.canvas.coords(brique_id)
            if (x2 >= bx1 and x1 <= bx2 and y2 >= by1 and y1 <= by2):
                
                briques_a_supprimer.append(brique_id)
                self.vy = -self.vy
                self.jeu.rules_affichage.maj_score(10)
                break

        for bid in briques_a_supprimer:
            self.canvas.delete(bid)
            self.jeu.briques.remove(bid)

        if not self.jeu.briques:
            self.jeu.victoire()

    def _perdre_vie(self):
        # Gère la perte d'une vie et réinitialise la balle
        self.en_mouvement = False
        self.jeu.rules_affichage.perdre_vie()
        self.jeu.reset_positions()

    def reset_position(self, x, y):
        # Réinitialise la position de la balle et arrête son mouvement
        self.canvas.coords(
            self.id,
            x - self.rayon, y - self.rayon,
            x + self.rayon, y + self.rayon
        )
        self.vx = 0
        self.vy = 0
        self.en_mouvement = False
