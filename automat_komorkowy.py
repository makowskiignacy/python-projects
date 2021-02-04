# !/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random as random
import sys as sys
import os as os

#0 - zdrowy
#1 - zarażony
#2 - ozdrowieniec

def zainicjalizuj_populacje(N, k):
    #zwraca tablicę zer z k-jedynek na losowych pozycjach
    populacja = np.zeros((N, N))
    i = 0
    while i < k:
        x = random.randint(0, N - 1)
        y = random.randint(0, N - 1)
        if populacja[x][y] == 0:
            populacja[x][y] = 1
            i += 1
            pass
        pass
    return populacja

def poprawne_wspolrzedne(x, y, N):
    #Sprawdza czy współrzędne znajdują się w tablicy
    if ((0 <= x) and (x < N) and (0 <= y) and (y < N)):
        return True
    else:
        return False
    pass

def kontakt(x, y, r, N, populacja):
    #Zwraca liczę zarażonych w odległości r
    zarazeni = 0
    for i in range(x - r, x + r + 1):
        for j in range(y - r, y + r + 1):
            if (poprawne_wspolrzedne(i, j, N) and (i != x or j != y)):
                if populacja[i][j] == 1:
                    zarazeni += 1
                    pass
                pass
            pass
        pass
    return zarazeni

def obrazuj_pandemie(m, lista_oz, lista_zd, lista_zz):
    #tworzy wykres ilości zarażonych, zdrowych i wyzdrowiałych od obrotów pętli
    x = range(m + 1)
    plt.plot(x, lista_zd, "b", label="zdrowi")
    plt.plot(x, lista_zz, "r", label="zarażeni")
    plt.plot(x, lista_oz, "g", label="ozdrowieńcy")
    plt.title("wykres")
    plt.legend()
    pass

def symulacja_pandemii(M, N, k, p_w, p_z, r):
    #M - maksymalnailość ilość rozpatrywanych dni
    #N - sqrt(ilosci wszystkich jednostek)
    #p_w - szansa na wyzdrowienie
    #p_z - szansa na zachorowanie
    #r - odległość Moore'a
    populacja = zainicjalizuj_populacje(N, k)
    populacja_nast = np.zeros((N, N))
    #listy ilości osób w poszczególnych stanach
    lista_oz = []
    lista_zz = []
    lista_zd = []
    #lista obrazów do animacji
    kadry = []
    #indeks dla poszczególnych kroków
    m = 0
    lista_oz.append(0)
    lista_zz.append(k)
    lista_zd.append(N**2 - k)
    ozdrowiency = 0
    zarazeni = 0
    zdrowi = 0
    #poszczególne kadry animacji są zapisywane do folderu WYNIK_M_N_k_(p_w)_(p_z)_r
    identyfikator = ("_" + str(M) + "_" + str(N) + "_" + str(k) + "_" + str(p_w) + "_" + str(p_z) + "_" + str(r))
    os.mkdir("./WYNIK" + identyfikator)
    kadr = plt.imshow(populacja, "brg", vmin=0, vmax=2, animated=True)
    kadry.append([kadr])
    plt.savefig("./WYNIK" + identyfikator + "/" + str(m) + ".png")
    while((m < M) and (ozdrowiency < N**2)):
        ozdrowiency = 0
        zarazeni = 0
        zdrowi = 0
        for i in range(N):
            for j in range(N):
                if populacja[i][j] == 0:
                    zarazeni_okolica = kontakt(i, j, r, N, populacja)
                    if random.random() <= 1 - (1 - p_z)**zarazeni_okolica:
                        zarazeni += 1
                        populacja_nast[i][j] = 1
                        pass
                    else:
                        zdrowi += 1
                        populacja_nast[i][j] = 0
                        pass
                    pass
                elif populacja[i][j] == 1:
                    if random.random() <= p_w:
                        ozdrowiency += 1
                        populacja_nast[i][j] = 2
                        pass
                    else:
                        zarazeni += 1
                        populacja_nast[i][j] = 1
                        pass
                    pass
                else:
                    ozdrowiency += 1
                    populacja_nast[i][j] = 2
                    pass
                pass
            pass
        lista_oz.append(ozdrowiency)
        lista_zd.append(zdrowi)
        lista_zz.append(zarazeni)
        pomocnicza = populacja
        populacja = populacja_nast
        populacja_nast = pomocnicza
        m += 1
        kadr = plt.imshow(populacja, "brg", vmin=0, vmax=2, animated=True)
        kadry.append([kadr])
        plt.savefig("./WYNIK" + identyfikator + "/" + str(m) + ".png")
        pass
    print("Poszczególne kadry znajdują się w folderze " + "./WYNIK" + identyfikator)
    plt.title("Wizualizacja zarażeń")
    film = animation.ArtistAnimation(plt.figure(), kadry, interval=50, blit=True)
    obrazuj_pandemie(m, lista_oz, lista_zd, lista_zz)
    plt.savefig("Wykres" + identyfikator + ".png")
    plt.show()
    pass

if len(sys.argv) == 7:
    M = int(sys.argv[1])
    N = int(sys.argv[2])
    k = int(sys.argv[3])
    p_w = float(sys.argv[4])
    p_z = float(sys.argv[5])
    r = int(sys.argv[6])
    symulacja_pandemii(M, N, k, p_w, p_z, r)
    pass
else:
    print("Niewłaściwa liczba argumentów: M, N, k, p_w, p_z, r")
