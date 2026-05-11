from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():  # seleziono tutto dalla tabella fermata
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"   # PRENDE TUTTE LE STAZIONI (NODI) POSSIBILI
        cursor.execute(query)
        for row in cursor:
            result.append(Fermata(**row))  # DB --> oggetti Fermata (python)
        cursor.close()
        conn.close()
        return result


# ========= ESISTE UNA CONNESSIONE DIRETTA TRA "u" E "v" ??? =================
    @staticmethod
    def hasConnexion(u:Fermata, v:Fermata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = (
            "SELECT * "
            "FROM connessione c "
            "WHERE c.id_stazP = %s "
            "AND c.id_stazA = %s"
        )
        # parametri --> id ! non l'oggetto
        cursor.execute(query, (u.id_fermata, v.id_fermata))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0  # True se trovo almeno 1 riga
                                # altrimenti False


    @staticmethod
    def getVicini(u:Fermata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = (
            "SELECT * "
            "FROM connessione c "
            "WHERE c.id_stazP = %s"
        )
        # tutti gli archi che partono da "u"

        cursor.execute(query, (u.id_fermata,)) # attenzione alla virgola
        for row in cursor:
            result.append(Connessione(**row))
            # ogni riga è un oggetto Connessione(id_stazP=1, id_stazA=2)
        cursor.close()
        conn.close()
        return result  # lista di connessioni uscenti da "u"



# ========= METODO USATO PER COSTRUIRE IL GRAFO IN MODO EFFICIENTE =============
    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione"
        # PRENDE TUTTE LE RIGHE DELLA TABELLA CONNESSIONE, cioò tutti gli archi del grafo
        # ogni oggetto rappresenta un arco del grafo
        # [
        #   Connessione(id_stazP=1, id_stazA=2),
        #   Connessione(id_stazP=2, id_stazA=3),
        #   Connessione(id_stazP=1, id_stazA=4),
        # ]
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    # ====================ALTERNATIVA PER CREARE GLI ARCHI PESATI ==============================
    @staticmethod
    def getAllEdgesPesati():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select c.id_stazP, c.id_stazA, count(*)as peso
                from connessione c
                group by c.id_stazP , c.id_stazA 
                order by peso desc"""
        # il risultato della query è diverso da Connessione.py
        cursor.execute(query)

        for row in cursor:
            result.append((row["id_stazP"], row["id_stazA"], row["peso"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdgesVelocita():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select c.id_stazP , c.id_stazA , max(l.velocita ) as v
                    from connessione c, linea l
                    where c.id_linea = l.id_linea 
                    group by c.id_stazP , c.id_stazA 
                    order by v asc 
                    """
        # il risultato della query è diverso da Connessione.py
        cursor.execute(query)

        for row in cursor:
            # IN UNA TUPLA DI TRE DATI
            result.append((row["id_stazP"], row["id_stazA"], row["v"]))
        cursor.close()
        conn.close()
        return result