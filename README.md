Evident Aplikacija za Radne Sate i Putni Nalog
Ovo je jednostavna web aplikacija za upravljanje radnim satima radnika i putnim nalozima. Aplikacija omogućava unos podataka o radnicima, izračunavanje ukupnih radnih sati i generisanje putnih naloga. Aplikacija je izgrađena pomoću Flask-a (Python web framework) i pokreće se lokalno na localhost:5000.

Karakteristike
Radni Sati: Omogućava unos podataka o radnicima i izračunavanje ukupnog broja radnih sati.
Putni Nalog: Omogućava kreiranje putnih naloga za radnike.
Generisanje PDF-a: Generiše PDF dokument za svaki putni nalog sa detaljima o radniku i putnom nalogu.

Preduslovi
Prije pokretanja aplikacije, potrebno je da imate instalirane sljedeće:
Python 3.x
pip (Python paket menadžer)
Flask (Python web framework)
Flask PDF biblioteka (npr. Flask-WeasyPrint ili ReportLab)
Instalacija

Kreiraj virtuelno okruženje (opcionalno, ali preporučeno):

python3 -m venv venv
source venv/bin/activate  # Na Windowsu koristite `venv\Scripts\activate`

Pokreni aplikaciju:
python app.py

Aplikacija će biti dostupna na http://localhost:5000.

Korištenje
Otvorite web preglednik i idite na http://localhost:5000.
Koristite ponuđene forme za unos podataka o radnicima i izračunavanje ukupnih radnih sati.
Generišite putne naloge i preuzmite odgovarajuće PDF fajlove.


Zavisnosti
Aplikacija zahtijeva sledeće Python pakete:
Flask
Flask-WeasyPrint (ili neka druga biblioteka za generisanje PDF-a)


