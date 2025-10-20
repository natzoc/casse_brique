#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato                                  
# Date : 06/10/2025                                                          
# But : Classe permettant de lancer le jeu de casse-brique                         
# Lien GitHub : https://github.com/natzoc/casse_brique.git                                                                     
#----------------------------------------------------------------------------#

from Jeu import Jeu

if __name__ == "__main__":
    app = Jeu()
    app.lancer()
    print("Jeu lancé avec succès !")