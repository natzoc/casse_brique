#----------------------------------------------------------------------------#
# Auteur : Loup Viornery                                                     #
# Date : 06/10/2025                                                          #
# But :                          #
# ToDo :                                                                     #
#----------------------------------------------------------------------------#

class Balle:
    def __init__(self, canvas, x, y, rayon=8, couleur="red"):
        self.canvas = canvas
        self.rayon = rayon
        self.id = canvas.create_oval(
            x - rayon, y - rayon,
            x + rayon, y + rayon,
            fill=couleur
        )
        self.vx = 3
        self.vy = -3

    def deplacer(self):
        self.canvas.move(self.id, self.vx, self.vy)
