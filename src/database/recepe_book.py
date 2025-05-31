from database import Data, Recepe, Country, Error

class RecepeBook(Data):
    """
    Repräsentiert das Rezeptbuch, welches mehrere Rezepte verwaltet.
    """
    def __init__(self):
        super().__init__()

    def countries(self) -> list[Country]:
        """
        Liefert eine Liste mit allen verfügbaren Ländern.
        """
        sql:str = 'SELECT cty_cs, cty_name FROM country ORDER BY cty_name'
        countries = []

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql)
                res = self.c.fetchall()
                countries = [Country(row[0], row[1]) for row in res]
        except Error as e: print(e)
        
        return countries

    def get_recepe(self, id:int) -> Recepe|None:
        """
        Liefert ein Rezept aus einer id.

        :param id: ID des Rezeptes
        :return: Instanz des Rezeptes, **None**, wenn kein Rezept gefunden wurde
        """
        sql:str = 'SELECT rcp_name, cty_cs, rcp_preparation FROM recepe WHERE rcp_id = ?'
        recepe:Recepe|None = None

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(id,))
                res = self.c.fetchone()
                if res: recepe = Recepe(res[0], Country(res[1]), id, res[2]) if res[2] else Recepe(res[0], Country(res[1]), id)
        except Error as e: print(e)
        finally: self.close()

        return recepe
    
    def find(self, name:str, country: Country) -> Recepe|None:
        """
        Sucht ein Rezept mit dem Namen und dem Land.

        :param name: Name des Rezeptes
        :param country: Ursprungsland des Rezeptes
        :return: Instanz des gefunden Rezeptes, **None**, wenn kein passendes Rezept gefunden wurde
        """
        sql:str = 'SELECT rcp_id, rcp_preparation FROM recepe WHERE rcp_name = ? AND cty_cs = ?'
        recepe:Recepe|None = None

        if not isinstance(country, Country) or not country.exists(): return None

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(name, country.cs))
                res = self.c.fetchone()
                if res: recepe = Recepe(name, country, res[0], res[1]) if res[1] else Recepe(name, country, res[0])
        except Error as e: print(e)
        finally: self.close()
        
        return recepe

    def recepies(self, country:Country) -> list[Recepe]|None:
        """
        Sucht alle Rezepte aus einem Land.

        :param country: Land aus dem die Rezepte stammen
        :return: Rezepteliste aus dem jeweiligen Land, **None**, wenn das Land nicht vorhanden ist
        """
        sql:str = 'SELECT rcp_name, rcp_id FROM recepe WHERE cty_cs = ? ORDER BY rcp_name'
        recepies = []

        if not isinstance(country, Country) or not country.exists():return None

        try:
            self.connect()
            if self.con and self.c:
                self.c.execute(sql,(country.cs,))
                res = self.c.fetchall()
                recepies = [Recepe(row[0], country, row[1]) for row in res]
        except Error as e: print(e)
        finally: self.close()

        return recepies