from database import DataObject, Error, FKON

class Country(DataObject):
    """
    Repräsentiert ein Land.

    :param cs: Kfz-Kennzeichen
    :param name: Name des Landes (Standard: "")
    """
    def __init__(self, cs:str, name:str = "") -> None:
        super().__init__()
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

    def add(self) -> int:
        """
        Fügt ein neues Land in die Datenbank ein.

        :return:
             | 0 - Erfolgreich
             | 1 - Landdaten ungültig
             | 3 - Land bereits vorhanden
        """
        sql:str = 'INSERT INTO country VALUES(?,?)'
        success:bool = False

        if len(self.cs) < 1 or len(self.cs) > 3 or len(self.name) == 0: return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(self.cs, self.name))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 3
    
    def remove(self) -> int:
        """
        Löscht ein Land.

        :return:
             | 0 - Erfolgreich
             | 1 - Land nicht gefunden

        .. important:: Wird ein Land gelöscht, so werden alle Rezepte aus diesem Land mit gelöscht.
        """
        sql:str = 'DELETE FROM country WHERE cty_cs = ?'
        success:bool = False

        if not self.exists(): return 1

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(FKON)
                self.c.execute(sql,(self.cs,))
                self.con.commit()
                success = True
        except Error as e: print(e)
        finally: self.close()

        return 0 if success else 1

    def to_dict(self) -> dict[str,str]:
        """
        Liefert die Daten des Landes.

        :return: Kfz-Kennzeichen, ggf. Name des Landes
        """
        outdict = {'cs':self.cs}
        if len(self.name) > 0: outdict['name'] = self.name
        return outdict