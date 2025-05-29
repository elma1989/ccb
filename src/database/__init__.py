DBPATH = '../ccb.db'
TABLEPATH = 'database/tables.sql'
FKON = 'PRAGMA foreign_keys = ON'

import os
from sqlite3 import Error
from .data import Data, DataObject
from .country import Country
from .ingrediant import Ingrediant
from .recepe import Recepe
from .recepe_book import RecepeBook

def indb():
    """
    Initialisiert die Datenbank.

    .. important:: Alle bisherigen Daten werden dabei gelöscht.
        Pyttests verwenden indb(). Daher sollten keine Pytests mehr durchgeführt werden sobald reale Daten existieren.
    """
    data = Data()

    if os.path.exists(DBPATH): os.remove(DBPATH)

    with open(TABLEPATH, 'r') as f:
        sql = f.read()

    try:
        data.connect()
        if data.con: data.con.executescript(sql)
    except Error as e: print(e)
    finally: data.close()