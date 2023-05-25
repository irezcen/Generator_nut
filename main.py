import random


nuty_is = ['c', 'cis', 'd', 'dis', 'e',
           'f', 'fis', 'g', 'gis', 'a', 'ais', 'b']
nuty_isnot = ['c', 'des', 'd', 'es', 'e',
              'f', 'ges', 'g', 'as', 'a', 'bes', 'b']


def losuj_liczby(a):
    n = a/4
    zbior = [1/16, 1/8, 1/4, 1/2, 1]
    liczby = []
    wydluzenie = []
    luki = []
    for i in range(4):
        counter = 0
        suma = []
        while sum(suma) < n/a:
            k = 1
            liczba = random.choice(zbior)
            if random.random() < 0.05:
                k = 1.5
                wydluzenie.append(True)
            else:
                wydluzenie.append(False)
            luki.append(False)
            if (sum(suma) + liczba*k) <= n/a:
                liczby.append(liczba)
                suma.append(liczba*k)
            else:
                wydluzenie.pop(-1)
                luki.pop(-1)
            if (0 < (n/a-sum(suma)) < 1/16 or counter == 100):
                wydluzenie.pop(-1)
                liczby.pop(-1)
                suma.pop(-1)
                luki.pop(-1)
                counter = 0
            counter += 1
        if (random.random() < 0.2):
            luki.pop(-1)
            luki.append(True)
    return liczby, wydluzenie, luki


def losuj_interwal(wagi, pierwszy, p):
    if (pierwszy):
        return p
    zakres = range(13)
    suma_wag = sum(wagi)
    wagi = [waga / suma_wag for waga in wagi]
    rd = random.random()
    suma = 0
    for i, waga in enumerate(wagi):
        suma += waga
        if (rd < suma):
            return zakres[i]
    return zakres[-1]


def losuj_dzwiek(wagi, ostatni, ambitus, pierwszy, p):
    interwal = losuj_interwal(wagi, pierwszy, p)
    amb_l = ambitus[0]
    amb_h = ambitus[1]
    oct = 0
    c = 1
    b = ""
    dzwieki = nuty_is
    if (random.choice([True, False])):
        c *= -1
    interwal *= c
    while ((ostatni+interwal) < amb_l or (ostatni+interwal) > amb_h):
        if (random.choice([True, False])):
            c *= -1
        interwal = losuj_interwal(wagi, pierwszy, p)*c
    d = ostatni+interwal
    while (d >= 12):
        oct += 1
        d -= 12
    nowe_dzwieki = random.choice([nuty_is, nuty_isnot])
    if (random.choice([True, False]) and (nuty_is[d] == nuty_isnot[d])):
        dzwieki = nowe_dzwieki
    b = dzwieki[d]
    for i in range(oct):
        b += "'"

    return ostatni+interwal, b, oct


start_str = "\\version \"2.24.1\"\n\\paper { \n #(set-paper-size \"a4\")\n }\n \\layout {\n indent = 0\\in\n ragged-last = ##f\n \\context {\n \\Score\n }\n}\n\\fixed c\n{"
end_str = "\n\\bar \"||\"\n}\n"

metrum = int(input('metrum?'))
liczba_taktow = int(input('liczba taktów?'))
pauzy_prob = float(input('prawdopodobienstwo pauzy?'))
stopien_poczatkowy = int(input('pierwszy dzwiek?'))-1
ambitus = input('ambitus?(2)')
ambitus = ambitus.split(" ")
ambitus = [int(f)-1 for f in ambitus]
interwaly_prob = input('prawdopodobienstwa interwalow?(13)')
if (interwaly_prob == ""):
    interwaly_prob = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
else:
    interwaly_prob = interwaly_prob.split(" ")
    interwaly_prob = [float(f) for f in interwaly_prob]


octave = 0
ost = 0
d = ost
p = stopien_poczatkowy
skip = False
pierwszy = True
dzwieki = "\n"
time = f"\n\\time {metrum}/4"
key = f"\n\\key c \\major"
rytm = []
kropki = []
luk = []
old_b = ''

for i in range(liczba_taktow):
    r, k, l = losuj_liczby(metrum)
    rytm += r
    kropki += k
    luk += l
rytm = [int(i**-1) for i in rytm]

for r, k, l in zip(rytm, kropki, luk):
    if random.random() < pauzy_prob:
        b = 'r'
    elif (skip != True):
        d, b, oct = losuj_dzwiek(interwaly_prob, ost, ambitus, pierwszy, p)
        pierwszy = False
        if (oct == 0):
            ottave = -1
        elif (oct == 1):
            ottave = 0
        else:
            ottave = oct-2
        if (octave != ottave):
            octave = ottave
            dzwieki += f" \\ottava #{octave}\n"
    if (skip):
        b = old_b
    dzwieki += f" {b}{r}"
    ost = d
    old_b = b
    if (k):
        dzwieki += "."
    if (l):
        skip = True
        dzwieki += "~"
    else:
        skip = False
    dzwieki += "\n"


wszystko = start_str+time+key+dzwieki+end_str

f = open("projekt.ly", 'w')
f.write(wszystko)
f.close()
