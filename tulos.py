'''
TEKIJÄ: OTTO LOUKKOLA

IDEA: Harjoittelun vuoksi tehty ohjelma,
jolla voi analysoida yo-koe tuloksia graafisen käyttöliittymän avulla.
Kehittely on kesken.
'''
import tkinter as tk
from tkinter.ttk import Separator
from tkinter import messagebox, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")

import numpy as np
import matplotlib.pyplot as plt

sanakirja = {
    "muistinumero":0
}

elementit = {
    "graafi": None,
    "piirto": None,
    "alue": None
}


def tutkinnon_ka(x):
    eri_lista = [0]
    keskiarvo_miehet = [0]
    keskiarvo_naiset = [0]
    with open(x) as lahde:
        for rivi in lahde.readlines():
            sisus = rivi.rstrip("\n")           
            lista = sisus.split(";")
            keskiarvo = 0
            pisteet = 0
            lkm = 0 
            for i in range(7, len(lista) - 1):
                try:
                    numero = int(lista[i])
                    if numero < 8:
                        pisteet = pisteet + numero
                        lkm = lkm + 1
                except ValueError:
                    pass
                else:
                    pass
            if lkm != 0:
                keskiarvo = pisteet / lkm
                eri_lista.append(keskiarvo)
                if int(lista[5]) == 1:
                    keskiarvo_miehet.append(keskiarvo)
                elif int(lista[5]) == 2:
                    keskiarvo_naiset.append(keskiarvo)
    return eri_lista, keskiarvo_miehet, keskiarvo_naiset
    #piirto(sorted(eri_lista), sanakirja["muistinumero"])

def nayta_tulokset(x):
    #FT2019KD4001.csv
    hyvaksytty = 0
    lkm = 0
    kaikki_pisteet = 0
    keskiarvo = 0
    tulos_lista = [0]
    
    pisteytys_m = [0]*8
    pisteytys_m[2] = 6.6
    pisteytys_m[3] = 13.2
    pisteytys_m[4] = 19.8
    pisteytys_m[5] = 26.4
    pisteytys_m[6] = 33.1
    pisteytys_m[7] = 39.7
    
    pisteytys_a = [0]*8
    pisteytys_a[2] = 5.5
    pisteytys_a[3] = 11
    pisteytys_a[4] = 16.5
    pisteytys_a[5] = 22
    pisteytys_a[6] = 27.5
    pisteytys_a[7] = 33
    
    pisteytys_f = [0]*8
    pisteytys_f[2] = 5.4
    pisteytys_f[3] = 10.8
    pisteytys_f[4] = 16.2
    pisteytys_f[5] = 21.5
    pisteytys_f[6] = 26.9
    pisteytys_f[7] = 32.3
    with open(x) as lahde:
        for rivi in lahde.readlines():
            sisus = rivi.rstrip("\n")
           
            lista = sisus.split(";")
            lkm = lkm + 1
            pisteet = 0
            fy = 0
            ke = 0
            for i in range(8):
                if lista[15] != "" and lista[15] != "M":
                    if int(lista[15]) == i:
                        pisteet = pisteet + pisteytys_m[i]
                if lista[7] != "" and lista[7] != "A":
                    if int(lista[7]) == i:
                        pisteet = pisteet + pisteytys_a[i]
                if lista[19] != "" and lista[19] != "FY":
                    if int(lista[19]) == i:
                        fy = pisteytys_f[i]
                if lista[26] != "" and lista[26] != "KE":
                    if int(lista[26]) == i:
                        ke = pisteytys_f[i]
            if fy > ke:
                pisteet = pisteet + fy
            else:
                pisteet = pisteet + ke
                        
            if lista[15] == "4" or lista[15] == "5" or lista[15] == "6" or lista[15] == "7" or lista[19] == "4" or lista[19] == "5"  or lista[19] == "6" or lista[19] == "7" or lista[26] == "4"or lista[26] == "5"or lista[26] == "6"or lista[26] == "7":
                if pisteet >= 36.3:
                    hyvaksytty = hyvaksytty + 1
            kaikki_pisteet = kaikki_pisteet + pisteet
            tulos_lista.append(pisteet)
    #lasku(kaikki_pisteet, lkm, tulos_lista, hyvaksytty)
    jorma = skaalaus(sorted(tulos_lista))
    #piirto(jorma)
    piirto(sorted(tulos_lista), sanakirja["muistinumero"])

def skaalaus(lista):
    uusi_lista = [0]
    for i in range(len(lista)):
        if i % 1000 == 0:
            uusi_lista.append(lista[i])
    return uusi_lista
            
def desiilit(lista_m, lista_n):
    lista_m_j = [0]
    lista_n_j = [0]
    lista_m_j = sorted(lista_m)
    lista_n_j = sorted(lista_n)
    desiili_m = [0]*9
    desiili_n = [0]*9
    labels = []
    for i in range(9):
        labels.append("{} / 10".format(i+1))
    for i in range(9):
        desiili_m[i] = lista_m_j[int((i+1)/10 * len(lista_m))]
        desiili_n[i] = lista_n_j[int((i+1)/10 * len(lista_n))]
    return desiili_m, desiili_n, labels
    
def piirakka(lista1, lista2, lista):
    elementit["piirto"].clear()
    x = np.arange(len(lista))

    #fig, ax = elementit["graafi"].subplots()
    fig, ax = plt.subplots()
    
    print("lista1: {}, lista2: {}, lista: {}".format(len(lista1), len(lista2), len(lista)))
    
    rects1 = ax.bar(x - 0.35/2, lista1, 0.35, label='Miehet')
    rects2 = ax.bar(x + 0.35/2, lista2, 0.35, label='Naiset')
    ax.set_xticks(x)
    ax.set_xticklabels(lista)
    ax.legend()
    '''
    for rect in rects1:
        korkeus = rect.get_height()
        ax.annotate('{}'.format(korkeus),
                    xy=(rect.get_x() +rect.get_width() / 2, korkeus),
                    textcoords="offset points",
                    ha='center', va='bottom')
    for rect in rects2:
        korkeus = rect.get_height()
        ax.annotate('{}'.format(korkeus),
                    xy=(rect.get_x() +rect.get_width() / 2, korkeus),
                    textcoords="offset points",
                    ha='center', va='bottom')
    '''
    
    fig.tight_layout()
    plt.show()
    #elementit["graafi"] = elementit["piirto"].subplots()
    
    #elementit["alue"].draw() 

def lasku(kaikki_pisteet, lkm, tulos_lista, hyvaksytty):
    keskiarvo = kaikki_pisteet / lkm
    tulos_lista_j = sorted(tulos_lista)
    mediaani = tulos_lista_j[int(lkm * 0.5)]
    maksimi = max(tulos_lista)
    kolme_nelja = tulos_lista_j[int(lkm * 3/4)]
    ysi = tulos_lista_j[int(lkm * 0.9)]
    for k in range(len((tulos_lista_j))):
        if tulos_lista_j[k] >= 36.1:
            print(k)
            print(tulos_lista_j[k])
            break
    '''
    print(hyvaksytty)   
    print("Keskiarvo on {:0.2f}".format(keskiarvo))
    print("Mediaani on {:0.2f}".format(mediaani))
    print("75% on {:0.2f}".format(kolme_nelja))
    print("90% on {:0.2f}".format(ysi))
    print(maksimi)
    '''

                   
                
def ikkuna():
    global ikkuna
    ikkuna = tk.Tk()
    ikkuna.wm_title("Ikkuna")
    return ikkuna

def nappi(x, y , z):
    nappi = tk.Button(x, text=y, command=z)
    nappi.pack(side=tk.TOP, fill=tk.BOTH)
    return nappi
    
def kasittelija(x):
    print("1")
    
def kehys(k, puoli=tk.LEFT):
    kehys = tk.Frame(k)
    kehys.pack(side=puoli, anchor="n")
    return kehys

def nuuskija():
    print("penis")
    sanakirja["muistinumero"] = 0
    nayta_tulokset("FT2019KD4001.csv")
    
def nuuskija1():
    sanakirja["muistinumero"] = 1
    nayta_tulokset("FT2020KD4001.csv")

def nuuskija2():
    sanakirja["muistinumero"] = 2
    ka_kaikki , ka_miehet, ka_naiset = tutkinnon_ka("FT2019KD4001.csv")
    piirto(sorted(ka_kaikki), sanakirja["muistinumero"])
    
def nuuskija3():
    sanakirja["muistinumero"] = 2
    ka_kaikki , ka_miehet, ka_naiset = tutkinnon_ka("FT2019KD4001.csv")
    piirto(sorted(ka_miehet), sanakirja["muistinumero"])
    
def nuuskija4():
    sanakirja["muistinumero"] = 4
    ka_kaikki , ka_miehet, ka_naiset = tutkinnon_ka("FT2019KD4001.csv")
    piirto(sorted(ka_naiset), sanakirja["muistinumero"])
    
def nuuskija5():
    a, b, c = tutkinnon_ka("FT2019KD4001.csv")
    d, e, f = desiilit(b, c)
    piirakka(d, e, f)

def lopeta():
    ikkuna.destroy()

def kuvaaja(k, kasittelija, leveys, korkeus):
    kuvaaja = Figure(figsize=(leveys / 100, korkeus / 100), dpi=100)
    piirtoalue = FigureCanvasTkAgg(kuvaaja, master=k)
    piirtoalue.get_tk_widget().pack(side=tk.TOP)
    piirtoalue.mpl_connect("button_press_event", kasittelija)
    alikuvaaja = kuvaaja.add_subplot()
    return piirtoalue, kuvaaja, alikuvaaja
    
def piirto(lista, x):
    elementit["piirto"].clear()
    d = np.array(lista)
    
    elementit["graafi"] = elementit["piirto"].stem(d)
    elementit["alue"].draw()
    #plt.show()
    
def main():
    testi = ikkuna()
    ikkuna.state("zoomed")
    ylakehys = kehys(testi, tk.LEFT)
    alakehys = kehys(testi, tk.LEFT)
    nappikehys = kehys(ylakehys, tk.LEFT)
    syotekehys = kehys(ylakehys, tk.LEFT)
    nappi1 = nappi(nappikehys, "DIA-pisteet 2019", nuuskija)
    nappi2 = nappi(nappikehys, "DIA-pisteet 2020", nuuskija1)
    nappi3 = nappi(nappikehys, "2019 keskiarvo kaikki", nuuskija2)
    nappi4 = nappi(nappikehys, "2019 keskiarvo miehet", nuuskija3)
    nappi5 = nappi(nappikehys, "2019 keskiarvo naiset", nuuskija4)
    nappi6 = nappi(nappikehys, "2019 desiili", nuuskija5)
    lopetusnappi = nappi(nappikehys, "lopeta", lopeta)
    elementit["alue"], elementit["kuvaaja"], perse = kuvaaja(alakehys, kasittelija, 600, 600)
    elementit["piirto"] = elementit["kuvaaja"].add_subplot(1, 1, 1)
    #nayta_tulokset("FT2019KD4001.csv")
    ikkuna.mainloop()
       
main()
