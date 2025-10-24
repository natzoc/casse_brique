#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato
# Date : 13/10/2025
# But : Classe représentant la raquette du joueur
#----------------------------------------------------------------------------#

"""
Classe représentant la raquette contrôlée par le joueur.
Elle gère le déplacement horizontal via les touches du clavier, 
empêche la sortie des limites du terrain,
 et met à jour la position en continu pendant le jeu.

"""

class Raquette:
    def __init__(self, canvas, x, y, largeur=100, hauteur=10, couleur="white", vitesse=10, parent=None):
        # Initialise la raquette du joueur avec position, dimensions et vitesse
        self.canvas = canvas
        self.largeur = largeur
        self.hauteur = hauteur
        self.vitesse = vitesse

        # Création graphique de la raquette
        self.id = canvas.create_rectangle(
            x, y, x + largeur, y + hauteur,
            fill=couleur
        )

        # États de déplacement
        self.deplacement_gauche = False
        self.deplacement_droite = False

        # Raquette inactive au départ (activée quand la balle démarre)
        self.actif = False

        # Widget sur lequel écouter les touches clavier
        self._binding_widget = parent if parent is not None else canvas

        # Essaye de donner le focus clavier
        try:
            self._binding_widget.focus_set()
        except Exception:
            pass

        # Liaisons clavier pour gauche/droite
        self._binding_widget.bind("<KeyPress-Left>", self._touche_appuyee)
        self._binding_widget.bind("<KeyPress-Right>", self._touche_appuyee)
        self._binding_widget.bind("<KeyRelease-Left>", self._touche_relachee)
        self._binding_widget.bind("<KeyRelease-Right>", self._touche_relachee)

        # Intervalle de mise à jour (~60 FPS)
        self._tick_ms = 16
        self._en_marche = True

        # Lance la boucle de déplacement continu
        self._deplacer_en_continu()

    # GESTION DES TOUCHES APPUYÉES
    def _touche_appuyee(self, event):
        # Active le déplacement si le jeu est actif
        if not self.actif:
            return

        if event.keysym == "Left":
            self.deplacement_gauche = True
        elif event.keysym == "Right":
            self.deplacement_droite = True

    # GESTION DES TOUCHES RELÂCHÉES
    def _touche_relachee(self, event):
        # Stoppe le déplacement quand la touche est relâchée
        if event.keysym == "Left":
            self.deplacement_gauche = False
        elif event.keysym == "Right":
            self.deplacement_droite = False

    # DEPLACEMENT HORIZONTAL
    def deplacer(self, dx):
        # Déplace la raquette de dx pixels horizontalement
        coords = self.canvas.coords(self.id)
        if coords:
            # Empêche la raquette de sortir des bords du canvas
            if dx < 0 and coords[0] + dx < 0:
                dx = -coords[0]  # limite à gauche
            elif dx > 0 and coords[2] + dx > self.canvas.winfo_width():
                dx = self.canvas.winfo_width() - coords[2]  # limite à droite

            # Applique le déplacement
            self.canvas.move(self.id, dx, 0)

    # BOUCLE DE DÉPLACEMENT CONTINU
    def _deplacer_en_continu(self):
        # Boucle appelée toutes les 16 ms pour le déplacement fluide
        if self._en_marche:
            # Déplacement uniquement si le jeu est actif
            if self.actif:
                if self.deplacement_gauche:
                    self.deplacer(-self.vitesse)
                if self.deplacement_droite:
                    self.deplacer(self.vitesse)

            # Planifie le prochain appel pour continuité
            self.canvas.after(self._tick_ms, self._deplacer_en_continu)

    # RENVOIE LA POSITION ACTUELLE
    def position(self):
        # Renvoie les coordonnées [x1, y1, x2, y2] de la raquette
        return self.canvas.coords(self.id)
