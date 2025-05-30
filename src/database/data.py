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

class DataObject(Data, ABC):
    """
    Repräsentiert eine Datenbank-Entität.
    """
    def __init__(self):
        Data.__init__(self)

    @abstractmethod
    def exists(self) -> bool:
        """
        Prüft, ob ein Objekt existiert.

        :return: **True**, wenn es vorhanden ist
        """
        pass

    @abstractmethod
    def add(self) -> int:
        """
        Fügt ein Objekt in die Datenbank ein.

        :return:
             | 0 - Erfolgreich
             | 1 - Objekt ungültig
             | 2 - Referenzen in Objekt nicht gefunden
             | 3 - Objekt bereits vorhanden
        """
        pass

    @abstractmethod
    def remove(self) -> int:
        """
        Löscht ein Objekt.

        :return:
             | 0 - Erfolgreich
             | 1 - Objekt nicht gefunden
             | 2 - Noch Referenzen vorhanden
        """
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Liefert die wichtigsten Daten eines Objektes.

        :return: Wörterbuch des jeweiligen Objektes.
        """
        pass