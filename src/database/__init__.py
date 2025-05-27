DBPATH = '../ccb.db'
TABLEPATH = 'database/tables.sql'

import os
from sqlite3 import Error
from .data import Data

def indb():
    """
    Initialisiert die Datenbank.

    .. important:: Alle bisherigen Daten werden dabei gelöscht.
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