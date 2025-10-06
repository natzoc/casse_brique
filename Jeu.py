#----------------------------------------------------------------------------#
# Auteur : Loup Viornery                                                     #
# Date : 06/10/2025                                                          #
# But : Interface graphique en utilisant tkinter                             #
# ToDo :                                                                     #
#----------------------------------------------------------------------------#

import tkinter as tk
from Boutons import BoutonsJeu

class Jeu:
    def __init__(self):
        # Fenêtre principale
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse-Brique 2025")
        self.fenetre.geometry("800x600")
        self.fenetre.config(bg="#001f3f")  # Bleu marine
        self.fenetre.resizable(False, False)

        # Menu principal
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain  # Action au clic sur "Jouer"
        )

        # Canvas de jeu (caché au départ)
        self.canvas = None

    def afficher_terrain(self):
        # Affiche le terrain de jeu
        self.canvas = tk.Canvas(
            self.fenetre,
            width=760,
            height=500,
            bg="#001f3f",   # Bleu marine
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        # --- Raquette ---
        largeur_raquette = 100
        hauteur_raquette = 10
        x0 = (760 - largeur_raquette) / 2
        y0 = 480
        self.raquette = self.canvas.create_rectangle(
            x0, y0, x0 + largeur_raquette, y0 + hauteur_raquette,
            fill="white"
        )

        # --- Balle ---
        rayon_balle = 8
        x_centre = 380
        y_centre = 480 - rayon_balle - 5  # juste au-dessus de la raquette
        self.balle = self.canvas.create_oval(
            x_centre - rayon_balle, y_centre - rayon_balle,
            x_centre + rayon_balle, y_centre + rayon_balle,
            fill="red"
        )

        # --- Briques (rangées en haut) ---
        self.afficher_briques()

    def afficher_briques(self):
        # Affiche des briques colorées en haut du canvas
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
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=couleurs[ligne % len(couleurs)],
                    outline=""
                )

    def lancer(self):
        # Démarre la boucle principale de l'interface graphique
        self.fenetre.mainloop()
