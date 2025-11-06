#x = 5
#y = 10
#punkt = [x,y]
#k = 0
#wez_sasiadow_krzyz(punkt, 0)
#wez_sasiadow_krzyz(punkt, 1)
from itertools import count

igen = count(1)
matrix = [[f"{next(igen):3d}" for i in range(1, 16)] for j in range(1, 16)]

def display(tablica = matrix):
    for row in tablica:
        print(" ".join(row))

def wez_sasiadow_krzyz(matriks, punkt, k_idx, kierunek, zakres = 4):
    sasiedzi = []
    for d in range(1, zakres + 1):

        pkd = punkt[k_idx] + (d * kierunek)

        if kierunek == 1:
            if pkd > 14:
                break
        elif kierunek == -1:
            if pkd < 0:
                break
        else:
            raise ValueError

        if k_idx == 0:
            sasiad = matriks[pkd][punkt[1]]
        elif k_idx == 1:
            sasiad = matriks[punkt[0]][pkd]
        else:
            raise ValueError

        sasiedzi.append(sasiad)

    return sasiedzi

def wez_sasiadow_skos(matriks, punkt, zakres = 4 ):
    sasiedzi = []

    kierunek = [(-1,-1),(-1,1),(1,-1),(1,1)]

    for kierunek_x, kierunek_y in kierunek:
        sasiedzi_kierunek = []
        for d in range(1, zakres + 1):
            pkd_x = punkt[0] + (d *kierunek_x)
            pkd_y = punkt[1] + (d * kierunek_y)

            if pkd_x < 0 or pkd_x > 14 or pkd_y < 0 or pkd_y > 14:
                continue

            sasiad = matriks[pkd_x][pkd_y]

            sasiedzi_kierunek.append(sasiad)
        sasiedzi.append(sasiedzi_kierunek)

    return sasiedzi

if __name__ == "__main__":
    x = 13
    y = 14
    matrix[x][y] = "  #"
    display(tablica=matrix)
    print(wez_sasiadow_skos(matrix, (13,14)))

#wez_sasiadow_krzyz(matrix, punkt, 1, -1) lewo
#wez_sasiadow_krzyz(matrix, punkt, 1, 1) prawo
#wez_sasiadow_krzyz(matrix, punkt, 0, -1) gora
#wez_sasiadow_krzyz(matrix, punkt, 0, 1) dol

