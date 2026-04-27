from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.fermata import Fermata


class DAO():

    @staticmethod
    def getAllFermate():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM fermata"
        cursor.execute(query)

        for row in cursor:
            result.append(Fermata(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def hasConnexion(u:Fermata, v:Fermata):

        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * "
                 "FROM connessione c"
                 "WHERE c.id_stazP =%s"
                 "AND c.id_stazA =%s")

        cursor.execute(query, (u.id_fermata, v.id_fermata))

        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return len(result) > 0  # True , altrimenti False


    @staticmethod
    def getVicini(u:Fermata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = ("SELECT * "
                 "FROM connessione c"
                 "WHERE c.id_stazP =%s")

        cursor.execute(query, (u.id_fermata,)) # occhio alla virgola
        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM connessione"
        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        conn.close()
        return result