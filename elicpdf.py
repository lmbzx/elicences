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
    def __init__(this,f,scale):
        this.scale=scale
        this.scale=0.27
        this.f=f
        this.cv = canvas.Canvas(f, pagesize=a4T)
        this.lignes=5
        this.cols=2
        this.nbpage=this.lignes*this.cols
        this.lw=a4[0]*this.scale
        this.lh=a4[1]*this.scale
        this.offsety=(a4[1]-this.lignes*this.lw)/2
        this.offsetx=(a4[0]-this.cols*this.lh)/2
        this.org=[0,0]
        this.lab=-1

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
      if entry["type"]!=0:
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
           sz=span["size"]*2*this.scale
           tx=span["text"]
           c.setFillColor(color)
           c.setFont(font, sz)
           c.drawString( this.scale*pos[0]+this.org[0], this.org[1]+this.scale*(a4[1]-pos[3]+sz-9.5*this.scale*1.8), tx)
    def ajouteimage(this,entry):
      if entry["type"]!=1:
        return
      c=this.cv
      pos=entry["bbox"]
      image= PILImage.open(io.BytesIO(entry["image"]),formats=[entry["ext"]])
      c.drawInlineImage(image, this.org[0]+this.scale*pos[0], this.scale*(a4[1]-pos[3])+this.org[1],width=this.scale*(pos[2]-pos[0]),height= this.scale*(pos[3]-pos[1]))

def create_pdf(z,f):
    c=licent(f,.27)
    for b in z:
       c.addpage(b)
    c.save()

def getpage(pdf_file,pblocks):
   pdf_document = fitz.open(pdf_file)
   for page in pdf_document:
    d = page.get_text("dict")
    blocks = d["blocks"]  
    pblocks.append(blocks)

def listelic(out,listefic):
   pblocks=[]
   for d in listefic:
    try:
       getpage(d,pblocks)
    except Exception as e:
       print(e)
       print(d)
   create_pdf(pblocks,out)


def csvlic(out,csvfile):
   donnees = []

   with open(csvfile, mode='r', encoding='ISO-8859-1') as fichier_csv:
     lecteur_csv = csv.DictReader(fichier_csv, delimiter=';')

     for ligne in lecteur_csv:
       donnees.append(dict(ligne))
   ds=[]
   for e in donnees:
     ds.append(f"lic_{e['Nom']}_{e['Prenom']}.pdf")
   listelic(out,ds)

def main():
    parser = argparse.ArgumentParser(description='elicpdf')
    parser.add_argument('--out', required=True, help='Fichier pdf de sortie')
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--liste', nargs='+', help='Liste de fichiers pdf a inclure')
    group.add_argument('--csv', help='Fichier CSV avec au moins les colones "Nom" et "Prenom"')

    args = parser.parse_args()

    if args.liste:
        listelic(args.out, args.liste)
    elif args.csv:
        csvlic(args.out, args.csv)
    else:
        print("Option non reconnue")


if __name__ == '__main__':
    main()



