import random
from itertools import count

igen = count(1)

matrix = [[f"{next(igen):3d}" for i in range(1, 16)] for j in range(1, 16)]

def nowy_board():
    return [["." for _ in range(15)] for _ in range(15)]

def display(tablica):
    for row in tablica:
        print(" ".join(row))

def rozpoczynajacy_zawodnik():
    aktualny_gracz = random.choice(["x", "o"])
    print(f"Grę rozpoczyna: {aktualny_gracz}")
    return aktualny_gracz

def zmiana_zawodnika(gracz):
    if gracz == "x":
        return "o"
    else:
        return "x"

def kordynaty(wspolrzedne):
    while True:
        try:
            zakres = int(input(f"Podaj {wspolrzedne}: "))
        except ValueError:
            print("Nipoprawna wartość. Proszę podać liczbę.")
            continue

        if 0 <= zakres <= 14:
            return zakres
        else:
            print("Wartość musi być w zakresie od 0 do 14")

def wolna_pozycja(board):
    while True:
        x = kordynaty("x")
        y = kordynaty("y")
        if board[x][y] == ".":
            return [x, y]
        else:
            print("Pozycja jest zajęta. Proszę podać nową.")

def cli():
    aktualny_gracz = rozpoczynajacy_zawodnik()
    board = nowy_board()
    while True:
        display(board)
        print(f"Ruch gracza: {aktualny_gracz}")

        pozycja = wolna_pozycja(board)
        x = pozycja[0]
        y = pozycja[1]

        board[x][y] = aktualny_gracz
        if czy_wygral(aktualny_gracz, board):
            print(f"Wygrał gracz: {aktualny_gracz}")
            print("Czy chesz zagrać ponownie?")
            decyzja = input("T - tak, N - nie.")
            if decyzja != "T":
                return
            aktualny_gracz = rozpoczynajacy_zawodnik()
            board = nowy_board()
            continue

        aktualny_gracz = zmiana_zawodnika(aktualny_gracz)

def policz(lista, element):
    ile = 0
    for i in lista:
        if i == element:
            ile = ile + 1
    return ile

def czy_wygral(aktulany_gracz, board):
    for x in range(15):
        for y in range(15):
            if board[x][y] != aktulany_gracz:
                continue

            sasiedzi_lewa = sprawdz_lewa(x, y, board)
            sasiedzi_aktulny_gracz = policz(sasiedzi_lewa, aktulany_gracz)

            if sasiedzi_aktulny_gracz == 4:
                return True

            sasiedzi_prawa = sprawdz_prawa(x, y, board)
            sasiedzi_aktulny_gracz = policz(sasiedzi_prawa, aktulany_gracz)

            if sasiedzi_aktulny_gracz == 4:
                return True

            sasiedzi_gora = sprawdz_gora(x, y, board)
            sasiedzi_aktulny_gracz = policz(sasiedzi_gora, aktulany_gracz)

            if sasiedzi_aktulny_gracz == 4:
                return True

            sasiedzi_dol = sprawdz_dol(x, y, board)
            sasiedzi_aktulny_gracz = policz(sasiedzi_dol, aktulany_gracz)

            if sasiedzi_aktulny_gracz == 4:
                return True

            sasiedzi_lewa_gora = sprawdz_lewo_gora(x, y, board)
            sasiedzi_aktulny_gracz = policz(sasiedzi_lewa_gora, aktulany_gracz)

            if sasiedzi_aktulny_gracz == 4:
                return True

            sasiedzi_prawo_gora = sprawdz_prawo_gora(x, y, board)
            sasiedzi_aktulny_gracz = policz(sasiedzi_prawo_gora, aktulany_gracz)

            if sasiedzi_aktulny_gracz == 4:
                return True

            sasiedzi_lewo_dol = sprawdz_lewo_dol(x, y, board)
            sasiedzi_aktulny_gracz = policz(sasiedzi_lewo_dol, aktulany_gracz)

            if sasiedzi_aktulny_gracz == 4:
                return True

            sasiedzi_prawo_dol = sprawdz_prawo_dol(x, y, board)
            sasiedzi_aktulny_gracz = policz(sasiedzi_prawo_dol, aktulany_gracz)

            if sasiedzi_aktulny_gracz == 4:
                return True

    return False

def sprawdz_lewa(x, y, board, zakres = 4):
    sasiedzi = []
    for dy in range(1, zakres + 1):
        i = y - dy
        if i < 0:
            break
        sasiad = board[x][i]
        sasiedzi.append(sasiad)

    return sasiedzi

def sprawdz_prawa(x, y, board, zakres = 4):
    sasiedzi = []
    for dy in range(1, zakres + 1):
        if y + dy > 14:
            break
        sasiad = board[x][y + dy]
        sasiedzi.append(sasiad)

    return sasiedzi

def sprawdz_gora(x, y, board, zakres = 4):
    sasiedzi = []
    for dx in range(1, zakres + 1):
        if x - dx < 0:
            break
        sasiad = board[x - dx][y]
        sasiedzi.append(sasiad)

    return sasiedzi

def sprawdz_dol(x, y, board, zakres = 4):
    sasiedzi = []
    for dx in range(1, zakres + 1):
        if x + dx > 14:
            break
        sasiad = board[x + dx][y]
        sasiedzi.append(sasiad)

    return sasiedzi

def sprawdz_lewo_gora(x, y, board, zakres = 4):
    sasiedzi = []
    for i in range(1, zakres + 1):
        dx = i
        dy = i
        if x - dx < 0 or y - dy < 0:
            break
        sasiad = board[x - dx][y - dy]
        sasiedzi.append(sasiad)

    return sasiedzi

def sprawdz_prawo_gora(x, y, board, zakres = 4):
    sasiedzi = []
    for i in range(1, zakres + 1):
        dx = i
        dy = i
        if x - dx < 0 or y + dy > 14:
            break
        sasiad = board[x - dx][y + dy]
        sasiedzi.append(sasiad)

    return sasiedzi

def sprawdz_lewo_dol(x, y, board, zakres = 4):
    sasiedzi = []
    for i in range(1, zakres + 1):
        dx = i
        dy = i
        if x + dx > 14 or y - dy < 0:
            break
        sasiad = board[x + dx][y - dy]
        sasiedzi.append(sasiad)

    return sasiedzi

def sprawdz_prawo_dol(x, y, board, zakres = 4):
    sasiedzi = []
    for i in range(1, zakres + 1):
        dx = i
        dy = i
        if x + dx > 14 or y + dy > 14:
            break
        sasiad = board[x + dx][y + dy]
        sasiedzi.append(sasiad)

    return sasiedzi

if __name__ == "__main__":
    cli()
























