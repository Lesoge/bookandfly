# bookandfly
Projekt Security by Design
# Setup
Um den Webserver zu starten muss eine Postgres Datenbank erstellt werden
und in der config konfiguriert werden(Mehr dazu unter config). Das File db_setup.py fügt standard
Daten in die Datenbank ein. Zudem wird der Nutzer aufgefordert ein Admin Account
zu erstellen. Hier kann ein schwaches Passwort gewählt werden. Beim ersten Login
in die Weboberfläche muss ein Passwort, dass den Richtlinien entspricht gewählt werden.

Es wird ein Zertifikat(.pem) und ein Schlüssel(.pem) im root ordner benötigt. Dazu kann folgender
Befehl 'penssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365' benutzt werden.
Um die Requirements zu installieren pip3 install -r requirements.txt ausführen
Die Anwendung kann mit python app.py gestartet werden
#Config
Die config muss im Ordner Config erstellt werden, mit dem namen config.py
config_example.py bietet eine Beispielskonfiguration die ergänzt werden muss.
Folgende Parameter müssen konfiguriert werden
dbname: String: Name der Datenbank
dbuser: String: Name eines Users der Datenbank
dbpassword: String: Password des Users der Datenbank
SQLALCHEMY_ECHO: String: Boolean Falls True werden die Datenbank SQL Befehle in die Konsole geschrieben
SQLALCHEMY_TRACK_MODIFICATIONS: Boolean: False da nicht benötigt
SECRET_KEY: String: Geheimer Schlüssel, der für die Signatur der Session benötigt wird.
Mit 'python scripts/secret_generator.py' kann ein sicherer Schlüssel generiert werden.
DEBUG: Boolean: Falls True wird Flask im Debug modus gestartet
SESSION_COOKIE_SECURE: Boolean: Falls True werden cookies nur über HTTPS gesendet
Zertifikat und Schlüssel kann mit
SECURITY_PASSWORD_HASH: String: Algorithmus der zum hashen von passwörtern benutzt werden soll
SECURITY_PASSWORD_SALT: String: Salz für die passwörter. Mit 'python scripts/secret_generator.py' kann ein sicherer Schlüssel generiert werden.
SECURITY_PASSWORD_LENGTH_MIN: Int: Mindestlänge des Passworts
SECURITY_PASSWORD_COMPLEXITY_CHECKER: string: definiert ein Modul um die Passwortkomplexität zu testen. 
Einzig verfügbares Modul
ist 'zxcvbn'
SECURITY_PASSWORD_CHECK_BREACHED:  String: Stellt ein OB die haveibeenpwnd Api abgefragt werden soll um zu überprüfen, ob die Passwörter bereits gebrochen sind

CERT_PATH: String: Name der Datei des Zertifikats
KEY_PATH: String: Name der Datei des Schlüssels

LOGIN_ATTEMPTS_BEFORE_LOCK: int: Anzahl der Login versuche bevor account gesperrt wird.
APP_IP: String: IP-Adresse auf die, die App laufen soll

#Aufbau
config/ Ordner für Config Dateien
logs/ Ordner für Logs
routes/ Ordner mit Dateien für die Routen der App
static/ Ordner für Dateien fürs front-end
scripts/ Scripts die Beim setup Hilfreich sein können
#Routen
Neben den Files des Ordners routes definierten Routen existieren noch Routen
für die Admin verwaltung unter /admin
