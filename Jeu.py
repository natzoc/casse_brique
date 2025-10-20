#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 15/10/2025
# But : Interface graphique du jeu Casse-Brique (menu, options, terrain)
#----------------------------------------------------------------------------#

import tkinter as tk
from Boutons import BoutonsJeu
from Rules import RulesAffichage
from Raquette import Raquette
from Balle import Balle
from Bonus import Bonus

class Jeu:
    def __init__(self):
        # Initialise la fenêtre principale
        self.fenetre = tk.Tk()
        self.fenetre.title("Casse-Brique 2025")
        self.fenetre.geometry("800x600")
        self.fenetre.config(bg="#001f3f")
        self.fenetre.resizable(False, False)

        # Initialisation des composants du jeu
        self.canvas = None
        self.raquette = None
        self.balle = None
        self.rules_affichage = None
        self.briques = []
        self.bonus_actifs = []
        self.bonus_actives = tk.BooleanVar(value=True)
        self.frame_menu = None

        # Scores
        self.score_actuel = 0
        self.meilleur_score = 0
        self.label_meilleur_score_menu = None
        self.label_meilleur_score_jeu = None

        # Indique si le jeu est gelé (victoire ou défaite)
        self.freeze = False

        # Menu principal
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain,
            action_options=self.afficher_options
        )
        # Affiche le meilleur score dans le menu
        self.afficher_meilleur_score_menu()

    # AFFICHAGE MEILLEUR SCORE MENU
    def afficher_meilleur_score_menu(self):
        # Supprime l'ancien label si nécessaire
        if self.label_meilleur_score_menu:
            self.label_meilleur_score_menu.destroy()
        # Crée un nouveau label pour le meilleur score
        self.label_meilleur_score_menu = tk.Label(
            self.fenetre,
            text=f"Meilleur score : {self.meilleur_score}",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#001f3f"
        )
        self.label_meilleur_score_menu.place(relx=0.5, rely=0.95, anchor="center")

    # AFFICHAGE MEILLEUR SCORE DANS LE JEU
    def afficher_meilleur_score_jeu(self):
        if self.label_meilleur_score_jeu:
            self.label_meilleur_score_jeu.destroy()
        self.label_meilleur_score_jeu = tk.Label(
            self.fenetre,
            text=f"Meilleur score : {self.meilleur_score}",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#001f3f"
        )
        self.label_meilleur_score_jeu.place(relx=0.5, rely=0.88, anchor="center")

    # AFFICHAGE DU TERRAIN DE JEU
    def afficher_terrain(self):
        # Débloque le jeu
        self.freeze = False

        # Supprime tous les widgets existants
        for widget in self.fenetre.winfo_children():
            widget.destroy()

        # Reset score actuel
        self.score_actuel = 0

        # Création du canvas pour le terrain
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

        # Initialisation des briques
        self.briques.clear()
        self.afficher_briques()

        # Affichage du score et du menu bas
        self.rules_affichage = RulesAffichage(self.fenetre, self)
        self.afficher_menu_jeu()
        self.afficher_meilleur_score_jeu()

    # MENU EN BAS DU JEU
    def afficher_menu_jeu(self):
        if self.frame_menu is not None:
            self.frame_menu.destroy()

        self.frame_menu = tk.Frame(self.fenetre, bg="#001f3f")
        self.frame_menu.place(relx=0.5, rely=0.92, anchor="center")

        # Bouton Menu
        btn_rejouer = tk.Button(
            self.frame_menu, text="Menu", font=("Arial", 12, "bold"),
            bg="white", fg="#001f3f", width=12, command=self.retour_menu_principal
        )
        btn_rejouer.pack(side="left", padx=10)

        # Bouton Options
        btn_options = tk.Button(
            self.frame_menu, text="Options", font=("Arial", 12, "bold"),
            bg="white", fg="#001f3f", width=12, command=self.afficher_options
        )
        btn_options.pack(side="left", padx=10)

        # Bouton Quitter
        btn_quitter = tk.Button(
            self.frame_menu, text="Quitter", font=("Arial", 12, "bold"),
            bg="white", fg="#001f3f", width=12, command=self.fenetre.destroy
        )
        btn_quitter.pack(side="left", padx=10)

    # AFFICHAGE DES BRIQUES
    def afficher_briques(self):
        couleurs = ["#ff5733", "#ffbd33", "#75ff33", "#33c1ff", "#c433ff"]
        largeur_brique = 70
        hauteur_brique = 20
        espacement = 5
        nb_colonnes = 10
        nb_lignes = 5

        # Création des briques
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

    # AFFICHAGE DU MENU OPTIONS
    def afficher_options(self):
        # Supprime tous les widgets existants
        for widget in self.fenetre.winfo_children():
            widget.destroy()

        frame_options = tk.Frame(self.fenetre, bg="#001f3f")
        frame_options.pack(expand=True, fill="both")

        # Titre Options
        label_titre = tk.Label(
            frame_options,
            text="Options du jeu",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#001f3f"
        )
        label_titre.pack(pady=30)

        # Case à cocher pour activer/désactiver les bonus
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

        # Bouton Retour au menu
        btn_retour = tk.Button(
            frame_options,
            text="Retour",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#001f3f",
            width=18,
            command=self.retour_menu_principal
        )
        btn_retour.pack(pady=30)

    # RETOUR AU MENU PRINCIPAL
    def retour_menu_principal(self):
        for widget in self.fenetre.winfo_children():
            widget.destroy()
        self.boutons = BoutonsJeu(
            parent=self.fenetre,
            couleur_fond="#001f3f",
            action_jouer=self.afficher_terrain,
            action_options=self.afficher_options
        )
        self.afficher_meilleur_score_menu()

    # BONUS / MALUS
    def modifier_taille_raquette(self, facteur, duree):
        # Ajuste la taille de la raquette selon le facteur
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
            # Réinitialise après la durée
            self.fenetre.after(duree, lambda: self.modifier_taille_raquette(1 / facteur, 0))

    def modifier_vitesse_raquette(self, facteur, duree):
        # Ajuste la vitesse de la raquette
        ancienne_vitesse = self.raquette.vitesse
        self.raquette.vitesse *= facteur
        if duree > 0:
            self.fenetre.after(duree, lambda: setattr(self.raquette, "vitesse", ancienne_vitesse))

    # REINITIALISATION DES POSITIONS
    def reset_positions(self):
        if not self.canvas:
            return
        self.raquette.actif = False
        x0 = (760 - self.raquette.largeur) / 2
        y0 = 480
        self.canvas.coords(self.raquette.id, x0, y0, x0 + self.raquette.largeur, y0 + 10)
        self.balle.reset_position(380, 480 - self.balle.rayon - 5)

    # FIN DE PARTIE - VICTOIRE
    def victoire(self):
        self.freeze = True
        if self.balle:
            self.balle.en_mouvement = False
        if self.raquette:
            self.raquette.actif = False

        if self.canvas:
            # Supprime toutes les briques et affiche message victoire
            for bid in self.briques:
                self.canvas.delete(bid)
            self.briques.clear()
            self.canvas.create_text(
                380, 250,
                text="🏆 Victoire 🏆",
                font=("Arial", 28, "bold"),
                fill="gold"
            )

        # Met à jour le meilleur score si nécessaire
        if self.score_actuel > self.meilleur_score:
            self.meilleur_score = self.score_actuel

        # Affiche le menu bas et le score
        self.afficher_menu_jeu()
        self.afficher_meilleur_score_jeu()

    # FIN DE PARTIE - GAME OVER
    def game_over(self):
        self.freeze = True
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

        if self.score_actuel > self.meilleur_score:
            self.meilleur_score = self.score_actuel

        self.afficher_menu_jeu()
        self.afficher_meilleur_score_jeu()

    # LANCEMENT DE LA BOUCLE PRINCIPALE
    def lancer(self):
        self.fenetre.mainloop()
