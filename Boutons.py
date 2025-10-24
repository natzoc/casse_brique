#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 13/10/2025
# But : Menu principal du jeu (Jouer, Options, Quitter)
#----------------------------------------------------------------------------#

import tkinter as tk

"""
Classe gérant le menu principal du jeu :
elle affiche les boutons "Jouer", "Options" et "Quitter",
et relie chacun à son action correspondante.
"""

class BoutonsJeu:
    def __init__(self, parent, couleur_fond="#001f3f", action_jouer=None, action_options=None):
        # Initialise le menu principal avec 3 boutons : Jouer, Options, Quitter
        self.parent = parent
        self.action_jouer = action_jouer
        self.action_options = action_options

        # Création d'un frame pour contenir les boutons
        self.frame = tk.Frame(parent, bg=couleur_fond)
        self.frame.pack(expand=True)

        # Bouton "Jouer"
        self.bouton_jouer = tk.Button(
            self.frame,
            text="Jouer",
            font=("Arial", 16, "bold"),
            bg="white",
            fg=couleur_fond,
            width=15,
            height=2,
            command=self.lancer_jeu  # Appelle la fonction lancer_jeu
        )
        self.bouton_jouer.pack(pady=15)

        # Bouton "Options"
        self.bouton_options = tk.Button(
            self.frame,
            text="Options",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=couleur_fond,
            width=15,
            height=2,
            command=self.ouvrir_options  # Appelle la fonction ouvrir_options
        )
        self.bouton_options.pack(pady=10)

        # Bouton "Quitter"
        self.bouton_quitter = tk.Button(
            self.frame,
            text="Quitter",
            font=("Arial", 14),
            bg="white",
            fg=couleur_fond,
            width=15,
            height=2,
            command=parent.destroy  # Ferme la fenêtre principale
        )
        self.bouton_quitter.pack(pady=10)

    def lancer_jeu(self):
        # Détruit le menu et démarre la partie
        if self.action_jouer:
            self.frame.destroy()  # Supprime le menu
            self.action_jouer()   # Lance la fonction de démarrage du jeu

    def ouvrir_options(self):
        # Ouvre le menu des options
        if self.action_options:
            self.frame.destroy()  # Supprime le menu
            self.action_options() # Lance la fonction des options
