from lic import lic
import sys
import csv
# laurent.menase.roc14@gmail.com
# a vos risque et périls

donnees = []

with open(sys.argv[1], mode='r', encoding='ISO-8859-1') as fichier_csv:
    lecteur_csv = csv.DictReader(fichier_csv, delimiter=';')

    for ligne in lecteur_csv:
        donnees.append(dict(ligne))

malic=lic( "",False)
for e in donnees:
   print(f"{e['numelic']};{e['Genre']};{e['Nom']};{e['Prenom']};{e['dn']}")
   malic.cherchepersonne(e["numelic"])



