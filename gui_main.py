from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QToolBar, QMessageBox, QWidget, QApplication, QLabel, QPushButton
from PyQt6.QtGui import QPalette, QAction
from PyQt6.QtCore import Qt
from data_manager import DataManager
from gui_nowy_kontakt import NowyKontakt
from gui_szukaj import Szukaj
from gui_statystyki import Statystyki



class ProgramGlowny(QMainWindow):
    """ Strona główna aplikacji """

    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.nowy_kontakt = None
        self.szukaj = None
        self.statystyki = None
        self.central_widget = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Książka adresowa")
        self.setGeometry(300, 300, 400, 400)

        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.menu()
        self.do_program_glowny()

    def menu(self):
        fmenu = self.menuBar().addMenu("Program")
        fmenu.addAction(QAction("O programie ", self,
                                    triggered=lambda: QMessageBox.information(self, "O programie",
                                    "Książka adresowa \nAutor: Szymon D\n")))
        fmenu.addSeparator()
        fmenu.addAction(QAction("Zamknij ", self, shortcut="Ctrl+Q", triggered=self.close))

        akcja_menu = self.menuBar().addMenu("Nawigacja")
        akcja_menu.addAction(QAction("Strona główna ", self, triggered=self.do_program_glowny))
        akcja_menu.addAction(QAction("Dodaj kontakt ", self, triggered=self.do_nowy_kontakt))
        akcja_menu.addAction(QAction("Szukaj kontaktów ", self, triggered=self.do_szukaj))
        akcja_menu.addAction(QAction("Statystyki ", self, triggered=self.do_statystyki))

    def do_program_glowny(self):
        self.central_widget = QWidget()
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Sprawdzenie czy tryb ciemny/jasny
        kolorki = QApplication.palette()
        czy_ciemny_motyw = kolorki.color(QPalette.ColorRole.WindowText).lightness() > (
                         kolorki.color(QPalette.ColorRole.Window).lightness())
        kolor_tekstu1 = "#FFFFFF" if czy_ciemny_motyw else "#000000"
        kolor_tekstu2 = "#AAAAAA" if czy_ciemny_motyw else "#555555"

        # Okno powitalne
        witaj = QLabel("Witaj w Książce adresowej!")
        witaj.setAlignment(Qt.AlignmentFlag.AlignCenter)
        witaj.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {kolor_tekstu1};")
        layout.addWidget(witaj)

        opis = QLabel(
            "Zarządzaj swoimi kontaktami w prosty sposób.\n"
            "Użyj menu, aby dodać, wyszukać lub zobaczyć statystyki kontaktów."
        )
        opis.setAlignment(Qt.AlignmentFlag.AlignCenter)
        opis.setStyleSheet(f"font-size: 14px; color: {kolor_tekstu2};")
        layout.addWidget(opis)

        # Przyciski
        przycisk_styl = QVBoxLayout()

        przycisk_dodaj = QPushButton("Dodaj kontakt")
        przycisk_dodaj.setStyleSheet("font-size: 14px; padding: 8px;")
        przycisk_dodaj.clicked.connect(self.do_nowy_kontakt)
        przycisk_styl.addWidget(przycisk_dodaj)

        przycisk_szukaj = QPushButton("Szukaj kontaktów")
        przycisk_szukaj.setStyleSheet("font-size: 14px; padding: 8px;")
        przycisk_szukaj.clicked.connect(self.do_szukaj)
        przycisk_styl.addWidget(przycisk_szukaj)

        przycisk_statystyki = QPushButton("Statystyki")
        przycisk_statystyki.setStyleSheet("font-size: 14px; padding: 8px;")
        przycisk_statystyki.clicked.connect(self.do_statystyki)
        przycisk_styl.addWidget(przycisk_statystyki)

        layout.addLayout(przycisk_styl)

        self.setCentralWidget(self.central_widget)

    def do_nowy_kontakt(self):
        self.nowy_kontakt = NowyKontakt(self.data_manager)
        self.nowy_kontakt.setWindowTitle("Dodaj nowy kontakt")
        self.nowy_kontakt.show()

    def do_szukaj(self):
        self.szukaj = Szukaj(self.data_manager)
        self.szukaj.setWindowTitle("Szukaj kontaktów")
        self.szukaj.show()

    def do_statystyki(self):
        self.statystyki = Statystyki(self.data_manager)
        self.statystyki.setWindowTitle("Statystyki")
        self.statystyki.show()

