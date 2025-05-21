# Książka adresowa

**Książka adresowa** to prosta aplikacja do zarządzania kontaktami. Pozwala na dodawanie, wyszukiwanie oraz edytowanie kontaktów.

## Funkcje

- Dodawanie, edycja i usuwanie kontaktów
- Wyszukiwanie i filtrowanie listy kontaktów
- Statystyki: liczba kontaktów, najczęstsze imię i miasto
- Automatyczny backup danych do bazy SQLite

## Wymagania

- Python 3.8+
- PyQt6

## Uruchomienie

Aby uruchomić aplikację, wpisz w terminalu:
```bash
python main.py
```

## Pliki

- `main.py` – uruchamia aplikację
- `gui_main.py` – strona główna i nawigacja
- `gui_nowy_kontakt.py` – dodawanie kontaktu
- `gui_szukaj.py` – wyszukiwanie i edycja kontaktów
- `gui_statystyki.py` – statystyki kontaktów
- `data_manager.py` – obsługa danych i backupu
- `kontakty.json` – przykładowy plik z kontaktami (dane użytkownika)
- `backup.db` – baza danych do backupu
- `logo.svg` – ikona aplikacji

## Uwagi

- Program automatycznie przywraca dane z kopii zapasowej (`backup.db`), jeśli plik `kontakty.json` zostanie uszkodzony.
- Wszystkie dane są przechowywane lokalnie.

## Autor

Szymon Druszcz

---

**Miłego korzystania z aplikacji!**
