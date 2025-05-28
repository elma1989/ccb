from database import DataObject, Error

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
    def amount(self) -> tuple[float,str]:
        """
        :getter: Menge
        :return:
            amount[0] - Anzahl der Einheiten
            amount[1] - Einheit        
        """
        return (self.__amount, self.__unit)
    
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
        return self.name if self.amount[0] == 0.0 else f'{self.name} ({self.amount[0]} {self.amount[1]})'
    
    def __eq__(self,other) -> bool:
        if not isinstance(other, Ingrediant): return False
        return self.name == other.name and self.amount[0] == other.amount[0] and self.amount[1] == other.amount[1]
    
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