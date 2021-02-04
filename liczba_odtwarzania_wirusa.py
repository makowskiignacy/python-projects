from scipy.linalg import lstsq
import numpy as np
import math
import pylab
import urllib.request as ureq
import re
import sys

#Sprawdza czy nazwa kraju na początku zadanego napisu jest zgodna z zapytaniem
def czy_kraj(napis, kraj):
    i = 0
    while(napis[i] < "A" or napis[i] > "Z"):
        i += 1
        pass
    wynik = True
    i_max = len(napis)
    j_max = len(kraj)
    j = 0
    while(wynik and (i < i_max and (j < j_max))):
        wynik = (napis[i] == kraj[j])
        i += 1
        j += 1
        pass
    return wynik

#Funkcja zwraca wektor [a, b], będący współrzędnymi funkcji liniowej
def najmniejsze_kwadraty(lista_danych, wagi):
    liczba_dni = len(lista_danych)
    b = np.array(lista_danych)
    a = np.zeros((liczba_dni, 2))
    #ustawienie liniowej zależności y = ax + b (x-liczba dni)
    #a[][0]-współczynnik a
    #a[][1]-współczynnik b
    for i in range(liczba_dni):
        a[i][0] = i + 1
        a[i][1] = 1
        pass
    #ustawienie wag elementów
    for j in range(liczba_dni):
        waga = math.sqrt(wagi[j])
        b[j] *= waga
        a[j][0] *= waga
        a[j][1] *= waga
        pass
    return lstsq(a, b)[0]

#Funkcja zwarca listę zachorowań z pierwszych 28 dni (od pierwszego przypadku) dla zadanego kraju
#Jeśli kraj nie znajduje się na liście zwraca listę pustą
#Jeśli kraj ma mniej niż 28 dni zwraca wszystkie
def import_danych_covid(kraj):
    dane_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    dane_swiat = ureq.urlopen(dane_url)
    dane_kraj = dane_swiat.readline()
    znaleziony_kraj = False
    while(dane_kraj and (not znaleziony_kraj)):
        kraj_str = str(dane_kraj)
        znaleziony_kraj = czy_kraj(kraj_str, kraj)
        if (not znaleziony_kraj):
            dane_kraj = dane_swiat.readline()
        pass
    if znaleziony_kraj:
        kraj_calkowite = map(int, re.findall('\d+', kraj_str))
        lista_danych = list(kraj_calkowite)
        del lista_danych[0:4]
        while(lista_danych[0] == 0):
            lista_danych.remove(0)
            pass
    else:
        lista_danych = []
    return lista_danych[0:min(28, len(lista_danych) - 1)]

#Funkcja dopasowuje do ilości zachorowań w kraju funkcję wykładniczą i tworzy wykres
#Sprowadza problem do problemu liniowego, wykorzystuje funkcję najmniejsze kwadraty()
#Podstawowa liczba odtwarzania wirusa (R), jest wyświetlana na wykresie
def liczba_odtwarzania_wirusa(kraj):
    dane_wykladnicze = import_danych_covid(kraj);
    dane_zlogarytmowane = []
    for i in dane_wykladnicze:
        dane_zlogarytmowane.append(math.log10(i))
        pass
    rozwiazanie = najmniejsze_kwadraty(dane_zlogarytmowane, dane_wykladnicze)
    R = 10**rozwiazanie[0]
    n = 10**rozwiazanie[1]
    dlugosc = len(dane_wykladnicze)
    dopasowanie = []
    for i in range(dlugosc):
        dopasowanie.append(n*(R**i))
        pass
    pylab.plot(range(dlugosc), dane_wykladnicze, "rx", label="dane")
    pylab.plot(range(dlugosc), dopasowanie, "b", label="dopasowanie\nR = " + str(R))
    pylab.title("Zarażeni (" + kraj + ")")
    pylab.xlabel("Dni od pierwszego przypadku")
    pylab.ylabel("Liczba zarażonych")
    pylab.legend()
    pylab.show()
    pass

if len(sys.argv) == 2:
    liczba_odtwarzania_wirusa(sys.argv[1])
else:
    print("Nie został podany pojedyńczy kraj do anlizy, zostanie ona przeprowadzona dla Polski")
    liczba_odtwarzania_wirusa("Poland")
