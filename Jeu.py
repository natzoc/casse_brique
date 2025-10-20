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
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse-Brique 2025")
        self.fenetre.geometry("800x600")
        self.fenetre.config(bg="#001f3f")
        self.fenetre.resizable(False, False)

        self.canvas = None
        self.raquette = None
        self.balle = None
        self.rules_affichage = None
        self.briques = []
        self.bonus_actifs = []
        self.bonus_actives = tk.BooleanVar(value=True)
        self.frame_menu = None

        # Menu principal
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain,
            action_options=self.afficher_options
        )

    # ================= AFFICHAGE DU TERRAIN =================
    def afficher_terrain(self):
        for widget in self.fenetre.winfo_children():
            widget.destroy()

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

        # Balle principale
        rayon_balle = 8
        x_centre = 380
        y_centre = 480 - rayon_balle - 5
        self.balle = Balle(
            self.canvas, x_centre, y_centre,
            rayon=rayon_balle, couleur="white", vitesse=5, jeu=self
        )

        self.briques.clear()
        self.afficher_briques()
        self.rules_affichage = RulesAffichage(self.fenetre)
        self.afficher_menu_jeu()  # Menu bas pendant le jeu

    # ================= MENU EN BAS =================
    def afficher_menu_jeu(self):
        if self.frame_menu is not None:
            self.frame_menu.destroy()

        self.frame_menu = tk.Frame(self.fenetre, bg="#001f3f")
        # Position proche du bas (mais pas collé)
        self.frame_menu.place(relx=0.5, rely=0.92, anchor="center")

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

    # ================= AFFICHAGE DES BRIQUES =================
    def afficher_briques(self):
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

    # ================= OPTIONS =================
    def afficher_options(self):
        for widget in self.fenetre.winfo_children():
            widget.destroy()

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
        for widget in self.fenetre.winfo_children():
            widget.destroy()
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain,
            action_options=self.afficher_options
        )

    # ================= BONUS / MALUS =================
    def modifier_taille_raquette(self, facteur, duree):
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
        if duree > 0:
            self.fenetre.after(duree, lambda: self.modifier_taille_raquette(1 / facteur, 0))

    def modifier_vitesse_raquette(self, facteur, duree):
        ancienne_vitesse = self.raquette.vitesse
        self.raquette.vitesse *= facteur
        if duree > 0:
            self.fenetre.after(duree, lambda: setattr(self.raquette, "vitesse", ancienne_vitesse))

    # ================= REINITIALISATION =================
    def reset_positions(self):
        if not self.canvas:
            return
        self.raquette.actif = False
        x0 = (760 - self.raquette.largeur) / 2
        y0 = 480
        self.canvas.coords(self.raquette.id, x0, y0, x0 + self.raquette.largeur, y0 + 10)
        self.balle.reset_position(380, 480 - self.balle.rayon - 5)

    def rejouer(self):
        for widget in self.fenetre.winfo_children():
            widget.destroy()
        self.briques.clear()
        self.bonus_actifs.clear()
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain,
            action_options=self.afficher_options
        )

    # ================= FIN DE PARTIE =================
    def victoire(self):
        if self.balle:
            self.balle.en_mouvement = False
        if self.raquette:
            self.raquette.actif = False

        if self.canvas:
            for bid in self.briques:
                self.canvas.delete(bid)
            self.briques.clear()
            self.canvas.create_text(
                380, 250,
                text="🏆 Victoire ! 🏆",
                font=("Arial", 28, "bold"),
                fill="gold"
            )

        self.afficher_menu_jeu()

    def game_over(self):
        if self.balle:
            self.balle.en_mouvement = False
        if self.raquette:
            self.raquette.actif = False

        if self.canvas:
            self.canvas.create_text(
                380, 250,
                text="💀 Game Over 💀",
                font=("Arial", 28, "bold"),
                fill="red"
            )

        self.afficher_menu_jeu()

    # ================= LANCEMENT =================
    def lancer(self):
        self.fenetre.mainloop()
