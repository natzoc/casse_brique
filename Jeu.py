#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 15/10/2025
# But : Interface graphique du jeu Casse-Brique (menu, options, terrain)
#----------------------------------------------------------------------------#

import tkinter as tk
import random
from Boutons import BoutonsJeu
from Rules import RulesAffichage
from Raquette import Raquette
from Balle import Balle
from Bonus import Bonus


class Jeu:
    def __init__(self):
        # Fenêtre principale
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse-Brique 2025")
        self.fenetre.geometry("800x600")
        self.fenetre.config(bg="#001f3f")
        self.fenetre.resizable(False, False)

        # Variables d’état
        self.canvas = None
        self.raquette = None
        self.balle = None
        self.rules_affichage = None
        self.briques = []
        self.bonus_actifs = []

        # Option : bonus/malus activés (par défaut True)
        self.bonus_actives = tk.BooleanVar(value=True)

        # Menu principal (affiché au démarrage)
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain,
            action_options=self.afficher_options
        )

        # frame_menu : référence au menu en bas pendant le jeu (créée dans afficher_menu_jeu)
        self.frame_menu = None

    #  AFFICHAGE DU TERRAIN DE JEU
    def afficher_terrain(self):
        # Affiche le terrain de jeu principal (canvas, raquette, balle, briques, HUD, menu bas) 
        # Supprime les widgets actuels (menu principal ou options)
        for widget in self.fenetre.winfo_children():
            widget.destroy()

        # Canvas de jeu
        self.canvas = tk.Canvas(
            self.fenetre,
            width=760,
            height=500,
            bg="#001f3f",
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        # Raquette 
        largeur_raquette = 100
        hauteur_raquette = 10
        x0 = (760 - largeur_raquette) / 2
        y0 = 480
        self.raquette = Raquette(
            self.canvas, x0, y0,
            largeur=largeur_raquette,
            hauteur=hauteur_raquette,
            parent=self.fenetre
        )

        # Balle 
        rayon_balle = 8
        x_centre = 380
        y_centre = 480 - rayon_balle - 5
        self.balle = Balle(
            self.canvas, x_centre, y_centre,
            rayon=rayon_balle, couleur="white", vitesse=5, jeu=self
        )

        # Briques 
        self.briques.clear()
        self.afficher_briques()

        # Score et vies (HUD bas) 
        self.rules_affichage = RulesAffichage(self.fenetre)

        # Menu de jeu (Rejouer / Options / Quitter) en bas 
        self.afficher_menu_jeu()

    #  MENU EN BAS DU JEU (pendant la partie)
    def afficher_menu_jeu(self):
        # Affiche le menu de jeu contenant Rejouer / Options / Quitter 
        # Si un ancien frame_menu existe, on le détruit d'abord
        if self.frame_menu is not None:
            try:
                self.frame_menu.destroy()
            except Exception:
                pass

        self.frame_menu = tk.Frame(self.fenetre, bg="#001f3f")
        self.frame_menu.pack(side="bottom", pady=10)

        btn_rejouer = tk.Button(
            self.frame_menu, text="🔁 Rejouer", font=("Arial", 12, "bold"),
            bg="white", fg="#001f3f", width=12, command=self.rejouer
        )
        btn_rejouer.pack(side="left", padx=10)

        btn_options = tk.Button(
            self.frame_menu, text="⚙️ Options", font=("Arial", 12, "bold"),
            bg="white", fg="#001f3f", width=12, command=self.afficher_options
        )
        btn_options.pack(side="left", padx=10)

        btn_quitter = tk.Button(
            self.frame_menu, text="❌ Quitter", font=("Arial", 12, "bold"),
            bg="white", fg="#001f3f", width=12, command=self.fenetre.destroy
        )
        btn_quitter.pack(side="left", padx=10)

    #  AFFICHAGE DES BRIQUES
    def afficher_briques(self):
        # Génère et place les briques sur le canvas
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

    #  INTERFACE D'OPTIONS (INTÉGRÉE) -> retourne au MENU PRINCIPAL sur Retour
    def afficher_options(self):
        # Affiche l'interface d'options dans la même fenêtre.
        # Le bouton 'Retour' renvoie au MENU PRINCIPAL (BoutonsJeu).
        # Supprime tout ce qui est affiché (canvas, HUD, menu bas, etc.)
        for widget in self.fenetre.winfo_children():
            widget.destroy()

        # Conteneur des options
        frame_options = tk.Frame(self.fenetre, bg="#001f3f")
        frame_options.pack(expand=True, fill="both")

        label_titre = tk.Label(
            frame_options,
            text="⚙️ Options du jeu",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#001f3f"
        )
        label_titre.pack(pady=30)

        # Case à cocher : activer / désactiver bonus/malus
        check_bonus = tk.Checkbutton(
            frame_options,
            text="Activer les bonus/malus",
            variable=self.bonus_actives,
            onvalue=True,
            offvalue=False,
            bg="#001f3f",
            fg="white",
            selectcolor="#001f3f",
            font=("Arial", 16)
        )
        check_bonus.pack(pady=10)

        # Retour : ramène au menu principal
        btn_retour = tk.Button(
            frame_options,
            text="⬅️ Retour au menu",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#001f3f",
            width=18,
            command=self.retour_menu_principal
        )
        btn_retour.pack(pady=30)

    def retour_menu_principal(self):
        # Retourne au menu principal (ré-affiche BoutonsJeu)
        # Supprime tous les widgets actuels (options ou autre)
        for widget in self.fenetre.winfo_children():
            widget.destroy()

        # Recrée le menu principal
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain,
            action_options=self.afficher_options
        )

    #  GESTION DES BONUS / MALUS (méthodes utilitaires)
    def modifier_taille_raquette(self, facteur, duree):
        # Modifie temporairement la taille de la raquette
        coords = self.canvas.coords(self.raquette.id)
        centre_x = (coords[0] + coords[2]) / 2
        largeur = (coords[2] - coords[0]) * facteur
        self.canvas.coords(
            self.raquette.id,
            centre_x - largeur / 2,
            coords[1],
            centre_x + largeur / 2,
            coords[3]
        )
        # Rétablit la taille après 'duree' ms (si duree > 0)
        if duree > 0:
            self.fenetre.after(duree, lambda: self.modifier_taille_raquette(1 / facteur, 0))

    def modifier_vitesse_raquette(self, facteur, duree):
        # Modifie temporairement la vitesse de déplacement de la raquette 
        ancienne_vitesse = self.raquette.vitesse
        self.raquette.vitesse *= facteur
        if duree > 0:
            self.fenetre.after(duree, lambda: setattr(self.raquette, "vitesse", ancienne_vitesse))

    def ajouter_balles_temp(self, nombre, duree):
        # Ajoute des balles temporaires pendant 'duree' ms 
        for _ in range(nombre):
            # place la nouvelle balle au centre de la balle principale
            x1, y1, x2, y2 = self.canvas.coords(self.balle.id)
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2
            nouvelle = Balle(self.canvas, x, y, self.balle.rayon, "lightblue", self.balle.vitesse, jeu=self)
            # supprime la balle temporaire après 'duree'
            if duree > 0:
                self.fenetre.after(duree, lambda b=nouvelle: self.supprimer_balle(b))

    def supprimer_balle(self, balle):
        # Supprime une balle temporaire en toute sécurité 
        try:
            self.canvas.delete(balle.id)
        except Exception:
            pass

    #  REINITIALISATION / REJOUER / VICTOIRE
    def reset_positions(self):
        # Replace la raquette et la balle au centre (après perte de vie) 
        if not self.canvas:
            return
        self.raquette.actif = False
        x0 = (760 - self.raquette.largeur) / 2
        y0 = 480
        self.canvas.coords(self.raquette.id, x0, y0, x0 + self.raquette.largeur, y0 + 10)
        self.balle.reset_position(380, 480 - self.balle.rayon - 5)

    def rejouer(self):
        # Réinitialise complètement le terrain et re-affiche le jeu 
        # Supprime tout et recrée le terrain
        for widget in self.fenetre.winfo_children():
            widget.destroy()
        # Réinitialise listes / états
        self.briques.clear()
        self.bonus_actifs.clear()
        # Recrée le menu principal (puis l'utilisateur clique Jouer)
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain,
            action_options=self.afficher_options
        )

    def victoire(self):
        # Affiche un message de victoire 
        if self.canvas:
            self.canvas.create_text(
                380, 250,
                text="🏆 Victoire ! 🏆",
                font=("Arial", 28, "bold"),
                fill="gold"
            )

    #  LANCEMENT DU JEU
    def lancer(self):
        self.fenetre.mainloop()
