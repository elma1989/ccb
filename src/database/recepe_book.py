from database import Data, Recepe, Country, Error

class RecepeBook(Data):
    """
    Repräsentiert das Rezeptbuch, welches mehrere Rezepte veraltet.
    """
    def __init__(self):
        super().__init__()

    def get_recepe(self, id:int):
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
    
    def find(self, name:str, country: Country):
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