import random

# jobbra, fel, balra, le
IRANYOK = [(0, 1), (1,0), (0,-1), (-1,0)]
class Pozicio:
    def __init__(self, koordinata, falak) -> None:
        self.koordinata = koordinata
        self.falak = falak

    def fal_lebont(self, fal_szama) -> None:
        self.falak[fal_szama] = False

# az algoritmust ezen az oldalon találtam:
# https://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm
def uj_labirintus(szelesseg: int, magassag: int) -> set:
    labirintus = set()
    while len(labirintus) < 2:
        labirintus.add(uj_veletlen_pozicio(szelesseg -1, magassag -1))

    kezdo_poz = list(labirintus)[0]

    lepesek = [uj_lepes(list(labirintus)[0], (0,0), szelesseg, magassag, kezdo_poz)]
    while len(labirintus) < szelesseg * magassag:
        while lepesek[-1][0].koordinata not in labirintus:
            lepesek += uj_lepes(lepesek[-1][0], lepesek[-1][1], szelesseg, magassag, kezdo_poz)





    return labirintus

def uj_lepes(pozicio: Pozicio, elozo_irany: tuple, max_x: int, max_y: int, kezdo) -> tuple:
    irany = (0,0)
    uj_poz = Pozicio((-1, -1), [True,True,True,True])
    while uj_poz.koordinata[0] not in range(0, max_x + 1) and uj_poz.koordinata[1] not in range(0, max_y + 1) and uj_poz != kezdo:
        while irany != elozo_irany:
            irany = random.choice(IRANYOK)

        uj_poz = Pozicio((pozicio.koordinata[0] + irany[0], pozicio.koordinata[1] + irany[1]), [True,True,True,True])
    return (uj_poz, irany)

def uj_veletlen_pozicio(max_x: int, max_y: int) -> Pozicio:
    return Pozicio((random.randint(0, max_x), random.randint(0, max_y)), [True, True, True, True])
