# bookandfly
Projekt Security by Design
##Config 
config_example.py bietet eine beispielskonfiguration die ergänzt werden muss.
Zertifikat und Schlüssel kann mit
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
generiert werden.