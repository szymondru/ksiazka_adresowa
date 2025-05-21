import json
import sqlite3
from PyQt6.QtWidgets import QMessageBox

DANE = "kontakty.json"

class DataManager:
    """ Zarządzanie danymi """

    def __init__(self, plik=DANE, plik_db="backup.db"):
        self.plik = plik
        self.plik_db = plik_db
        self.conn = None
        self.cursor = None
        self.kontakty = self.dane_odczyt()
        self.baza_danych_inicjuj()

    # Zamknięcie bazy danych przy zamknięciu programu
    def __del__(self):
        if self.conn:
            self.conn.close()

    # Odczyt danych z pliku JSON (lub przywrócenie z backup'u)
    def dane_odczyt(self):
        try:
            with open(self.plik, "r", encoding="utf-8") as file:
                dane = json.load(file)
                if isinstance(dane, list) and all(isinstance(entry, dict) for entry in dane):
                    self.kontakty = dane
                    self.kontakty_sprawdz()
                    return self.kontakty
                else:
                    raise ValueError("Nieprawidłowa struktura danych.")
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            print("Błąd odczytu. \n"
                  "Plik danych jest uszkodzony lub ma nieprawidłową strukturę. \n"
                  "Przywracanie danych z backup'u...")
            self.baza_danych_przywroc_backup()
            self.kontakty_sprawdz()
            if not self.kontakty:
                print("Nie udało się przwrócić kontaktów z backup'u. " \
                "Tworzenie pustej listy kontaktów.")
                self.kontakty = []
            self.kontakty_sprawdz()
            return self.kontakty

    # Zapis danych do pliku JSON (kontakty.json) oraz backup (backup.db)
    def dane_zapis(self):
        try:
            with open(self.plik, "w", encoding="utf-8") as file:
                json.dump(self.kontakty, file, indent=4, ensure_ascii=False)
                self.baza_danych_backup()
        except IOError as e:
            QMessageBox.critical(None, "Błąd zapisu", f"Nie można zapisać danych: {e}")

    # Zainicjowanie bazy danych sqlite do backup'u
    def baza_danych_inicjuj(self):
        try:
            self.conn = sqlite3.connect(self.plik_db)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS kontakty (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    imie TEXT NOT NULL,
                    nazwisko TEXT NOT NULL,
                    tel TEXT NOT NULL,
                    email TEXT,
                    ulica TEXT,
                    miasto TEXT,
                    kod TEXT
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Błąd bazy danych",
                                 f"Nie można zainicjować bazy danych: {e}")

    # Dodanie kontaktów do bazy danych w celu backup'u
    def baza_danych_backup(self):
        try:
            self.cursor.execute("DELETE FROM kontakty")
            for kontakt in self.kontakty:
                self.cursor.execute("""
                    INSERT INTO kontakty (imie, nazwisko, tel, email, ulica, miasto, kod)
                    VALUES (?, ?, ?, ?, ?, ?, ?) """, (
                    kontakt.get("imie", ""),
                    kontakt.get("nazwisko", ""),
                    kontakt.get("tel", ""),
                    kontakt.get("email", ""),
                    kontakt.get("ulica", ""),
                    kontakt.get("miasto", ""),
                    kontakt.get("kod", "")
                    ))
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Błąd bazy danych", f"Nie można wykonać backupu: {e}")

    # Przywrócenie danych z backup'u (bazy danych)
    def baza_danych_przywroc_backup(self):
        try:
            self.cursor.execute("SELECT imie, nazwisko, tel, email, ulica, miasto, kod FROM kontakty")
            rows = self.cursor.fetchall()
            self.kontakty = [
                {"imie": row[0], "nazwisko": row[1], "tel": row[2], "email": row[3],
                 "ulica": row[4], "miasto": row[5], "kod": row[6]}
                for row in rows]
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Błąd bazy danych", f"Nie można przywrócić danych: {e}")

    # Sprawdź kontakty. Dodanie brakujących (pustych) pól
    def kontakty_sprawdz(self):
        for kontakt in self.kontakty:
            for wyraz in ["imie", "nazwisko", "tel", "email", "ulica", "miasto", "kod"]:
                if wyraz not in kontakt:
                    kontakt[wyraz] = ""

    # Sprawdzenie poprawności e-mail
    @staticmethod
    def czy_email(email):
        if "@" not in email or email.count("@") != 1:
            return False
        nazwa, domena = email.split("@")
        if not nazwa or not domena or "." not in domena:
            return False
        if domena.startswith(".") or domena.endswith("."):
            return False
        if ".." in email:
            return False
        return True
