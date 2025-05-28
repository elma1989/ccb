import re
from database import DataObject, Error, Country, Ingrediant, FKON

class Recepe(DataObject):
    """
    Repräsentiert ein Rezept.

    :param name: Name des Rezeptes
    :param country: Land, aus dem das Rezept stammt
    :param id: ID in der Datenbank (Standard: 0)
    :param preparation: Zubereitungsanleitung (Standard: "")
    :ivar ingrediants: Zutatenliste
    :type ingrediants: list[Ingrediant]
    """
    def __init__(self, name:str, country:Country, id:int=0, preparation:str=''):
        super().__init__()
        self.__name = name
        self.__country: Country|None = country if isinstance(country, Country) and country.exists() else None
        self.__id = id
        self.__preparation = preparation
        self.__ingrediants:list[Ingrediant] = []

    @property
    def name(self) -> str:
        ''':getter: Name des Rezeptes'''
        return self.__name
    
    @property
    def country(self) -> Country|None:
        """
        :getter: Urprungsland des Rezeptes
        :return: Instanz des Landes, **None**, wenn das Land nicht vorhanden ist.
        """
        return self.__country
    
    @property
    def id(self) -> int:
        ''':getter: ID des Rezeptes'''
        sql:str = 'SELECT rcp_id FROM recepe WHERE rcp_name = ? AND cty_cs = ?'

        if self.__id == 0 and self.country:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(self.name))
                    res = self.c.fetchone()
                    if res: self.__id = res[0]
            except Error as e: print(e)
            finally: self.close()
        
        return self.__id
    
    @property
    def preparation(self) -> str:
        """
        Verwaltet die Zubereitung.

        :getter: Liefert die Zubereitungsanleitung.
        :setter: Speichert die Zubereittungsanleitung ab.
        """
        return self.__preparation
    
    @preparation.setter
    def preparation(self, manuel:str) -> None:
        sql:str = 'UPDATE recepe SET rcp_preparation = ? WHERE rcp_id = ?'
        
        if self.id != 0:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(manuel, self.id))
                    self.con.commit()
                    self.__preparation = manuel
            except Error as e: print(e)
            finally: self.close()

    @property
    def ingrediants(self) -> list[Ingrediant]:
        ''':getter: Liefert die Zutatenliste eines Rezeptes'''
        sql:str = """
            SELECT i.igdt_name, r.igdt_amount, r.igdt_unit, i.igdt_id
            FROM recepe_ingrediant r JOIN ingrediant i ON r.igdt_id = i.igdt_id
            WHERE rcp_id = ?
            ORDER BY i.igdt_name"""
        
        if self.id != 0:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(self.id,))
                    res = self.c.fetchall()
                    self.__ingrediants = [Ingrediant(row[0], row[1], row[2], row[3]) for row in res]
            except Error as e: print(e)
            finally: self.close()

        return self.__ingrediants
    
    def __repr__(self) -> str: return f'{self.name} ({self.country.cs})' if self.country else self.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, Recepe): return False
        return self.name == other.name and self.country == other.country
    
    def exists(self) -> bool:
        """
        Prüft, ob ein Recept vorhanden ist.

        :return: **True**, wenn das Rezept vorhanden ist
        """
        sql:str = 'SELECT rcp_id FROM recepe WHERE rcp_name = ? AND cty_cs = ?'
        found:bool = False

        if not self.country: return False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.name, self.country.cs))
                res = self.c.fetchone()
                if res: found = True
        except Error as e: print(e)
        finally: self.close()

        return found

    def add(self) -> int:
        """
        Fügt ein neues Rezept in die Datenkbank ein.

        :return:
             | 0 - Erfolgeich
             | 1 - Name ungültig (musss mit Großbuchstaben beginnen)
             | 2 - Land nicht gefuden
             | 3 - Recept bereits vorhanden
        """
        sql:str = 'INSERT INTO recepe VALUES(NULL,?,NULL,?)'
        success:bool = False
        x = re.search('^[A-Z][a-z]*', self.name)

        if not x: return 1
        if not self.country: return 2
        if self.exists(): return 3

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql,(self.name, self.country.cs))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 1

    def remove(self) -> int:
        return 1

    def to_dict(self) -> dict[str,str|int]:
        return {}