#----------------------------------------------------------------------------#
# Auteur : Loup Viornery & Nathan Zoccarato                                  #
# Date : 12/10/2025                                                          #
# But : Affichage du score et des vies                                       #
#----------------------------------------------------------------------------#

import tkinter as tk
import tkinter.messagebox as msg


class RulesAffichage:
    def __init__(self, parent):
        self.parent = parent

        # Frame en bas
        self.frame_info = tk.Frame(parent, bg="#001f3f")
        self.frame_info.pack(side="bottom", fill="x")

        # Score
        self.score_label = tk.Label(
            self.frame_info,
            text="Score : 0",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#001f3f"
        )
        self.score_label.pack(side="left", padx=20, pady=10)

        # Vies
        self.vies_label = tk.Label(
            self.frame_info,
            text="Vies : 3",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#001f3f"
        )
        self.vies_label.pack(side="right", padx=20, pady=10)

    def maj_score(self, points):
        # Met à jour le score en ajoutant des points
        texte = self.score_label.cget("text")
        score_actuel = int(texte.split(": ")[1])
        nouveau = score_actuel + points
        self.score_label.config(text=f"Score : {nouveau}")

    def perdre_vie(self):
        # Réduit le nombre de vies de 1 et gère la fin de partie si nécessaire
        texte = self.vies_label.cget("text")
        vies_actuelles = int(texte.split(": ")[1])
        nouvelles_vies = vies_actuelles - 1
        self.vies_label.config(text=f"Vies : {nouvelles_vies}")

        if nouvelles_vies <= 0:
            self._fin_partie("défaite")

    def _fin_partie(self, resultat):
        # Affiche une boîte de dialogue de fin de partie et ferme la fenêtre principale
        msg.showinfo("Fin de partie", f"Partie terminée : {resultat.upper()}")
        self.parent.destroy()
        