import argparse
import csv 
import fitz 
#import sys
#import pprint
from PIL import Image as PILImage

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os
import io
a4=(595.2760009765625,841.8900146484375)
a4T=(a4[1],a4[0])
def coulacoul(val):
      b=float(int(val)%256)/255.0
      val=val/256
      v=float(int(val)%256)/255.0
      val=val/256
      r=float(int(val)%256)/255.0
      return colors.Color(r,v,b,1)

class licent():
    def __init__(this,f,echelle=0.27,taillef=2,massicot=False):
        this.scale=echelle
        this.f=f
        this.massicot=massicot
        x=int(1/echelle)
        y0=int(210/297/echelle)
        y1=int(297/210/echelle)
        if(y0*y1<x*x):
            this.lignes=x
            this.cols=x
            this.pg=(a4[1],a4[0])
            this.cv = canvas.Canvas(f, pagesize=a4)
        else:
            this.lignes=y1
            this.cols=y0
            this.pg=(a4[0],a4[1])
            this.cv = canvas.Canvas(f, pagesize=a4T)
        this.nbpage=this.lignes*this.cols
        this.lw=a4[0]*this.scale
        this.lh=a4[1]*this.scale
        this.offsety=(this.pg[1]-this.lignes*this.lw)/2
        this.offsetx=(this.pg[0]-this.cols*this.lh)/2
        this.org=[0,0]
        this.lab=-1
        this.taillef=taillef

    def addpage(this,b):
      this.lab=this.lab+1
      l=this.lab%this.nbpage
      #print(l)
      if this.lab>0 and l%this.nbpage==0:
          print("nouvelle page")
          this.cv.showPage()
      li=l%this.cols
      #0 if(l<this.lignes) else 1
      #print(li)
      col=int(l/this.cols)%this.lignes
      #print(col)
      this.org=[this.offsety+col*this.lw,this.offsetx+li*this.lh]
      for i in b: 
        this.ajoutetext(i)
        this.ajouteimage(i)

    def save(this):
        this.cv.save()



    def  ajoutetext(this,entry):
      if 'type' not in entry or entry["type"]!=0:
        return
      c=this.cv
      lines=entry['lines']  
      for line in lines:
        spans=line["spans"]
        for span in spans:
           if span["size"]==20 and span["color"] == 255:
               continue
           pos=span["bbox"]  
           color=coulacoul(span["color"]  )
           font=span["font"]
           org=span["origin"]
           sz=span["size"]*this.taillef*this.scale
           tx=span["text"]
           c.setFillColor(color)
           c.setFont(font, sz)
           c.drawString( this.scale*pos[0]+this.org[0], this.org[1]+this.scale*(this.pg[1]-pos[3]+sz-9.5*this.scale*1.8), tx)
    def ajouteimage(this,entry):
      if 'type' not in entry or entry["type"]!=1:
        return
      c=this.cv
      pos=entry["bbox"]
      image= PILImage.open(io.BytesIO(entry["image"]),formats=[entry["ext"]])
      c.drawInlineImage(image, this.org[0]+this.scale*pos[0], this.scale*(this.pg[1]-pos[3])+this.org[1],width=this.scale*(pos[2]-pos[0]),height= this.scale*(pos[3]-pos[1]))

    def nbpages(this):
        return this.nbpage

def create_pdf(z,f,massicot=False,taillef=2,echelle=0.27):
    c=licent(f,echelle=echelle,massicot=massicot,taillef=taillef)
    if massicot:
        pos=0
        pos0=0
        nbpage=c.nbpage
        nbpg=int((len(z)+nbpage-1)/nbpage)
        bz=[]
        for i in range(0,nbpg):
         for j in range(0,10):
          if pos <len(z):
            #print(f"x {pos}")
            bz.append(z[pos])
          else: 
            #print(f"y {pos}")
            bz.append({})
          pos+=nbpg
          if pos > nbpg*nbpage-1:
              pos0+=1
              pos=pos0

    else:
        bz=z
    for b in bz:
       c.addpage(b)
    c.save()

def getpage(pdf_file,pblocks):
   pdf_document = fitz.open(pdf_file)
   for page in pdf_document:
    d = page.get_text("dict")
    blocks = d["blocks"]  
    pblocks.append(blocks)

def listelic(out,listefic,massicot=False,taillef=2):
   pblocks=[]
   for d in listefic:
    try:
       getpage(d,pblocks)
    except Exception as e:
       print(e)
       print(d)
   create_pdf(pblocks,out,massicot=massicot,taillef=taillef)
   print(f"done {len(d)}")


def csvlic(out,csvfile,workdir="",massicot=False):
   donnees = []

   print(workdir)
   with open(csvfile, mode='r', encoding='ISO-8859-1') as fichier_csv:
     lecteur_csv = csv.DictReader(fichier_csv, delimiter=';')

     for ligne in lecteur_csv:
       donnees.append(dict(ligne))
   ds=[]
   for e in donnees:
       ds.append(os.path.join(workdir,f"lic_{e['Nom']}_{e['Prenom']}.pdf"))
   listelic(out,ds,massicot=massicot)

def main():
   parser = argparse.ArgumentParser(description="Script Python avec deux sous-commandes.")
   subparsers = parser.add_subparsers(dest="subcommand")
   liste_parser = subparsers.add_parser("liste", help="Mode liste")
   liste_parser.add_argument("out", help="Nom du fichier de sortie")
   liste_parser.add_argument("licencespdf", nargs="+", help="Liste des fichiers a traiter")
   csv_parser = subparsers.add_parser("csv", help="Mode csv")
   csv_parser.add_argument("out", help="Nom du fichier de sortie")
   csv_parser.add_argument("fichiercsv", help="Nom du fichier CSV de donnees")
   csv_parser.add_argument("--massicot", action="store_true", help="Activer le massicot")
   args = parser.parse_args()

   if args.subcommand == "liste":
        print("Mode liste selectionne.")
        print("Fichier de sortie :", args.out)
        print("Fichiers a traiter :", args.licencespdf)
        listelic(args.out, args.licencespdf)
   elif args.subcommand == "csv":
        print("Mode csv selectionne.")
        print("Fichier de sortie :", args.out)
        print("Fichier CSV de donnees :", args.fichiercsv)
        if args.massicot:
          print("Option -massicot activée.")
        csvlic(args.out, args.fichiercsv,args.massicot)
   else:
    parser.print_help()

    print(args)
    exit

   '''
   if args.liste:
        listelic(args.out, args.liste)
   elif args.csv:
        csvlic(args.out, args.csv)
   else:
        print("Option non reconnue")
   '''


if __name__ == '__main__':
    main()



