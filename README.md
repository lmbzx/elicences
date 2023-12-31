# elicences

## version executable windows
- des versions executables ( non testes sont disponibles dans le repertoire dist, pour les executer, remplacer "python3 macommand.py" par "macommande"
### liste des fichiers
- [reduitelic2](https://github.com/lmbzx/elicences/raw/main/dist/reduitelic2.exe)
- [reduitelic](https://github.com/lmbzx/elicences/raw/main/dist/reduitelic.exe)
- [elicpdf](https://github.com/lmbzx/elicences/raw/main/dist/elicpdf.exe)
- [pdflic](https://github.com/lmbzx/elicences/raw/main/dist/pdflic.exe)
- [lic](https://github.com/lmbzx/elicences/raw/main/dist/lic.exe)
- [getlic](https://github.com/lmbzx/elicences/raw/main/dist/getlic.exe)
- [checklic](https://github.com/lmbzx/elicences/raw/main/dist/checklic.exe)
- [cherchestatus](https://github.com/lmbzx/elicences/raw/main/dist/cherchestatus.exe)

## version avec python
### dependances:
```
  # pip3 install beautifulsoup4
  # pip3 install pyPDF4
  # pip3 install reportlab
  # pip3 install pillow
  # pip3 install PyMuPDF
  # pip3 install tkinter
```
## les script pour generer un pdf
- n'utilise pas auth.ini
### reduitelic.py/reduitelic.exe avec interface plus facile
- reduitelic2 est une version plus complete pouvant prendre en entree un fichier csv 
```
     "numelic;Genre;Nom;Prenom;dn;clubnum;club"
```
- pour executer reduitelic:  ( pareil pour reduitelic2)
```
# python3 reduitelic.py
ou
 click sur reduitelic.exe
`
```
### elicpdf.py
- 2 modes, csv ou liste
#### mode csv:
- le fichier csv a au moins les colones Nom et Prenom, et les fichiers licence pdf s'appellent lic_{nom}_{prenom}.pdf
```
  # python3 ./elicpdf.py csv [--massicot] fichiersortie.pdf tx.csv  
  ou
  # elicpdf.exe csv [--massicot] fichiersortie.pdf tx.csv

l'option --massicot imprime en colonne pour un massicotage facile
```
#### mode liste:
- les fichiers pdf sont dans le repertoire d'execution
```
  # python3 ./elicpdf.py liste resultat.pdf licence1.pdf licence2.pdf licence3.pdf ... licencen.pdf 
  ou
  # elicpdf.exe liste resultat.pdf licence1.pdf licence2.pdf licence3.pdf ... licencen.pdf 
```
### pdflic.py
- toujours le meme format de fichier csv, apres le getlic.py
qui nomme tous les fichiers de licence lic_nom_prenom.pdf
- dans le repertoir ou sont les fichiers lic_nom_prenom.pdf
```
  # python3 ./pdflic.py tx.csv  resultat.pdf
```
ca génére des planches de 10 etiquetes a 27%, en mettant une chaine de characteres plus grande et donc lisible a 27%

## verification et collect des licences
### configuration:
- remplacer le compte et mot de passe dans auth.ini
### les fichiers:
- lic.py
    - C'est la librarie principale
    - on peut l'utilise pour rechercher 1 personne par son nom prenom ou id elicence
    - ca ressort toutes les homonymes avec leur les potentiels doublons
```
  # python3 lic.py  "lau men"
```
- checklic.py  
     - Prend un CSV en entrée (ISO, pas utf8) 
```
     "numelic;Genre;Nom;Prenom;dn;clubnum;club"
```

     - cherche chaque Prenom Nom, et affiche tous les resultats possibles, avec le club dans lequel la licence est prise
     - exemple:
```
# cat t.csv
numelic;Genre;Nom;Prenom;dn;clubnum;club
1;M;Menase;laur;24/01/1988;ziv
225066;M;abzki;Arthur;30/06/1991;
1;M;ZZZZ;YYYY;29/05/1991;

# python3 ./checklic.py t.csv
1;M;Menase;laurent;21/02/1988;ziv
0187816 M MENASE Laurent 21/02/1988 04991 ROC 14
0424654 M TEST Laire 24/01/2001
0424243 M TOTO Toto 21/01/2017
225066;M;abzki;Arthur;30/06/1991;
0225062 M ABZKI Arthur 30/06/1991
0225063 M ABZKI Arthur 30/06/1991
0225066 M ABZKI Arthur 30/06/1991 04991 ROC 14
1;M;ZZZZ;YYYY;29/05/1991;
0290534 Mme ZZZZ YYYY;09/10/1970;05112 CIMES 19;31/08/2024;avec IA
```
- cherchestatus.py  
   - recherche le status de chaque licence d'apres le numero elicence
```
# cat tx.csv
numelic;Genre;Nom;Prenom;dn;clubnum;club
0187816;M;Menase;laur;24/01/1988;ziv
225066;M;abzki;Arthur;30/06/1991;
0290534;M;ZZZZ;YYYY;29/05/1991;

# python3 ./cherchestatus.py tx.csv
0187816;M;MENASE;laur;24/01/1988
0187816 M MENASE Laurent;24/01/1988;04991 ROC 14;31/08/2024;avec IA
225066;M;abzki;Arthur;30/06/1991;
0225066 M ABZKI Arthur;30/06/1991;04991 ROC 14;31/08/2024;avec IA
0290534;M;ZZZZ;YYYY;29/05/1991;
0290534 Mme ZZZZ YYYY;29/05/1970;05112 CIMES 19;31/08/2024;avec IA
```
- getlic.py  
    - recupere tous les pdf de licence d'une liste de numelic
    - si c'est un membre d'un autre club, le fichier licence n'est pas recupéré et un message d'erreur est affiché
```
# python3 getlic.py ./tx.csv
python3 ./getlic.py  ./tx.csv
0187816;M;MENASE;laurent;24/01/1988
Valeur de data-licence : 386311
Fichier déplacé avec succès vers : lic_MENASE_laurent.pdf
0225066;M;ABZKI;Arthur;30/06/1991
Valeur de data-licence : 403375
Fichier déplacé avec succès vers : lic_ABZKI_Arthur.pdf
0290534;Mme;ZZZZ;YYYY;29/05/1970;
0290534 Mme ZZZZ YYYY;29/05/1970;05112 CIMES 19;31/08/2024;avec IA
Erreur lors du déplacement du fichier : [Errno 2] No such file or directory: 'lic190534.pdf'
```


 

