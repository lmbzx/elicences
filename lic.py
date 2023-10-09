import requests
from bs4 import BeautifulSoup
import sys
import configparser
import json

# laurent.menase.roc14@gmail.com
# a vos risque et périls


class lic:
    def __init__(this,xx,debug):
       this.csrf_token=""
       this.switchurl={
            "infos":this.getinfos,
            "apercu":this.getapercu,
            "login":this.getlogin,
            "licences":this.getlicences,
            "licence":this.getlicences
            }
       this.debug=debug
       config = configparser.ConfigParser()
       config.read('auth.ini')
       this.username=config["auth"]["username"]
       this.password=config["auth"]["password"]
       try:
         with open("cook.json", 'r') as fichier_json:
           this.cook = json.load(fichier_json)
       except FileNotFoundError:
           this.cook = { "XSRF-TOKEN":"eyJpdiI6IkdKZVlXbHVKQ2hMQThkWmtQUis3Umc9PSIsInZhbHVlIjoiN3FlUGVXV1I5aHpDaXBJbU1VazNsTWRRRlN3VktkMjFYYktkZVRzTk9SalI3czJMMmxYQlFpUHl0RitcL1lVTzh2MUlqUjlIYzMwNFBld2xNZDJ2Z3ZVV3l0RU9OYm1Kc1hEYXBva3hrVFwveWRJNjVrQmZlN3pxN3VFTCswWmVVWiIsIm1hYyI6ImNkOGVjYWEwMWUzYzgzYTc0YzljZjBiYWJjMmMyZTcwMTAzZTc4NGFhNTZhMThiNTM4MThkYTMzMGI3MTJmMTMifQ", 
    "laravel_session":"eyJpdiI6Ik9mVW9zdTJVZzcxVGMzQkgwcExnWlE9PSIsInZhbHVlIjoiTmxlQkg0WkhaYkN2bExocStneUpvcjA5UjFlNGl3SjFJaFwvN2hqSXNOZmM5c05ZcGFFTXdYc2ZzdXl3NGtQQ1grOElHdG1vUDZHZUV0ZXhlcHhWbmFMRkhyNmVcLzFQbXN6U2RIVjB1NW1SN1c4VlB6NjBqM09aUGxvUlNUa21jOCIsIm1hYyI6ImY5NWY4NjllMDM1Y2IyMzdhYjVlNmY5MzkzYzg5OGIwYjdlYTY5NjhhNmViNzQ3YjYxODFkZWEwNDc2N2QxN2YifQ" 
            }
       with open("cook.json", 'w') as fichier_json:
          json.dump(this.cook, fichier_json)



    def getinfos(this,r,fn):
        elic=r.url.split("/")[-2]
        if this.debug:
            print(f"infos: {elic}")
        with open(fn,"wb") as f:
            f.write(r.content)
        this.get(r.url.replace("/infos","/apercu"),f"apercu{elic}.txt")
        return False
    def getapercu(this,r,fn):
        elic=r.url.split("/")[-2]
        if this.debug:
           print(f"apercu: {elic}")
        with open(fn,"wb") as f:
            f.write(r.content)
        soup = BeautifulSoup(r.content, 'html.parser')
        h6_element = soup.find('h6', class_='card-title')
        tbody_element = soup.find('tbody')
        dn=""
        if tbody_element:
            tr_elements=tbody_element.find_all('tr')
            if tr_elements:
               for tr in tr_elements:
                   td_elements=tr.find_all('td')
                   if " ".join(td_elements[0].text.split()) == "Date de naissance":
                       dn=td_elements[1].text.split()[0]
            else:
               print("pas de date de naissance 1")
        else:
            print("pas de date de naissance")


        soup = BeautifulSoup(r.content, 'html.parser')
        test_a = lambda tag: tag.name == 'a' and '/structures/fic' in tag.get('href', '') and tag.find('span', class_='text-primary')
        a_es= soup.find(test_a)
        cl=""
        if a_es:
            cl=" ".join(a_es.text.split())
        licence_es = soup.find_all("li")
        datelic=""
        valIA=""
        for lics in licence_es:
            if "avec I.A." in lics.text:
                valIA="avec IA"
            if "sans I.A." in lics.text:
                valIA="sans IA"
            if "Valide du" in lics.text:
                datelic=" ".join(lics.text.split())
                datelic=lics.text.split()[4]
        if h6_element:
            print(";".join([" ".join(h6_element.text.split()),dn,cl,datelic,valIA]))
 
        return False

    def gettoken(this,r):
      soup = BeautifulSoup(r, 'html.parser')
      csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']
      if this.debug:
         print(f"Token CSRF : {csrf_token}")
      this.csrf_token=csrf_token
      return csrf_token
   
    def printheader(this,r):
       print("En-têtes de la réponse:")
       for key, value in r.headers.items():
           print(f"{key}: {value}")

    def setcookie(this,s):
      s1=s.split(";")
      s11=s1[0].split("=")
      this.cook[s11[0] ]=s11[1]
      with open("cook.json", 'w') as fichier_json:
          json.dump(this.cook, fichier_json)

    def getcookie(this,response):
      for key, value in response.raw.headers.items():
        if key == "set-cookie":
           this.setcookie(value)

    def getcookies(this):
       sx=[]
       cook=this.cook
       for key in cook:
         ex=[key,cook[key]]
         sx.append( "=".join(ex ))
       return "; ".join(sx)

    def entete(this,response):
      if not this.debug:
         return
      status_code = response.status_code
      print(  f"Code de statut : {status_code}")
      print("En-têtes de la réponse:")
      for key, value in response.headers.items():
          print(f"{key}: {value}")
      for redirection in response.history:
          print(f"Redirection de {redirection.url} avec code de statut {redirection.status_code}")
      print(f"url final: {response.url}")


    def geturl(this,url,fn):
        headers = {
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
           "Cookie": this.getcookies(),
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        this.getcookie(response)
        this.entete(response)
        return response

    def getlicences(this,response,fn):
        soup = BeautifulSoup(response.text, 'html.parser')
        div_element = soup.find('div', {'data-licence': True})
        if div_element:
           valeur_data_licence = div_element['data-licence']
           print("Valeur de data-licence :", valeur_data_licence)
        else:
           valeur_data_licence=""
           print("Aucun élément <div> avec l'attribut 'data-licence' trouvé.")
           return False
        response=this.geturl( "https://extranet.fsgt.org/licences/attestations/licence-pdf/l/"+valeur_data_licence,fn)
        with open(fn+".pdf","wb") as f:
          f.write(response.content)
        return False

    def get(this,url,fn):
        for retry in range(4):
           response=this.geturl(url,fn)
           endurl=response.url.split("/")[-1]
           if endurl in this.switchurl:
               if this.switchurl[endurl](response,fn):
                  with open(str(retry)+fn,"wb") as f:
                    f.write(response.content)
                  continue
               return False
           return response
        return response

        
    def  cherchepersonne(this,oncherche):
        cherchestr="+".join(oncherche.split())
        url = "https://extranet.fsgt.org/personnes/recherche?personnes_q="+cherchestr
        response=this.get(url,"cherche"+cherchestr)
        if not response:
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        title=soup.find("title")
        first_tbody = soup.find('tbody')
        if first_tbody:
           tr_elements = first_tbody.find_all('tr')
           if tr_elements:
            for tr in tr_elements:
             td_elements = tr.find_all('td')
             if td_elements and len(td_elements)>=5:
              ll=[" ".join(td_elements[0].text.split()),"M" if "Masculin" in " ".join(td_elements[2].text.split()) else "Mme"," ".join(td_elements[1].text.split())," ".join(td_elements[3].text.split())," ".join(td_elements[5].text.split())]
              i=0
              print(" ".join(ll))
             else:
               print(f"pas trouvé {title} {cherchestr}")
           else:
               print(f"pas trouvé-2 {title} {cherchestr}")
        else:
            print(f"pas trouvé-3 {title} {cherchestr}")
            a_element = soup.find('a', href=lambda x: x and "infos" in x and "infos/" not in x )
            if a_element:
              href = a_element['href']
              print(f"href ={href}")
              this.getapercu(href)

   
    def getpersonnelic(this, numelic):
        #print(f"xx: {numelic}")
        numelic0=numelic
        if numelic >422546 :
            numelic=numelic+77453
        if  numelic >    503191:
            numelic=numelic+1
        #print(f"yy: {numelic}")

        response=this.get(f"https://extranet.fsgt.org/personnes/fiche/{numelic}/licences",f"lic{numelic0}")


    def getlogin(this,response,fn):
        url=response.url
        with open(fn+"login1.txt","wb") as f:
          f.write(response.content) 
        this.gettoken(response.content)
        header={
          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
          "Accept-Encoding":"gzip, deflate, br",
          "Accept-Language":"en-US,en;q=0.9,fr;q=0.8",
          "Cache-Control":"max-age=0",
          "Cookie": this.getcookies()
         }
        payload={ 
                 "_token": this.csrf_token, 
                 "username": this.username,
                 "password": this.password
                 }
        response = requests.post(url, json=payload, headers=header)
        this.getcookie(response)
        with open(fn+"login2.txt","wb") as f:
            f.write(response.content)
        return True


def licmain():
   malic=lic( "",False)
#malic.getlogin()
#malic.getpersonnelic(numelic)
   malic.cherchepersonne(sys.argv[1])

#malic.cherchepersonne("menase")
        
#malic.getpersonnelic(187855)

if __name__ == "__main__":
    licmain()



