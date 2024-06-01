from datetime import datetime

def menu():
    print("\n1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("0. Kilépés")

def foglalas_felvetele(szalloda, foglalasok):
    szoba_szam = input("Kérem adja meg a foglalni kívánt szoba számát: ")
    datum_str = input("Kérem adja meg a foglalás dátumát (YYYY-MM-DD): ")
    datum = datetime.strptime(datum_str, "%Y-%m-%d")
    
    for szoba in szalloda.szobak:
        if szoba.szobaszam == szoba_szam:
            if szoba.foglal(datum):
                foglalasok.append(Foglalas(szoba, datum))
                print("Foglalás sikeres.")
            else:
                print("A megadott dátumra a szoba nem elérhető.")
            break
    else:
        print("Nincs ilyen szobaszám.")

def foglalas_leadasa(szalloda, foglalasok):
    szoba_szam = input("Kérem adja meg a lemondani kívánt foglalás szoba számát: ")
    datum_str = input("Kérem adja meg a lemondani kívánt foglalás dátumát (YYYY-MM-DD): ")
    datum = datetime.strptime(datum_str, "%Y-%m-%d")
    
    for foglalas in foglalasok:
        if foglalas.szoba.szobaszam == szoba_szam and foglalas.datum == datum:
            foglalas.szoba.lemond(datum)
            foglalasok.remove(foglalas)
            print("Lemondás sikeres.")
            break
    else:
        print("Nincs ilyen foglalás.")

def foglalasok_listazasa(foglalasok):
    print("\nAktuális foglalások:")
    for foglalas in foglalasok:
        print("Szoba:", foglalas.szoba.szobaszam, "Datum:", foglalas.datum.strftime("%Y-%m-%d"))

def main():
    egyagyas1 = EgyagyasSzoba("101", 2000)
    ketagyas1 = KetagyasSzoba("201", 3000, True)
    szalloda = Szalloda("Példa Szálloda", [egyagyas1, ketagyas1])

    foglalasok = [
        Foglalas(egyagyas1, datetime(2024, 5, 5)),
        Foglalas(ketagyas1, datetime(2024, 5, 7)),
        Foglalas(ketagyas1, datetime(2024, 5, 9)),
        Foglalas(ketagyas1, datetime(2024, 5, 11)),
        Foglalas(egyagyas1, datetime(2024, 5, 12))
    ]

    while True:
        menu()
        valasztas = input("Kérem válasszon a menüpontok közül (0-3): ")

        if valasztas == "1":
            foglalas_felvetele(szalloda, foglalasok)
        elif valasztas == "2":
            foglalas_leadasa(szalloda, foglalasok)
        elif valasztas == "3":
            foglalasok_listazasa(foglalasok)
        elif valasztas == "0":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás.")

if __name__ == "__main__":
    main()