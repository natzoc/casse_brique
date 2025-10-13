#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato                                  #
# Date : 06/10/2025                                                          #
# But :                          
# ToDo :                                                                     #
#----------------------------------------------------------------------------#

class Brique:
    def __init__(self, canvas, x1, y1, x2, y2, couleur):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="")
