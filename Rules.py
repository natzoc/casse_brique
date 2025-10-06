#----------------------------------------------------------------------------#
# Auteur : Loup Viornery                                                     #
# Date : 06/10/2025                                                          #
# But :                          #
# ToDo :                                                                     #
#----------------------------------------------------------------------------#

import tkinter as tk

class RulesAffichage:
    def __init__(self, parent):
        """
        Crée et affiche la zone d'information contenant le score et les vies.
        parent : fenêtre principale (tk.Tk)
        """
        self.parent = parent

        # Frame en bas de la fenêtre
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