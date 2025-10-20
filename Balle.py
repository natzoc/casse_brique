#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 13/10/2025
# But : Classe représentant la balle du casse-brique
#----------------------------------------------------------------------------#

import tkinter as tk
import random
import math
from Bonus import Bonus   # ✅ Import de la classe Bonus


class Balle:
    def __init__(self, canvas, x, y, rayon=8, couleur="white", vitesse=5, jeu=None):
        """
        Initialise une balle :
        - canvas : zone de dessin Tkinter
        - x, y : position de départ
        - rayon : taille de la balle
        - couleur : couleur de la balle
        - vitesse : vitesse de déplacement (pixels / frame)
        - jeu : référence au jeu principal
        """
        self.canvas = canvas
        self.jeu = jeu
        self.rayon = rayon
        self.couleur = couleur
        self.vitesse = vitesse

        # Création du cercle représentant la balle
        self.id = canvas.create_oval(
            x - rayon, y - rayon, x + rayon, y + rayon,
            fill=couleur, outline=""
        )

        # Vecteurs de déplacement (horizontal et vertical)
        self.vx = 0
        self.vy = 0

        # Indique si la balle bouge ou non
        self.en_mouvement = False

        # Associe la touche "Espace" pour lancer la balle
        if jeu is not None:
            jeu.fenetre.bind("<space>", self.lancer)

        # Démarre la boucle de mise à jour (rafraîchissement continu)
        self._boucle()

    #   LANCEMENT DE LA BALLE
    def lancer(self, event=None):
        """ Lance la balle si elle est immobile """
        if not self.en_mouvement:
            self.en_mouvement = True

            # Direction aléatoire gauche/droite
            self.vx = random.choice([-self.vitesse, self.vitesse])
            self.vy = -self.vitesse  # Toujours vers le haut au départ

            # Active la raquette dès le début
            if self.jeu and self.jeu.raquette:
                self.jeu.raquette.actif = True

    #   BOUCLE PRINCIPALE
    def _boucle(self):
        """ Boucle appelée toutes les 16ms (~60 FPS) """
        if self.en_mouvement:
            self.deplacer()
            self._gerer_collisions()

        # Replanifie la fonction pour la prochaine "frame"
        self.canvas.after(16, self._boucle)

    def deplacer(self):
        """ Déplace la balle selon son vecteur de déplacement """
        self.canvas.move(self.id, self.vx, self.vy)

    #   COLLISIONS
    def _gerer_collisions(self):
        """ Gère les collisions avec les murs, la raquette et les briques """
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height()

        # Murs gauche / droite 
        if x1 <= 0:
            self.vx = abs(self.vx)   # rebondit vers la droite
        elif x2 >= largeur:
            self.vx = -abs(self.vx)  # rebondit vers la gauche

        # Mur haut
        if y1 <= 0:
            self.vy = abs(self.vy)   # rebondit vers le bas

        # Mur bas : la balle tombe => perte de vie 
        if y2 >= hauteur:
            self._perdre_vie()
            return

        # Collision avec la raquette
        if self.jeu and self.jeu.raquette:
            rx1, ry1, rx2, ry2 = self.jeu.raquette.position()
            if y2 >= ry1 and y1 <= ry2 and x2 >= rx1 and x1 <= rx2 and self.vy > 0:
                # Calcul du rebond en fonction de la zone touchée sur la raquette
                milieu_raquette = (rx1 + rx2) / 2
                distance = (x1 + self.rayon - milieu_raquette) / (self.jeu.raquette.largeur / 2)
                # Conversion de la position d’impact en angle (jusqu’à ±60°)
                angle = distance * (math.pi / 3)
                self.vx = self.vitesse * math.sin(angle)
                self.vy = -self.vitesse * math.cos(angle)

        # Collision avec les briques
        # Liste temporaire pour stocker les briques touchées par la balle
        briques_a_supprimer = []
        # Parcourt toutes les briques du jeu
        for brique_id in self.jeu.briques:
            # Récupère les coordonnées (x1, y1, x2, y2) de la brique
            bx1, by1, bx2, by2 = self.canvas.coords(brique_id)
            # Test de collision : vérifie si la balle et la brique se chevauchent
            # - x2 >= bx1 : le bord droit de la balle dépasse le bord gauche de la brique
            # - x1 <= bx2 : le bord gauche de la balle dépasse le bord droit de la brique
            # - y2 >= by1 : le bas de la balle dépasse le haut de la brique
            # - y1 <= by2 : le haut de la balle dépasse le bas de la brique
            if (x2 >= bx1 and x1 <= bx2 and y2 >= by1 and y1 <= by2):
                # Si collision détectée :
                # On ajoute cette brique dans la liste à supprimer
                briques_a_supprimer.append(brique_id)
                # On inverse la direction verticale de la balle
                # Cela simule le rebond après avoir touché une brique
                self.vy = -self.vy  # rebond vertical
                # On augmente le score de 10 points via l’affichage du HUD (RulesAffichage)
                self.jeu.rules_affichage.maj_score(10)

                # ✅ 15% de chance de générer un bonus ou malus (si activés)
                if self.jeu.bonus_actives.get() and random.random() < 0.15:
                    type_bonus = random.choice(["agrandir", "multi", "reduire", "ralentir"])
                    bx = (bx1 + bx2) / 2
                    by = (by1 + by2) / 2
                    bonus = Bonus(self.canvas, bx, by, type_bonus, self.jeu)
                    self.jeu.bonus_actifs.append(bonus)

                # On quitte la boucle : une seule brique est cassée à la fois
                break

        for bid in briques_a_supprimer:
            self.canvas.delete(bid)
            self.jeu.briques.remove(bid)

        # Si plus de briques => victoire
        if not self.jeu.briques:
            self.jeu.victoire()

        # Normalisation de la vitesse
        self._normaliser_vitesse()

    # GESTION DES VIES
    def _perdre_vie(self):
        """ Gère la perte d'une vie et réinitialise la balle """
        self.en_mouvement = False
        self.jeu.rules_affichage.perdre_vie()
        self.jeu.reset_positions()

    def reset_position(self, x, y):
        """ Replace la balle au point de départ et arrête le mouvement """
        self.canvas.coords(
            self.id,
            x - self.rayon, y - self.rayon,
            x + self.rayon, y + self.rayon
        )
        self.vx = 0
        self.vy = 0
        self.en_mouvement = False

    # Normalisation de la vitesse
    def _normaliser_vitesse(self):
        """ Garde la vitesse constante après les rebonds """
        vitesse_actuelle = math.sqrt(self.vx**2 + self.vy**2)
        if vitesse_actuelle == 0:
            return
        facteur = self.vitesse / vitesse_actuelle
        self.vx *= facteur
        self.vy *= facteur
