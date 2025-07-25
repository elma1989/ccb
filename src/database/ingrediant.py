from typing import Any
from database import DataObject, Error, FKON
import re

class Ingrediant(DataObject):
    """
    Repräsentiert eine Zutat.

    :param name: Name der Zutat
    :param amount: Menge der Zutat (Standard: 0.0)
    :param unit: Einheit der Menge (Standard: "")
    :param id: Id der Zutat in der Datenbank (Standard: 0)
    """
    def __init__(self, name:str, amount:float=0.0, unit:str='', id:int=0) -> None:
        super().__init__()
        self.__name = name
        self.__amount = amount
        self.__unit = unit
        self.__id = id

    @property
    def name(self) -> str:
        ''':getter: Name der Zutat'''
        return self.__name
    
    @property
    def amount(self) -> float:
        """
        :getter: Menge
        """
        return self.__amount
    
    @property
    def unit(self) -> str:
        ''':getter: Einheit'''
        return self.__unit
    
    @property
    def id(self) -> int:
        ''':getter: Zutat-ID'''
        sql:str = 'SELECT igdt_id FROM ingrediant WHERE igdt_name = ?'

        if self.__id == 0:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(self.name,))
                    res = self.c.fetchone()
                    if res: self.__id = res[0]
            except Error as e: print(e)
            finally: self.close()

        return self.__id
    
    def __repr__(self) -> str:
        return self.name if self.amount == 0.0 else f'{self.name} ({self.amount} {self.unit})'
    
    def __eq__(self,other) -> bool:
        if not isinstance(other, Ingrediant): return False
        return self.name == other.name and self.amount == other.amount and self.unit == other.unit
    
    def exists(self) -> bool:
        """
        Prüft, ob eine Zutat bereits vohanden ist.

        :return: **True**, wenn die Zutat vorhanden ist
        """
        sql:str = 'SELECT igdt_name FROM ingrediant WHERE igdt_name = ?'
        found:bool = False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.name,))
                res = self.c.fetchone()
                if res: found = True
        except Error as e: print(e)
        finally: self.close()

        return found
    
    def add(self) -> int:
        """
        Fügt eine Zutat in die Datenbank ein.

        :return:
             | 0 - Erfolgreich
             | 1 - Name ungültig (muss mit Großbuchstaben beginnen)
             | 3 - Zutat bereits vorhanden
        """
        sql:str = 'INSERT INTO ingrediant VALUES(NULL, ?)'
        success:bool = False
        x = re.search('[A-Z][a-z]*', self.name)

        if not x: return 1
        if self.exists(): return 3

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.name,))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 1

    def remove(self) -> int:
        """
        Löscht einen Zutat.

        :return:
             | 0 - Erfolgreich
             | 1 - Zutat nicht gefunden
             | 2 - Zutat wird noch in mindestens einem Rezept verwendet

        .. important:: Eine Zutat kann nur gelöscht werden, wenn sie von keinen Rezept verwendet wird.
            Betroffene Rezepte müssen zuvor einzeln gelöscht werden.
        """
        sql:str = 'DELETE FROM ingrediant WHERE igdt_name = ?'
        success:bool = False

        if not self.exists(): return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql,(self.name,))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 2
    
    def to_dict(self) -> dict:
        """
        Liefert die Daten einer Zutat:

        :return: Name, Menge, Einheit, ID
        """
        outdict:dict[str,str|float] = {'name': self.name}
        if self.amount != 0.0:
            outdict['amount'] = self.amount
            outdict['unit'] = self.unit
        if self.id != 0: outdict['id'] = self.id
        return outdict