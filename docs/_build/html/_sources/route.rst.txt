Pakete: route
#############

Modul: recepe
=============

.. http:get:: /

    Rendert die Hauptseite.

    :resheader Content-Type: text/html; charset=utf8
    :statuscode 200: Hauptseite wurde erfolgreich geladen
    :statuscode 404: index.html wurde nicht gefunden

.. http:get:: /countries

    Liefert einee Liste mit allen verfügbaren Läandern.

    :resheader Content-Type: application/json
    :statuscode 200: Liste wurde erfolgreich geladen