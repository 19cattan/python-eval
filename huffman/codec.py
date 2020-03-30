from collections import Counter


class Noeud():
    """
    classe qui permet de définir un noeud par son string, l'occurence totale des caractères du string, de son fils gauche, et de son fils droit

    """

    def __init__(self, string, occu, fils_gauche, fils_droit):
        self.string = string
        self.occu = occu
        self.fils_gauche = fils_gauche
        self.fils_droit = fils_droit

    def __str__(self):

        if self.fils_gauche != None and self.fils_droit != None:
            return (f"{self.string} d'occurrence {self.occu} de fils {self.fils_gauche.string} et {self.fils_droit.string}")

        if self.fils_gauche == None and self.fils_droit != None:
            return (f"{self.string} d'occurrence {self.occu} de fils None et {self.fils_droit.string}")

        if self.fils_gauche != None and self.fils_droit == None:
            return (f"{self.string} d'occurrence {self.occu} de fils {self.fils_gauche.string} et None")

        if self.fils_gauche == None and self.fils_droit == None:
            return (f"{self.string} d'occurrence {self.occu} de fils None et None")


class TreeBuilder():

    """
    classe qui permet de construire l'arbre à partir d'une chaîne de cractère

    """

    def __init__(self, text):
        self.text = text

    def tree(self):
        text = self.text
        # Retourne un dictionnaire dont les clés sont les caractères et les définitions leurs occurences
        D = Counter(text)
        Occurences, Lettres = [], []

        # on crée une liste des cractères et une liste des occurences par ordre croissant d'occurence
        for a, b in sorted(D.items(), key=lambda x: x[1]):
            Lettres.append(a)
            Occurences.append(b)

        n = len(Lettres)
        # On crée une liste liste_noeuds des noeuds que l'on traitera pour construire l'arbre
        liste_noeuds = [0 for k in range(n)]

        for i in range(n):
            # on crée les feuilles de base
            liste_noeuds[i] = Noeud(Lettres[i], Occurences[i], None, None)

        while len(liste_noeuds) >= 2:  # On va créer les nouveaux noeuds, en parcourant l'arbre en partant des feuilles, et les classer par occurence croissante dans la liste liste_noeuds 
            a, b = liste_noeuds[0], liste_noeuds[1]
            # un noeud est crée par la concaténation des str et la somme des occurences, on lui indique qui sont ses enfants et on supprime les enfants de la liste des nouveaux noeuds     
            nouveau_noeud = Noeud(a.string + b.string, a.occu + b.occu, a, b)
            del liste_noeuds[0]
            del liste_noeuds[0]

            liste_noeuds.insert(0, nouveau_noeud)
            c = 1

            # On insère le nouveau noeud de manière ordonnée dans la liste liste_noeuds
            while c < len(liste_noeuds) and liste_noeuds[c].occu <= nouveau_noeud.occu:
                liste_noeuds[c], liste_noeuds[c -
                                              1] = liste_noeuds[c-1], liste_noeuds[c]
                c += 1

        return liste_noeuds[0]  # on obtient la racine de l'arbre


class Codec():

    """
    Classe qui permet, à partir de l'arbre reçu par la méthode .tree() de la classe TreeBuilder, de coder et décoder une chaîne de caractère

    """

    def __init__(self, tree):
        self.tree = tree

    def codage(self, text):  # Fonction qui associe à chaque caractère (les feuilles) un code en binaire
        racine = self.tree  # la racine constitue le noeud le plus haut
        A = Counter(racine.string)
        Lettres = []
        code = {}
        for i in A.keys():
            Lettres.append(i)
        for let in Lettres:
            noeud = racine
            chemin = ''

            while len(noeud.string) > 1:  # tant que le noeud n'est pas une feuille on parcourt l'arbre en s'assurant de suivre le chemin de la lettre, et en codant la lettre au fur et à mesure
                a = noeud.fils_gauche
                b = noeud.fils_droit
                if let in a.string:
                    noeud = a
                    chemin = chemin + '0'
                else:
                    noeud = b
                    chemin = chemin + '1'
            code[let] = chemin

        return code

    def encode(self, text):  # encode un texte en assignant à chaque caractère son code
        code = self.codage(text)
        rep = ''
        for i in text:
            rep = rep + code[i]
        return rep

    def decode(self, encoded):  # décode un message codé
        res = ''
        racine = self.tree
        noeud = racine  # en partant de la racine

        for i in encoded:
            if i == '0':
                # on parcourt l'arbre en suivant les 0 et 1...
                noeud = noeud.fils_gauche
            else:
                noeud = noeud.fils_droit
            # ... et on vérifié à chaque étape si l'on est arrivé à la feuille en question
            if len(noeud.string) == 1:
                res = res + noeud.string
                noeud = racine

        return res


text_test = "Insérez le message que vous voulez tester"

builder = TreeBuilder(text_test)
binary_tree = builder.tree()

codec = Codec(binary_tree)
encoded = codec.encode(text_test)
decoded = codec.decode(encoded)

print(encoded)
print(decoded)

if decoded != text_test:
    print("Game over")