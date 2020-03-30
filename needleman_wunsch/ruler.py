import numpy as np
from colorama import init, Fore, Style
from random import randrange
import time

init(convert=True)  # nécessaire car sinon la coloration du signe "=" pose problème


def generator(n):  # génère un str de taille n
    s = ""
    for k in range(n):
        s = s + chr(97+randrange(26))
    return s


def red_text(text):  # coloré du texte en rouge
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


class Ruler:
    """
    calcul de la distance et du meilleur "alignement" entre deux strings

    """

    C = np.ones([26, 26], dtype=int)
    # création de la matrice de comptage par défaut
    C = C - np.eye(26, dtype=int)

    def __init__(self, c1, c2, g=1, S=C):

        self.c1 = c1
        self.c2 = c2
        self.gap = g
        # la matrice de comptage ou la matrice pénalité est définie par C par défaut
        self.comptage = S
        self.distance = "None"
        self.retranchement = None
        # on distingue le cas des majuscules et minuscules
        if 65 <= ord(self.c1[0]) <= 90:
            self.retranchement = 65
        else:
            self.retranchement = 97

    def compute(self):  # on construit dans cette fonction la matrice score et la matrice map

        ligne = len(self.c2) + 1
        colonne = len(self.c1) + 1

        # la matrice score nous permettra d'obtenir la distance entre les deux chaînes
        Score = np.zeros([ligne, colonne])
        # la matrice Map nous permettra de savoir quel chemin suivre pour réaliser le meilleur alignement
        Map = np.zeros([ligne, colonne])

        for i in range(1, ligne):
            Score[i, 0] = Score[i-1, 0] + self.gap
            Map[i, 0] = 1  # up = 1

        for j in range(1, colonne):
            Score[0, j] = Score[0, j-1] + self.gap
            Map[0, j] = -1  # left = -1 et donc diag = 0

        for i in range(1, ligne):
            for j in range(1, colonne):
                q_diag = Score[i-1, j-1] + self.comptage[ord(self.c1[j-1])-self.retranchement, ord(
                    self.c2[i-1])-self.retranchement]  # on se ramène à un nombre entre 0 et 25
                q_up = Score[i-1, j] + self.gap
                q_left = Score[i, j-1] + self.gap
                L = [q_left, q_diag, q_up]
                Score[i, j] = min(L)
                # -1 pour garder le code left/diag/up cité plus haut
                Map[i, j] = L.index(min(L))-1

        self.distance = int(Score[-1, -1])
        self.Map = Map

    def report(self):   # on parcourt la matrice Map pour savoir quelles modifications apporter aux chaînes
        top = ""
        bottom = ""
        i, j = len(self.c2), len(self.c1)
        while (i, j) != (0, 0):
            if self.Map[i, j] == 0:  # cas où on tombe sur "diag" et que les lettres sont les mêmes
                if self.c1[j-1] == self.c2[i-1]:
                    top = self.c1[j-1] + top
                    bottom = self.c2[i-1] + bottom
                else:  # cas où on tombe sur "diag" mais que les lettres sont diff
                    top = red_text(self.c1[j-1]) + top
                    bottom = red_text(self.c2[i-1]) + bottom
                i, j = i-1, j-1

            elif self.Map[i, j] == -1:  # cas où on tombe sur un "left"
                top = self.c1[j-1] + top
                bottom = red_text("=") + bottom
                i, j = i, j-1

            else:  # cas où on tombe sur un "up"
                top = red_text("=") + top
                bottom = self.c2[i-1] + bottom
                i, j = i-1, j

        return top, bottom


# start_time = time.perf_counter()


# a,b = generator(100),generator(100)
# a,b = "ACTGCCAACAGTC","ACCTGCGAACAGC"
# ruler = Ruler (a,b)
# ruler.compute()
# print(ruler.distance)
# top,bottom = ruler.report()

# print(top)
# print(bottom)

# print ("temps d'éxecution :", time.perf_counter() - start_time, "secondes")