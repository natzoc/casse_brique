#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato                                  #
# Date : 06/10/2025                                                          #
# But :                          #
# ToDo :                                                                     #
#----------------------------------------------------------------------------#

class Raquette:
    def __init__(self, canvas, x, y, largeur=100, hauteur=10, couleur="white"):
        self.canvas = canvas
        self.largeur = largeur
        self.hauteur = hauteur
        self.id = canvas.create_rectangle(
            x, y, x + largeur, y + hauteur,
            fill=couleur
        )

    def deplacer(self, dx):
        self.canvas.move(self.id, dx, 0)
