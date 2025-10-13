#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato                                  #
# Date : 13/10/2025                                                          #
# But : Classe représentant la raquette du joueur                            #
#----------------------------------------------------------------------------#

import tkinter as tk

class Raquette:
    def __init__(self, canvas, x, y, largeur=100, hauteur=10, couleur="white", vitesse=10, parent=None):
        self.canvas = canvas
        self.largeur = largeur
        self.hauteur = hauteur
        self.vitesse = vitesse
        self.id = canvas.create_rectangle(
            x, y, x + largeur, y + hauteur,
            fill=couleur
        )

        # États de déplacement
        self.deplacement_gauche = False
        self.deplacement_droite = False

        # Raquette inactive tant que la partie n'a pas commencé
        self.actif = False

        # Widget sur lequel binder les touches
        self._binding_widget = parent if parent is not None else canvas

        try:
            self._binding_widget.focus_set()
        except Exception:
            pass

        # Bind des touches directionnelles
        self._binding_widget.bind("<KeyPress-Left>", self._touche_appuyee)
        self._binding_widget.bind("<KeyPress-Right>", self._touche_appuyee)
        self._binding_widget.bind("<KeyRelease-Left>", self._touche_relachee)
        self._binding_widget.bind("<KeyRelease-Right>", self._touche_relachee)

        # Démarre la boucle de déplacement fluide
        self._tick_ms = 16  # ~60 FPS
        self._en_marche = True
        self._deplacer_en_continu()

    # Gestion du clavier
    def _touche_appuyee(self, event):
        # Déclenche le mouvement lorsqu’une touche est appuyée
        if not self.actif:
            return  # ❌ Ne bouge pas si le jeu n'a pas commencé
        if event.keysym == "Left":
            self.deplacement_gauche = True
        elif event.keysym == "Right":
            self.deplacement_droite = True

    def _touche_relachee(self, event):
        # Arrête le mouvement lorsqu’une touche est relâchée
        if event.keysym == "Left":
            self.deplacement_gauche = False
        elif event.keysym == "Right":
            self.deplacement_droite = False

    # Déplacement
    def deplacer(self, dx):
        # Déplace la raquette horizontalement de dx pixels
        coords = self.canvas.coords(self.id)
        if coords:
            if dx < 0 and coords[0] + dx < 0:
                dx = -coords[0]
            elif dx > 0 and coords[2] + dx > self.canvas.winfo_width():
                dx = self.canvas.winfo_width() - coords[2]
            self.canvas.move(self.id, dx, 0)

    def _deplacer_en_continu(self):
        # Boucle de déplacement fluide
        if self._en_marche:
            # 🔓 On ne bouge que si la partie est active
            if self.actif:
                if self.deplacement_gauche:
                    self.deplacer(-self.vitesse)
                if self.deplacement_droite:
                    self.deplacer(self.vitesse)
            self.canvas.after(self._tick_ms, self._deplacer_en_continu)

    def position(self):
        # Renvoie les coordonnées actuelles de la raquette
        return self.canvas.coords(self.id)
