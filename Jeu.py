#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato                                  #
# Date : 12/10/2025                                                          #
# But : Interface principale du jeu Casse-Brique                              #
#----------------------------------------------------------------------------#

import tkinter as tk
from Boutons import BoutonsJeu
from Rules import RulesAffichage
from Raquette import Raquette
from Balle import Balle


class Jeu:
    def __init__(self):
        # Fenêtre principale
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse-Brique 2025")
        self.fenetre.geometry("800x600")
        self.fenetre.config(bg="#001f3f")
        self.fenetre.resizable(False, False)

        # Éléments du jeu
        self.canvas = None
        self.rules_affichage = None
        self.raquette = None
        self.balle = None
        self.briques = []

        # Menu d’accueil
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain
        )

    def afficher_terrain(self):
        # Affiche le terrain et instancie les objets du jeu
        self.canvas = tk.Canvas(
            self.fenetre,
            width=760,
            height=500,
            bg="#001f3f",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        self.fenetre.focus_set()

        # Raquette 
        largeur_raquette = 100
        hauteur_raquette = 10
        x0 = (760 - largeur_raquette) / 2
        y0 = 480
        self.raquette = Raquette(
            self.canvas, x0, y0,
            largeur=largeur_raquette, hauteur=hauteur_raquette,
            couleur="white", vitesse=12,
            parent=self.fenetre
        )

        # Briques
        self.afficher_briques()

        # Règles (score + vies)
        self.rules_affichage = RulesAffichage(self.fenetre)

        # Balle
        rayon_balle = 8
        x_centre = x0 + largeur_raquette / 2
        y_centre = y0 - rayon_balle - 5
        self.balle = Balle(
            self.canvas, x_centre, y_centre,
            rayon=rayon_balle, couleur="red", vitesse=6,
            jeu=self
        )

    def afficher_briques(self):
        # Affiche un ensemble de briques colorées
        couleurs = ["#ff5733", "#ffbd33", "#75ff33", "#33c1ff", "#c433ff"]
        largeur_brique = 70
        hauteur_brique = 20
        espacement = 5
        nb_colonnes = 10
        nb_lignes = 5

        for ligne in range(nb_lignes):
            for col in range(nb_colonnes):
                x1 = 20 + col * (largeur_brique + espacement)
                y1 = 20 + ligne * (hauteur_brique + espacement)
                x2 = x1 + largeur_brique
                y2 = y1 + hauteur_brique
                brique_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=couleurs[ligne % len(couleurs)],
                    outline=""
                )
                self.briques.append(brique_id)

    def reset_positions(self):
        # Réinitialise la position de la raquette et de la balle
        largeur_raquette = self.raquette.largeur
        x0 = (760 - largeur_raquette) / 2
        y0 = 480
        self.canvas.coords(
            self.raquette.id,
            x0, y0, x0 + largeur_raquette, y0 + self.raquette.hauteur
        )

        # Balle juste au-dessus de la raquette
        rayon = self.balle.rayon
        x_centre = x0 + largeur_raquette / 2
        y_centre = y0 - rayon - 5
        self.balle.reset_position(x_centre, y_centre)

    def victoire(self):
        # Affiche un message de victoire et ferme le jeu
        import tkinter.messagebox as msg
        msg.showinfo("Victoire", "Félicitations ! Vous avez détruit toutes les briques.")
        self.fenetre.destroy()

    def lancer(self):
        # Lance la boucle principale du jeu
        self.fenetre.mainloop()
