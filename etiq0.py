import PyPDF4
import sys
import csv
facteur_echelle=float(0.27)
largeur_page_a4 = 1190/2 
hauteur_page_a4 = 841   
lp=largeur_page_a4*facteur_echelle
hp=hauteur_page_a4*facteur_echelle
nbh=int(largeur_page_a4/hp)
nbl=int(hauteur_page_a4/lp)
print(f"{nbh} {nbl}")
l_interval=(largeur_page_a4-nbh*hp)/(nbh+1)
h_marge=(hauteur_page_a4-nbl*lp)/2
class mondoc():
    def __init__(this):
        this.position=0
        this.pdf_final = PyPDF4.PdfFileWriter()


    def posit(this):
      ajoutepage=False
      if this.position%(nbh*nbl)==0:
        ajoutepage=True
      r=this.position%(nbh*nbl)
      c=int(r%nbh)
      l=int(r/nbh)%nbl
      c=l_interval+(l_interval+ hp)*c
      l=h_marge+l*lp
      #l=l*lp
      print(f"{c} {l}")
      this.position=1+this.position
      if ajoutepage: 
          page_a4 = PyPDF4.pdf.PageObject.createBlankPage(height=largeur_page_a4, width=hauteur_page_a4)
          this.pdf_final.addPage(page_a4)
      return c,l
    def ajoutepdf(this,fichier):
       pdf = PyPDF4.PdfFileReader(open(fichier, "rb"))
       premiere_page=pdf.getPage(0)
       premiere_page.scaleBy(facteur_echelle)
       #premiere_page.rotateClockwise(90)
       c,l=this.posit()
       page_a4=this.pdf_final.getPage(this.pdf_final.getNumPages()-1)
       page_a4.mergeTranslatedPage(pdf.getPage(0), l, c)  

    def sortle(this,fichier):
        with open(fichier, "wb") as fichier_final:
           this.pdf_final.write(fichier_final)
donnees = []

with open(sys.argv[1], mode='r', encoding='ISO-8859-1') as fichier_csv:
    lecteur_csv = csv.DictReader(fichier_csv, delimiter=';')

    for ligne in lecteur_csv:
        donnees.append(dict(ligne))

mdoc=mondoc()
for e in donnees:
  try:
   mdoc.ajoutepdf(f"lic_{e['Nom']}_{e['Prenom']}.pdf")
   print(f"{e['numelic']};{e['Genre']};{e['Nom']};{e['Prenom']};{e['dn']}")
  except:
      print(f"lic_{e['Nom']}_{e['Prenom']}.pdf non trouvé")
mdoc.sortle(sys.argv[2])




