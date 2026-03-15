# Ferdynand-2137

Bardzo ważny bot discordowy, którego jedynym i ostatecznym zadaniem jest celebrowanie najważniejszej minuty w ciągu doby.

## Działanie

Bot codziennie o godzinie **21:37** (czasu polskiego):
1. Wysyła trzykrotnie wiadomość tekstową z oznaczeniem skonfigurowanej roli.
2. Dołącza do wyznaczonego kanału głosowego.
3. Odtwarza strumień audio z serwisu YouTube (utwór "Wapiesz - hehe papież tańczy") dokładnie od 27. sekundy.
4. Po 60 sekundach automatycznie kończy transmisję i opuszcza kanał.

---

## Wymagania Systemowe

Aby Ferdynand mógł prawidłowo funkcjonować, system musi posiadać zainstalowane następujące komponenty:

* **Python 3.9+**: Wymagany ze względu na natywną obsługę stref czasowych (`zoneinfo`).
* **FFmpeg**: Krytyczny dekoder multimedialny. 
    * **Windows**: Plik `ffmpeg.exe` musi zostać dodany do systemowej zmiennej **PATH**.
    * **Linux**: Instalacja komendą `sudo apt install ffmpeg`.

---

## Instalacja i Konfiguracja

### 1. Pobranie bibliotek
Po sklonowaniu repozytorium zainstaluj wymagane zależności Pythona:

```BASH
pip install -r requirements.txt
```

### 2. Konfiguracja zmiennych (.env)
W głównym folderze projektu stwórz plik o nazwie .env. Plik ten jest ignorowany przez system Git dla zachowania bezpieczeństwa Twoich danych. Wypełnij go według poniższego wzoru:
```
DISCORD_TOKEN=twoj token bota
TEXT_CHANNEL_ID=id kanalu tekstowego
VOICE_CHANNEL_ID=id kanalu glosowego
ROLE_ID=id roli do oznaczenia
```

### 3. Uruchamianie
W celu uruchomienia bota wpisz w terminalu:
```BASH
python Ferdynand.py
```
