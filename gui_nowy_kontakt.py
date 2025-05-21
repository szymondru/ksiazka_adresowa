from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from data_manager import DataManager



class NowyKontakt(QWidget):
    """ Dodawanie nowego kontaktu """

    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.edytuj = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.setLayout(layout)
        self.setWindowTitle("Nowy kontakt")
        self.setGeometry(300, 300, 400, 250)

        # Wprowadzenie danych
        self.imie_in = QLineEdit(self)
        self.imie_in.setPlaceholderText("imię")
        layout.addWidget(self.imie_in)

        self.nazwisko_in = QLineEdit(self)
        self.nazwisko_in.setPlaceholderText("nazwisko")
        layout.addWidget(self.nazwisko_in)

        self.tel_in = QLineEdit(self)
        self.tel_in.setPlaceholderText("numer telefonu")
        layout.addWidget(self.tel_in)

        self.email_in = QLineEdit(self)
        self.email_in.setPlaceholderText("e-mail")
        layout.addWidget(self.email_in)

        self.ulica_in = QLineEdit(self)
        self.ulica_in.setPlaceholderText("ulica")
        layout.addWidget(self.ulica_in)

        self.miasto_in = QLineEdit(self)
        self.miasto_in.setPlaceholderText("miasto")
        layout.addWidget(self.miasto_in)

        self.kod_in = QLineEdit(self)
        self.kod_in.setPlaceholderText("kod pocztowy")
        layout.addWidget(self.kod_in)

        # Przycisk zapisz
        self.przycisk_zapisz = QPushButton("Zapisz nowy kontakt", self)
        self.przycisk_zapisz.clicked.connect(self.dane_konwersja)
        layout.addWidget(self.przycisk_zapisz)

    # Dane
    def dane_konwersja(self):
        imie = self.imie_in.text().strip()
        nazwisko = self.nazwisko_in.text().strip()
        tel = self.tel_in.text().strip()
        email = self.email_in.text().strip()
        ulica = self.ulica_in.text().strip()
        miasto = self.miasto_in.text().strip()
        kod = self.kod_in.text().strip()

        for pole in [self.imie_in, self.nazwisko_in, self.tel_in, self.email_in,
                     self.ulica_in, self.miasto_in, self.kod_in]:
            pole.setStyleSheet("")

        bledy = []

        # Sprawdzenie duplikatu kontaktu
        for entry in self.data_manager.kontakty:
            if (entry['imie'].lower() == imie.lower() and
                entry['nazwisko'].lower() == nazwisko.lower() and
                entry['miasto'] == miasto.lower() and
                entry['ulica'] == ulica.lower()):
                QMessageBox.warning(self, "Błąd", "Ta osoba już istnieje w bazie danych.")
                return

        # Sprawdzenie wymaganych danych
        if not imie:
            self.imie_in.setStyleSheet("border: 1px solid red;")
            bledy.append("Pole 'imię' jest wymagane.")
        if not nazwisko:
            self.nazwisko_in.setStyleSheet("border: 1px solid red;")
            bledy.append("Pole 'nazwisko' jest wymagane.")
        if not tel:
            self.tel_in.setStyleSheet("border: 1px solid red;")
            bledy.append("Pole 'numer telefonu' jest wymagane.")
        if not ulica:
            self.ulica_in.setStyleSheet("border: 1px solid red;")
            bledy.append("Pole 'ulica' jest wymagane.")
        if not miasto:
            self.miasto_in.setStyleSheet("border: 1px solid red;")
            bledy.append("Pole 'miasto' jest wymagane.")

        if tel and not tel.isdigit():
            self.tel_in.setStyleSheet("border: 1px solid red;")
            bledy.append("Numer telefonu może zawierać tylko cyfry.")

        if email and not self.data_manager.czy_email(email):
            self.email_in.setStyleSheet("border: 1px solid red;")
            bledy.append(f"Nieprawidłowy adres e-mail: {email}")

        if kod and not kod.replace("-", "").isdigit():
            self.kod_in.setStyleSheet("border: 1px solid red;")
            bledy.append("Kod pocztowy musi zawierać tylko cyfry i myślnik.")

        if miasto and not miasto.isalpha():
            self.miasto_in.setStyleSheet("border: 1px solid red;")
            bledy.append("Miasto musi zawierać tylko litery.")

        # Okno z błędami
        if bledy:
            QMessageBox.warning(self, "Błędy", "\n".join(bledy))
            return

        for pole in [self.imie_in, self.nazwisko_in, self.tel_in, self.email_in,
                 self.ulica_in, self.miasto_in, self.kod_in]:
            pole.setStyleSheet("")

        # Zapis danych
        self.data_manager.kontakty.append({
            "imie": imie, "nazwisko": nazwisko, "tel": tel,
            "email": email, "ulica": ulica, "miasto": miasto, "kod": kod
        })
        self.data_manager.dane_zapis()
        QMessageBox.information(self, "Sukces", "Adres zapisano pomyślnie!")

        # Czyszczenie pól
        for pole_tekst in [self.imie_in, self.nazwisko_in, self.tel_in, self.email_in,
                             self.ulica_in, self.miasto_in, self.kod_in]:
            pole_tekst.clear()
