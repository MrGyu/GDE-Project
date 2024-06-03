from datetime import datetime, date, timedelta
import random

class Szoba:
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
        self.foglalt_datumok = []

    def foglal(self, datum):
        if datum not in self.foglalt_datumok:
            self.foglalt_datumok.append(datum)
            return True
        return False

    def lemond(self, datum):
        if datum in self.foglalt_datumok:
            self.foglalt_datumok.remove(datum)
            return True
        return False

class EgyagyasSzoba(Szoba):
    pass

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar, potagy_lehetoseg=False):
        super().__init__(szobaszam, ar)
        self.potagy_lehetoseg = potagy_lehetoseg

class Szalloda:
    def __init__(self, nev, szobak):
        self.nev = nev
        self.szobak = szobak

    def szabad_szoba_keresese(self, szoba_tipus, datum):
        for szoba in self.szobak:
            if isinstance(szoba, szoba_tipus) and datum not in szoba.foglalt_datumok:
                return szoba
        return None

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

def menu():
    print("\n1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("0. Kilépés")

def foglalas_felvetele(szalloda, foglalasok):
    print("\nSzoba típusok:")
    print("1. Egyágyas szoba")
    print("2. Kétágyas szoba")
    szoba_tipus_valasztas = input("Kérem válassza ki a szoba típusát (1-2): ")
    datum_str = input("Kérem adja meg a foglalás dátumát (YYYY-MM-DD): ")

    try:
        datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
        if datum <= date.today():
            print("Nem lehet múltbeli vagy mai dátumot megadni.")
            return
    except ValueError:
        print("Hibás dátum formátum.")
        return

    if szoba_tipus_valasztas == "1":
        szoba_tipus = EgyagyasSzoba
    elif szoba_tipus_valasztas == "2":
        szoba_tipus = KetagyasSzoba
    else:
        print("Érvénytelen választás.")
        return

    szoba = szalloda.szabad_szoba_keresese(szoba_tipus, datum)
    if szoba:
        if szoba.foglal(datum):
            foglalasok.append(Foglalas(szoba, datum))
            print(f"Foglalás sikeres: {szoba.szobaszam} szoba {datum.strftime('%Y-%m-%d')} dátumra. Ár: {szoba.ar} Ft.")
        else:
            print("A megadott dátumra a szoba nem elérhető.")
    else:
        print("Nincs szabad szoba a megadott típusban erre a dátumra.")

def foglalas_leadasa(szalloda, foglalasok):
    szoba_szam = input("Kérem adja meg a lemondani kívánt foglalás szoba számát: ")
    relevans_foglalasok = [foglalas for foglalas in foglalasok if foglalas.szoba.szobaszam == szoba_szam]
    
    if not relevans_foglalasok:
        print("Nincs ilyen foglalás.")
        return
    
    print("\nLemondásra elérhető foglalások:")
    for index, foglalas in enumerate(relevans_foglalasok, start=1):
        print(f"{index}. Dátum: {foglalas.datum.strftime('%Y-%m-%d')}, Ár: {foglalas.szoba.ar} Ft")
    
    valasztas = input("Kérem válassza ki a lemondani kívánt foglalást (1-{}): ".format(len(relevans_foglalasok)))
    
    try:
        valasztas_index = int(valasztas) - 1
        if 0 <= valasztas_index < len(relevans_foglalasok):
            foglalas = relevans_foglalasok[valasztas_index]
            if foglalas.szoba.lemond(foglalas.datum):
                foglalasok.remove(foglalas)
                print("Lemondás sikeres.")
            else:
                print("Nem sikerült lemondani a foglalást.")
        else:
            print("Érvénytelen választás.")
    except ValueError:
        print("Hibás választás.")

def foglalasok_listazasa(foglalasok):
    print("\nAktuális foglalások:")
    for foglalas in foglalasok:
        print("Szoba:", foglalas.szoba.szobaszam, "Dátum:", foglalas.datum.strftime("%Y-%m-%d"))

def random_jovobeli_datum():
    return date.today() + timedelta(days=random.randint(1, 365))

def main():
    egyagyas1 = EgyagyasSzoba("101", 2000)
    ketagyas1 = KetagyasSzoba("201", 3000, True)
    ketagyas2 = KetagyasSzoba("202", 3000, True)
    szalloda = Szalloda("Példa Szálloda", [egyagyas1, ketagyas1, ketagyas2])

    foglalasok = [
        Foglalas(egyagyas1, random_jovobeli_datum()),
        Foglalas(ketagyas1, random_jovobeli_datum()),
        Foglalas(ketagyas1, random_jovobeli_datum()),
        Foglalas(ketagyas1, random_jovobeli_datum()),
        Foglalas(egyagyas1, random_jovobeli_datum())
    ]

    # Foglaljuk le az alapértelmezett foglalások dátumait
    for foglalas in foglalasok:
        foglalas.szoba.foglal(foglalas.datum)

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
