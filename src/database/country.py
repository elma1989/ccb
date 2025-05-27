from database import DataObject, Error

class Country(DataObject):
    """
    Repräsentiert ein Land.

    :param cs: Kfz-Kennzeichen
    :param name: Name des Landes (Standard: "")
    """
    def __init__(self, cs:str, name:str = "") -> None:
        self.__cs = cs.upper()
        self.__name = name

    @property
    def cs(self) -> str:
        ''':getter: Kfz-Kennzeichen'''
        return self.__cs
    
    @property
    def name(self) -> str:
        ''':getter: Landname'''
        sql:str = 'SELECT cty_name FROM country WHERE cty_cs = ?'

        if len(self.__name) == 0:
            try:
                self.connect()
                if self.con and self.c:
                    self.c.execute(sql,(self.cs,))
                    res = self.c.fetchone()
                    if res: self.__name = res[0]
            except Error as e: print(e)
            finally: self.close()

        return self.__name
    
    def __repr__(self) -> str: return self.cs

    def __eq__(self, other) -> bool:
        if not isinstance(other, Country): return False
        return self.cs == other.cs
    
    def exists(self) -> bool:
        """
        Prüft, ob ein Land vorhanden ist.

        :return: **True**, wenn das Land verhanden ist
        """
        sql:str = 'SELECT cty_cs FROM country WHERE cty_cs = ?'
        found:bool = False

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.cs,))
                res = self.c.fetchone()
                if res: found = True
        except Error as e: print(e)
        finally: self.close()

        return found