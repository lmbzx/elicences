from lic import lic
import sys
import csv
import shutil

donnees = []

with open(sys.argv[1], mode='r', encoding='ISO-8859-1') as fichier_csv:
    lecteur_csv = csv.DictReader(fichier_csv, delimiter=';')

    for ligne in lecteur_csv:
        donnees.append(dict(ligne))

malic=lic( "",False)
for e in donnees:
   print(f"{e['numelic']};{e['Genre']};{e['Nom']};{e['Prenom']};{e['dn']}")
   malic.getpersonnelic(int(e["numelic"]))

   s=f"lic{int(e['numelic'])}.pdf"
   d=f"lic_{e['Nom']}_{e['Prenom']}.pdf"

   try:
    shutil.move(s, d)
    print(f"Fichier déplacé avec succès vers : {d}")
   except Exception as e:
    print(f"Erreur lors du déplacement du fichier : {e}")


