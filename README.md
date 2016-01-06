#nodes_json_api

Das perl-Script filtert eine vorhandene nodes.json des meshviewers anhand von URL-Parametern.
Die Filter können kombiniert werden. Die URL zur nodes.json muss im Script gesetzt werden und ist default auf: http://localhost:8078/nodes.json

Vorraussetzungen sind folgende perl-Module:
JSON
LWP::UserAgent
CGI
CGI::Carp
Data::Printer

Das CGI Modul des jeweiligen Webservers muss aktiviert sein.

Aktuell verfügbare Filter und ein Beispiel findet man mit dem Aufruf /?filter=list

