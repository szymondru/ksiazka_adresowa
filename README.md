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

- `ksiazka_aio.py` – główny plik aplikacji
- `kontakty.json` – plik z kontaktami (tworzy się automatycznie)
- `backup.db` – kopia zapasowa kontaktów (tworzy się automatycznie)
- `logo.svg` – ikona aplikacji

## Uwagi

- Program automatycznie przywraca dane z kopii zapasowej, jeśli plik `kontakty.json` zostanie uszkodzony.
- Wszystkie dane są przechowywane lokalnie.

## Autor

Szymon D

---

**Miłego korzystania z aplikacji!**
