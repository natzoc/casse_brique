#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 13/10/2025
# But : Classe représentant la raquette du joueur
#----------------------------------------------------------------------------#

import tkinter as tk

class Raquette:
    def __init__(self, canvas, x, y, largeur=100, hauteur=10, couleur="white", vitesse=10, parent=None):
        """
        Initialise la raquette du joueur.
        - canvas : zone de jeu (Tkinter Canvas)
        - x, y : position initiale (coin supérieur gauche)
        - largeur, hauteur : dimensions de la raquette
        - couleur : couleur d’affichage
        - vitesse : nombre de pixels parcourus à chaque "frame"
        - parent : widget parent sur lequel les touches clavier sont écoutées
        """
        self.canvas = canvas
        self.largeur = largeur
        self.hauteur = hauteur
        self.vitesse = vitesse

        # Création graphique
        self.id = canvas.create_rectangle(
            x, y, x + largeur, y + hauteur,
            fill=couleur
        )

        # États de mouvement
        self.deplacement_gauche = False
        self.deplacement_droite = False

        # Raquette inactive au début (activée quand la balle démarre)
        self.actif = False

        # Détermine où écouter les touches clavier
        self._binding_widget = parent if parent is not None else canvas

        # Tente de donner le focus clavier au widget
        try:
            self._binding_widget.focus_set()
        except Exception:
            pass

        # Liaisons clavier
        self._binding_widget.bind("<KeyPress-Left>", self._touche_appuyee)
        self._binding_widget.bind("<KeyPress-Right>", self._touche_appuyee)
        self._binding_widget.bind("<KeyRelease-Left>", self._touche_relachee)
        self._binding_widget.bind("<KeyRelease-Right>", self._touche_relachee)

        # Fréquence de mise à jour (16 ms ≈ 60 FPS)
        self._tick_ms = 16
        self._en_marche = True

        # Lancement de la boucle de déplacement fluide
        self._deplacer_en_continu()

    #----------------------#
    #  GESTION DU CLAVIER
    #----------------------#
    def _touche_appuyee(self, event):
        """ Active le mouvement à gauche/droite lorsqu'une touche est pressée """
        if not self.actif:
            return  # ❌ Le joueur ne peut pas bouger avant le début du jeu

        if event.keysym == "Left":
            self.deplacement_gauche = True
        elif event.keysym == "Right":
            self.deplacement_droite = True

    def _touche_relachee(self, event):
        """ Stoppe le mouvement lorsque la touche est relâchée """
        if event.keysym == "Left":
            self.deplacement_gauche = False
        elif event.keysym == "Right":
            self.deplacement_droite = False

    #----------------------#
    #  DEPLACEMENT
    #----------------------#
    def deplacer(self, dx):
        """
        Déplace la raquette horizontalement de dx pixels.
        Gère aussi les collisions avec les bords gauche/droite.
        """
        coords = self.canvas.coords(self.id)
        if coords:
            # Empêche la raquette de sortir de l'écran
            if dx < 0 and coords[0] + dx < 0:
                dx = -coords[0]  # limite à gauche
            elif dx > 0 and coords[2] + dx > self.canvas.winfo_width():
                dx = self.canvas.winfo_width() - coords[2]  # limite à droite

            self.canvas.move(self.id, dx, 0)

    def _deplacer_en_continu(self):
        """
        Boucle de mise à jour appelée toutes les 16 ms (~60 fois par seconde).
        Si une touche est enfoncée, la raquette se déplace continuellement.
        """
        if self._en_marche:
            # 🔓 Le joueur ne peut bouger que si le jeu est actif
            if self.actif:
                if self.deplacement_gauche:
                    self.deplacer(-self.vitesse)
                if self.deplacement_droite:
                    self.deplacer(self.vitesse)

            # Planifie le prochain appel (animation continue)
            self.canvas.after(self._tick_ms, self._deplacer_en_continu)

    def position(self):
        """ Renvoie les coordonnées actuelles de la raquette """
        return self.canvas.coords(self.id)
