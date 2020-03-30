import sys
from ruler import Ruler #on importe notre classe

file_name = sys.argv[1] #sys.argv permet de créer une liste avec les arguments rentrés dans cmd
fichier1 = open(file_name, "r") #on met en deuxième le nom du fichier à lire

L = [] #L est une liste contenant les strings contenu dans le fichier texte

for ligne in fichier1:
    l = ligne.replace('\n', "") #on enlève les \n dans chaque string

    if l != "": #si jamais on a une ligne vide, on passe à la ligne suivante
        L.append(l)

i = 0

while i < len(L)-1: #on s'arrête à l'avant-avant-dernier
    ruler = Ruler(L[i], L[i+1]) #on applique la classe Ruler
    ruler.compute()
    top, bottom = ruler.report()
    print(f'''-----------------example #{i//2 + 1} distance = {ruler.distance}
    {top}
    {bottom}''')
    i += 2
