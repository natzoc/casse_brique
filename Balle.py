#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 13/10/2025
# But : Classe représentant la balle du casse-brique
#----------------------------------------------------------------------------#

import tkinter as tk
import random
import math
from Bonus import Bonus

class Balle:
    def __init__(self, canvas, x, y, rayon=8, couleur="white", vitesse=5, jeu=None):
        # Initialise la balle avec position, rayon, couleur et vitesse
        self.canvas = canvas
        self.jeu = jeu
        self.rayon = rayon
        self.couleur = couleur
        self.vitesse = vitesse

        # Création du cercle représentant la balle sur le canevas
        self.id = canvas.create_oval(
            x - rayon, y - rayon, x + rayon, y + rayon,
            fill=couleur, outline=""
        )

        self.vx = 0
        self.vy = 0
        self.en_mouvement = False

        # Compteur de points progressif par lancer
        self.score_par_brique = 10

        if jeu is not None:
            # Lie la touche espace pour lancer la balle si le jeu est actif
            jeu.fenetre.bind("<space>", self.lancer)

        # Lance la boucle de mouvement automatique
        self._boucle()

    # LANCEMENT DE LA BALLE
    def lancer(self, event=None):
        # Lance la balle si elle n'est pas déjà en mouvement, si le jeu est actif,
        # et s'il reste au moins 1 vie (empêche relance après Game Over)
        if not self.en_mouvement and self.jeu and getattr(self.jeu, "jeu_actif", True):
            # Vérifie via RulesAffichage le nombre de vies si disponible
            if self.jeu.rules_affichage and getattr(self.jeu.rules_affichage, "vies", 1) <= 0:
                # plus de vies -> ne lance pas
                return
            self.en_mouvement = True
            # Direction horizontale aléatoire
            self.vx = random.choice([-self.vitesse, self.vitesse])
            self.vy = -self.vitesse
            if self.jeu.raquette:
                self.jeu.raquette.actif = True
            # Réinitialise le compteur de points pour le nouveau lancer
            self.score_par_brique = 10

    # BOUCLE DE MOUVEMENT
    def _boucle(self):
        # Déplace la balle et gère les collisions si le jeu est actif
        if self.en_mouvement and getattr(self.jeu, "jeu_actif", True):
            self.deplacer()
            self._gerer_collisions()
        # Rappelle cette boucle toutes les 16ms (~60fps)
        self.canvas.after(16, self._boucle)

    # DEPLACEMENT
    def deplacer(self):
        # Déplace la balle selon ses vitesses horizontale et verticale
        self.canvas.move(self.id, self.vx, self.vy)

    # GESTION DES COLLISIONS
    def _gerer_collisions(self):
        # Récupère la position actuelle de la balle
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        largeur = self.canvas.winfo_width()
        hauteur = self.canvas.winfo_height()

        # Collision avec les murs gauche/droite
        if x1 <= 0:
            self.vx = abs(self.vx)
        elif x2 >= largeur:
            self.vx = -abs(self.vx)

        # Collision avec le mur haut
        if y1 <= 0:
            self.vy = abs(self.vy)

        # Collision avec le mur bas : perte de vie
        if y2 >= hauteur:
            self._perdre_vie()
            return

        # Collision avec la raquette
        if self.jeu and self.jeu.raquette:
            rx1, ry1, rx2, ry2 = self.jeu.raquette.position()
            if y2 >= ry1 and y1 <= ry2 and x2 >= rx1 and x1 <= rx2 and self.vy > 0:
                # Calcul de l’angle de rebond selon la position sur la raquette
                milieu_raquette = (rx1 + rx2) / 2
                distance = (x1 + self.rayon - milieu_raquette) / (self.jeu.raquette.largeur / 2)
                angle = distance * (math.pi / 3)
                self.vx = self.vitesse * math.sin(angle)
                self.vy = -self.vitesse * math.cos(angle)
                # Réinitialisation du compteur de points par lancer
                self.score_par_brique = 10

        # Collision avec les briques
        briques_a_supprimer = []
        for brique_id in self.jeu.briques:
            bx1, by1, bx2, by2 = self.canvas.coords(brique_id)
            if (x2 >= bx1 and x1 <= bx2 and y2 >= by1 and y1 <= by2):
                briques_a_supprimer.append(brique_id)
                self.vy = -self.vy
                if self.jeu.rules_affichage:
                    self.jeu.rules_affichage.maj_score(self.score_par_brique)
                    # Incrémente le score pour le prochain impact
                    self.score_par_brique += 10

                # Génération aléatoire d’un bonus
                if self.jeu.bonus_actives.get() and random.random() < 0.15:
                    type_bonus = random.choice(["agrandir", "multi", "reduire", "ralentir"])
                    bx = (bx1 + bx2) / 2
                    by = (by1 + by2) / 2
                    bonus = Bonus(self.canvas, bx, by, type_bonus, self.jeu)
                    self.jeu.bonus_actifs.append(bonus)
                break

        # Supprime les briques touchées
        for bid in briques_a_supprimer:
            self.canvas.delete(bid)
            if bid in self.jeu.briques:
                self.jeu.briques.remove(bid)

        # Vérifie si toutes les briques sont détruites
        if not self.jeu.briques:
            self.jeu.victoire()

        # Ajuste la vitesse pour rester constante
        self._normaliser_vitesse()

    # PERTE DE VIE
    def _perdre_vie(self):
        # Arrête la balle et permet le relancement si le joueur a encore des vies
        self.en_mouvement = False
        if self.jeu:
            # On laisse RulesAffichage.perdre_vie gérer la décrémentation des vies
            # et appeler jeu.game_over() si nécessaire.
            # Ici on s'assure que, sauf game over, le jeu pourra être réactivé pour relancer la balle.
            self.jeu.jeu_actif = True
        if self.jeu.rules_affichage:
            self.jeu.rules_affichage.perdre_vie()
        # Réinitialise les positions balle/raquette
        if self.jeu:
            self.jeu.reset_positions()

    # RESET POSITION
    def reset_position(self, x, y):
        # Replace la balle à la position x, y et arrête le mouvement
        self.canvas.coords(
            self.id,
            x - self.rayon, y - self.rayon,
            x + self.rayon, y + self.rayon
        )
        self.vx = 0
        self.vy = 0
        self.en_mouvement = False

    # NORMALISATION VITESSE
    def _normaliser_vitesse(self):
        # Ajuste vx et vy pour que la vitesse totale reste constante
        vitesse_actuelle = math.sqrt(self.vx**2 + self.vy**2)
        if vitesse_actuelle == 0:
            return
        facteur = self.vitesse / vitesse_actuelle
        self.vx *= facteur
        self.vy *= facteur
