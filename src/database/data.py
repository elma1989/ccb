from sqlite3 import Connection, Cursor, connect
from database import DBPATH, Error
from abc import ABC, abstractmethod

class Data:
    """
    Stellt die Datenbank zur Verfügung.
    """
    def __init__(self) -> None:
        self.__con: Connection|None = None
        self.__c: Cursor|None = None

    @property
    def con(self) -> Connection|None:
        ''':getter: Datenbankverbindung'''
        return self.__con
    
    @property
    def c(self) -> Cursor|None:
        ''':getter: Datenbankzeiger'''
        return self.__c
    
    def connect(self) -> None:
        '''Stellt eine Verbindung zur Datenbank her.'''
        if not self.con:
            try:
                self.__con = connect(DBPATH)
                if self.con: self.__c = self.con.cursor()
            except Error as e: print(e)

    def close(self) -> None:
        '''Trennt die Datenbankverbindung wieder'''
        if self.con and self.c:
            self.c.close()
            self.con.close()
            self.__c = None
            self.__con = None