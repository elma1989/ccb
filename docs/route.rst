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

    Liefert einee Liste mit allen verfügbaren Ländern.

    :resheader Content-Type: application/json
    :statuscode 200: Liste wurde erfolgreich geladen

.. http:get:: /recepies

    Liefert eine Liste mit Rezepten aus einem Land

    :query string country: Kfz-Kennzeichen des zu suchenden Landes in der Datenbank
    :resheader Content-Type: application/json
    :statuscode 200: Rezepte wurden erfolgreich geladen
    :statuscode 400: Angabe des Landes fehlt
    :statuscode 404: Land nicht gefunden

.. http:get:: /recepies/(int:recepe_id)

    Liefet eine detailierte Informationen zu einem Rezept.

    :param int recepe_id: Id des Rezeptes
    :resheader Content-Type: application/json
    :statuscode 200: Rezept-Daten wurden erfolgreich geladen
    :statuscode 404: Rezept wurde nicht gefunden