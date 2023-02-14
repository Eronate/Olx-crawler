from bs4 import BeautifulSoup
import requests
import re

anvelope_count=[0 for i in range(3)]
jante_count=[0 for i in range(6)]
caroserie_count=[0 for i in range(6)]
piese_interior_count= [0 for i in range(5)]
electronice_count=[0 for i in range(4)]
marca_masina_count=[0 for i in range(4)]
stare_piesa_count=[0 for i in range(1)]
frane_count=[0 for i in range(5)]
piese_motor=[0 for i in range(4)]

regex_anvelope=[r"215[ .,\/-]*?65[ .,/\/-]*?[Rr]?[ .,\/-]*17",r"235[ .,\/-]*?55[ .,/\/-]*?[Rr]?[ .,\/-]*19",r"245[ .,\/-]*?45[ .,/\/-]*?[Rr]?[ .,\/-]*17"]
regex_jante=  [r"[Rr][ .\/,-]*?16",r"[Rr][ .\/,-]*?17",r"[Rr][ .\/,-]*?18",r"[Rr][ .\/,-]*?19",r"[Rr][ .\/,-]*?20",r"[Rr][ .\/,-]*?21"]
regex_caroserie= [r"(far(uri)?)",r"(arip([aă]*)?i?e?)",r"(b[aă]*r[aăi]*)[ ,.\/-]*?(spate)",r"(b[aă]*r[aăi]*)[ ,.\/-]*?(fa[țt]*[aă]*)",r"(ha[iye]*on)",r"(oglin((zi)|(d[aă]*)))]"]
regex_piese_interior= [r"(nav[iy]*ga[tț]*[iy]*e)",r"(nuc[aă]*)[ .,\/-]*(de)?[ .,\/-]*(schimb[aă]*tor)[ .,\/-]*(de)?[ .,\/-]*(vitez[eaă])",r"([ ,.\/-]hus[aăe][ .,\/-])",r"([ ,.\/-]volan[ .,\/-])",r"[ ,.\/-](box[aă])[ ,.\/-]]"]
regex_electronice =[r"(senzori?)[ ]*(parcare)",r"((calculator)|(computer))[ ]*(de)?[ ]*(bord)",r"(camer[aă])[ ]*(video)?((spate)|(auto)|(360)|(marsalier)|(masalier)|(marsarier))",r"(ceas(uri)?)[ ]*(de)?[ ]*(bord)"]
regex_marca_masina=[r"(bmw) | (bemve) | (bmve) | (bmv)",r"(vw) | (volkswagen) | (volsvagen) | (vozagan) | (volskvagen) | (volskwagen) | (volksvagen)",r"(audi) | (audy)",r"(mercedes)[ ,. \ /-]*(benz)"]
regex_stare_piesa=[r"(nou[aă]?)"]
regex_frane=[r"(\b)((discuri) | (disc))(.*)",r"(fr[âa]n[aăe])(\b)",r"(\b)(etrier[ie]?)(\b)",r"(\b)(pomp[aă])(.*)fr[âa]n[aăe](\b)",r"(\b)((butuc[i]?)(.*)fr[âa]n[aăe])(\b)",r"(\b)placu[tț][aeă][ ]*(de)?[ ]*fr[âa]n[aăe](\b)"]
regex_piese_motor=[r"[,.]?([Tt]urbin[aă])[.,]?",r"(\b)[iI]njector(\b) | (\b)[Ii]njectoare(\b)",r"(\b)[,.]?[vV]olant[aă][., /]?(\b)",r"(\b)[Aa]mbreiaj[e]?(\b) | (\b)[Aa]mbreaj[e]?(\b)"]
regexAll = [regex_anvelope, regex_jante, regex_caroserie, regex_piese_interior, regex_electronice, regex_marca_masina,
            regex_stare_piesa, regex_frane, regex_piese_motor]

occurencesfinal = [[0 for i in range(10)]for j in range(9)]

def calcOccurences(link):
    r2 = requests.get(link)
    html_deep = BeautifulSoup(r2.text, features="html.parser")
    descriere = ""
    title = ""
    if link.find("/anunt/")!=-1:
        descriere = html_deep.find('div', {'class': "offer-description__description"}).text
        title = html_deep.find('span', {'class': 'offer-title big-text fake-title is-parts'}).text

    elif link.find("/d/")!=-1:
        titluri = html_deep.findAll("h1")
        title = titluri[0].text
        descriere = html_deep.find('div', {'class': "css-bgzo2k er34gjf0"}).text

    for i in range(0,len(regexAll)):
        regexList = regexAll[i]
        for j in range (0,len(regexAll[i])):
            regexListItem = regexList[j]
            if(re.search(regexListItem, title)!=None): #or re.search(regexListItem, descriere)!=None):
                #print(title, "|||Match found on:|||", regexListItem)
                occurencesfinal[i][j] += 1

def startCrawler(page):
    try:
        link = "https://www.olx.ro/d/piese-auto" + "/?page=" + str(page)
        linkuri = []
        r = requests.get(link)
        html_pagina = BeautifulSoup(r.text, features="html.parser")
        #gridContainer = html_pagina.find('div', {'class': "listing-grid-container"})
        anunturi = html_pagina.findAll('a')
        k=0
        for anunt in anunturi:
            anuntCurent = anunt.get("href")
            if anuntCurent:
                if anuntCurent.find("/anunt/")!=-1:
                   linkuri.append(anuntCurent)
                elif anuntCurent.find("/oferta/")!=-1:
                    linkuri.append("https://olx.ro" + anuntCurent)
        for link in linkuri:
            calcOccurences(link)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print("Crawling...")
    for i in range(1,25):
        startCrawler(i)
    print("____________________________________________________")
    print("____________________________________________________")
    print("____________________________________________________")

    print("Anvelope 215 65 17, 235 55 19, respectiv 245 45 17:", occurencesfinal[0][1],occurencesfinal[0][1], occurencesfinal[0][2])
    print("Jante R16, R17, R18, R19, R20, respectiv R21: ", occurencesfinal[1][0], occurencesfinal[1][1],
          occurencesfinal[1][2], occurencesfinal[1][3], occurencesfinal[1][4])
    print("Faruri, Aripi, Bari spate, Bari fata, Haion, respectiv Oglinzi", occurencesfinal[2][0], occurencesfinal[2][1],
          occurencesfinal[2][2], occurencesfinal[2][3], occurencesfinal[2][4], occurencesfinal[2][5])
    print("Navigatie, Nuca de schimbator de viteza, Husa, Volan, Boxa", occurencesfinal[3][0], occurencesfinal[3][1],
          occurencesfinal[3][2], occurencesfinal[3][3], occurencesfinal[3][4])
    print("Senzori de parcare,  Calculator de bord, Camera video spate, Ceasuri de bord", occurencesfinal[4][0], occurencesfinal[4][1],
          occurencesfinal[4][2], occurencesfinal[4][3])
    print("BMW,  VW, Audi, Mercedes Benz", occurencesfinal[5][0],
          occurencesfinal[5][1], occurencesfinal[5][2], occurencesfinal[5][3])
    print("Noua", occurencesfinal[6][0])
    print("Discuri, Frana, Etrieri, Pompa frana, Butuci frana, Placuta de frana", occurencesfinal[6][0],
          occurencesfinal[6][1], occurencesfinal[6][2], occurencesfinal[6][3], occurencesfinal[6][4], occurencesfinal[6][5])
    print("Turbina, Injector, Volanta, Ambreiaj", occurencesfinal[7][0],
          occurencesfinal[7][1], occurencesfinal[7][2], occurencesfinal[7][3])



