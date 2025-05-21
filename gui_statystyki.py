from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel



class Statystyki(QWidget):
    """ Funkcjonalność: Statystyki """

    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle("Statystyki")
        self.setGeometry(300, 300, 400, 300)

        self.stats_label = QLabel("Statystyki:")
        layout.addWidget(self.stats_label)

        self.statystyka()

    def statystyka(self):
        kontakty = self.data_manager.kontakty

        kontakty_liczba = len(kontakty)

        miasta_liczba = {}
        for entry in kontakty:
            miasto = entry.get('miasto', 'Nieznane')
            miasta_liczba[miasto] = miasta_liczba.get(miasto, 0) + 1

        miasto_najczestsze = max(miasta_liczba, key=miasta_liczba.get) if miasta_liczba else "Brak danych"

        imiona_liczba = {}
        for entry in kontakty:
            imie = entry.get('imie', 'Nieznane')
            imiona_liczba[imie] = imiona_liczba.get(imie, 0) + 1

        imie_najczestsze = max(imiona_liczba, key=imiona_liczba.get) if imiona_liczba else "Brak danych"

        statystyka_tekst = (
            f"Statystyki:\n\n"
            f"Łączna liczba kontaktów: {kontakty_liczba}\n"
            f"Najczęściej występujące miasto: {miasto_najczestsze} ({miasta_liczba.get(miasto_najczestsze, 0)} kontaktów)\n"
            f"Najczęściej występujące imię: {imie_najczestsze} ({imiona_liczba.get(imie_najczestsze, 0)} razy)"
        )

        self.stats_label.setText(statystyka_tekst)
