from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QApplication
from PyQt6.QtGui import QPalette
from gui_nowy_kontakt import NowyKontakt



class Szukaj(QWidget):
    """ Funkcjonalność: Szukaj kontaktów """

    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.edytuj = None
        self.initUI()

    # Wywołanie interfejsu
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Szukaj kontaktów")
        self.setGeometry(300, 300, 760, 500)

        # Opis działania 'Szukaj kontaktów'
        instrukcja = QLabel("\nAby wyszukać kontakt, wpisz imię, nazwisko lub inne dane w polu wyszukiwania. \n"
                            "Możesz skorzystać z opcji 'Pokaż wszystkie', aby zobaczyć wszystkie kontakty. \n"
                            "Aby edytować, wybierz kontakt z tabeli i kliknij przycisk 'Edytuj'.\n")

        # Dostosowanie koloru tekstu
        kolorki = QApplication.palette()
        czy_ciemny_motyw = kolorki.color(QPalette.ColorRole.WindowText).lightness() > (
                    kolorki.color(QPalette.ColorRole.Window).lightness())
        kolor = "#FFFFFF" if czy_ciemny_motyw else "#000000"
        instrukcja.setStyleSheet(f"font-size: 12px; color: {kolor};")
        layout.addWidget(instrukcja)

        self.szukaj_in = QLineEdit(self)
        self.szukaj_in.setPlaceholderText("Wyszukaj...")
        self.szukaj_in.returnPressed.connect(self.kontakty_szukaj)
        layout.addWidget(self.szukaj_in)

        self.przycisk_szukaj = QPushButton("Szukaj", self)
        self.przycisk_szukaj.clicked.connect(self.kontakty_szukaj)
        layout.addWidget(self.przycisk_szukaj)

        self.przycisk_wyczysc = QPushButton("Wyczyść", self)
        self.przycisk_wyczysc.clicked.connect(self.czysc_szukaj)
        layout.addWidget(self.przycisk_wyczysc)

        self.przycisk_pokaz_wszystkie = QPushButton("Pokaż wszystkie", self)
        self.przycisk_pokaz_wszystkie.clicked.connect(self.szukaj_pokaz_wszystkie)
        layout.addWidget(self.przycisk_pokaz_wszystkie)

        self.tabela_wyniki = QTableWidget(self)
        self.tabela_wyniki.setColumnCount(7)
        self.tabela_wyniki.setHorizontalHeaderLabels(["Imię", "Nazwisko", "Telefon",
                                                     "Email", "Ulica", "Miasto", "Kod pocztowy"])
        layout.addWidget(self.tabela_wyniki)

        self.szukaj_pole = QLineEdit(self)
        self.szukaj_pole.setPlaceholderText("Pole (np. imie, nazwisko, miasto)")
        layout.addWidget(self.szukaj_pole)

        self.przycisk_edytuj = QPushButton("Edytuj", self)
        self.przycisk_edytuj.clicked.connect(self.szukaj_edycja_kontaktu)
        layout.addWidget(self.przycisk_edytuj)

    # Szukaj kontaktów
    def kontakty_szukaj(self):
        zapytanie = self.szukaj_in.text().strip().lower()
        pole = self.szukaj_pole.text().strip().lower()
        self.tabela_wyniki.clearContents()

        if not zapytanie:
            QMessageBox.warning(self, "Błąd", "Wprowadź zapytanie do wyszukiwania.")
            return

        szukane = zapytanie.split()

        rekordy = []
        for entry in self.data_manager.kontakty:
            if pole and pole in entry:
                if all(slowo in str(entry[pole]).lower() for slowo in szukane):
                    rekordy.append(entry)
            else:
                if any(all(slowo in str(value).lower() for slowo in szukane
                           ) for value in entry.values()):
                    rekordy.append(entry)

        if not rekordy:
            QMessageBox.information(self, "Brak wyników", "Nie znaleziono żadnych wyników.")
        else:
            self.tabela_wyniki.setRowCount(len(rekordy))
            for row, entry in enumerate(rekordy):
                self.tabela_wyniki.setItem(row, 0, QTableWidgetItem(entry.get("imie", "")))
                self.tabela_wyniki.setItem(row, 1, QTableWidgetItem(entry.get("nazwisko", "")))
                self.tabela_wyniki.setItem(row, 2, QTableWidgetItem(entry.get("tel", "")))
                self.tabela_wyniki.setItem(row, 3, QTableWidgetItem(entry.get("email", "")))
                self.tabela_wyniki.setItem(row, 4, QTableWidgetItem(entry.get("ulica", "")))
                self.tabela_wyniki.setItem(row, 5, QTableWidgetItem(entry.get("miasto", "")))
                self.tabela_wyniki.setItem(row, 6, QTableWidgetItem(entry.get("kod", "")))

    # Czyszczenie pól
    def czysc_szukaj(self):
        self.szukaj_in.clear()
        self.szukaj_pole.clear()
        self.tabela_wyniki.clearContents()

    # Funkcjonalność: pokaż wszystkie kontakty
    def szukaj_pokaz_wszystkie(self):
        self.tabela_wyniki.clearContents()
        kontakty = self.data_manager.kontakty

        if not kontakty:
            QMessageBox.information(self, "Brak danych", "Brak zapisanych kontaktów.")
            return

        self.tabela_wyniki.setRowCount(len(kontakty))
        for row, entry in enumerate(kontakty):
            self.tabela_wyniki.setItem(row, 0, QTableWidgetItem(entry.get("imie", "")))
            self.tabela_wyniki.setItem(row, 1, QTableWidgetItem(entry.get("nazwisko", "")))
            self.tabela_wyniki.setItem(row, 2, QTableWidgetItem(entry.get("tel", "")))
            self.tabela_wyniki.setItem(row, 3, QTableWidgetItem(entry.get("email", "")))
            self.tabela_wyniki.setItem(row, 4, QTableWidgetItem(entry.get("ulica", "")))
            self.tabela_wyniki.setItem(row, 5, QTableWidgetItem(entry.get("miasto", "")))
            self.tabela_wyniki.setItem(row, 6, QTableWidgetItem(entry.get("kod", "")))

    # Edytuj kontakt
    def szukaj_edycja_kontaktu(self):
        wybrany = self.tabela_wyniki.currentRow()
        if wybrany == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz kontakt do edycji.")
            return

        kontakt = {
            "imie": self.tabela_wyniki.item(wybrany, 0).text(),
            "nazwisko": self.tabela_wyniki.item(wybrany, 1).text(),
            "tel": self.tabela_wyniki.item(wybrany, 2).text(),
            "email": self.tabela_wyniki.item(wybrany, 3).text(),
            "ulica": self.tabela_wyniki.item(wybrany, 4).text(),
            "miasto": self.tabela_wyniki.item(wybrany, 5).text(),
            "kod": self.tabela_wyniki.item(wybrany, 6).text()
        }

        self.edytuj = EdytujKontakt(self.data_manager, kontakt, wybrany, self.tabela_wyniki, self)
        self.edytuj.show()


class EdytujKontakt(QWidget):
    """ Funkcjonalność: Edytowanie kontaktu """

    def __init__(self, data_manager, kontakt, wybrany, tabela_wyniki, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.kontakt = kontakt
        self.wybrany = wybrany
        self.tabela_wyniki = tabela_wyniki
        self.initUI()

    # Wywołanie interfejsu do edycji kontaktu
    def initUI(self):
        self.edytuj = NowyKontakt(self.data_manager)
        self.edytuj.imie_in.setText(self.kontakt["imie"])
        self.edytuj.nazwisko_in.setText(self.kontakt["nazwisko"])
        self.edytuj.tel_in.setText(self.kontakt["tel"])
        self.edytuj.email_in.setText(self.kontakt["email"])
        self.edytuj.ulica_in.setText(self.kontakt["ulica"])
        self.edytuj.miasto_in.setText(self.kontakt["miasto"])
        self.edytuj.kod_in.setText(self.kontakt["kod"])

        self.edytuj.przycisk_zapisz.setText("Edytuj kontakt")
        try:
            self.edytuj.przycisk_zapisz.clicked.disconnect()
        except TypeError:
            pass
        self.edytuj.przycisk_zapisz.clicked.connect(lambda: self.zmiana_zapisz(self.wybrany))
        self.edytuj.show()

    # Zapis zmian w edytowanym kontakcie, weryfikacja danych, aktualizacja tabeli
    def zmiana_zapisz(self, wybrany):
        nowy_kontakt = {
            "imie": self.edytuj.imie_in.text().strip(),
            "nazwisko": self.edytuj.nazwisko_in.text().strip(),
            "tel": self.edytuj.tel_in.text().strip(),
            "email": self.edytuj.email_in.text().strip(),
            "ulica": self.edytuj.ulica_in.text().strip(),
            "miasto": self.edytuj.miasto_in.text().strip(),
            "kod": self.edytuj.kod_in.text().strip()
        }

        bledy = []
        if not nowy_kontakt["imie"]:
            bledy.append("Pole 'imię' jest wymagane.")
        if not nowy_kontakt["nazwisko"]:
            bledy.append("Pole 'nazwisko' jest wymagane.")
        if not nowy_kontakt["tel"]:
            bledy.append("Pole 'numer telefonu' jest wymagane.")
        if nowy_kontakt["tel"] and not nowy_kontakt["tel"].isdigit():
            bledy.append("Numer telefonu może zawierać tylko cyfry.")
        if nowy_kontakt["email"] and not self.data_manager.czy_email(nowy_kontakt["email"]):
            bledy.append(f"Nieprawidłowy adres e-mail: {nowy_kontakt['email']}")
        if nowy_kontakt["kod"] and not nowy_kontakt["kod"].replace("-", "").isdigit():
            bledy.append("Kod pocztowy musi zawierać tylko cyfry i myślnik.")
        if nowy_kontakt["miasto"] and not nowy_kontakt["miasto"].isalpha():
            bledy.append("Miasto musi zawierać tylko litery.")

        if bledy:
            QMessageBox.warning(self, "Błędy", "\n".join(bledy))
            return

        self.data_manager.kontakty[wybrany] = nowy_kontakt
        self.data_manager.dane_zapis()

        self.tabela_wyniki.setItem(wybrany, 0, QTableWidgetItem(nowy_kontakt["imie"]))
        self.tabela_wyniki.setItem(wybrany, 1, QTableWidgetItem(nowy_kontakt["nazwisko"]))
        self.tabela_wyniki.setItem(wybrany, 2, QTableWidgetItem(nowy_kontakt["tel"]))
        self.tabela_wyniki.setItem(wybrany, 3, QTableWidgetItem(nowy_kontakt["email"]))
        self.tabela_wyniki.setItem(wybrany, 4, QTableWidgetItem(nowy_kontakt["ulica"]))
        self.tabela_wyniki.setItem(wybrany, 5, QTableWidgetItem(nowy_kontakt["miasto"]))
        self.tabela_wyniki.setItem(wybrany, 6, QTableWidgetItem(nowy_kontakt["kod"]))

        self.edytuj.close()
        QMessageBox.information(self, "Sukces", "Kontakt został pomyślnie zaktualizowany!")
