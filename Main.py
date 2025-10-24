#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato                                  
# Date : 06/10/2025                                                          
# But : Classe permettant de lancer le jeu de casse-brique                         
# Lien GitHub : https://github.com/natzoc/casse_brique.git                                                                     
#----------------------------------------------------------------------------#

from Jeu import Jeu

"""
Point d'entrée principal pour lancer le jeu de casse-brique.
Crée une instance de la classe Jeu et démarre la boucle principale."""

if __name__ == "__main__":
    app = Jeu()
    app.lancer()
    print("Jeu lancé avec succès !")