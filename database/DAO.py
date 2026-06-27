from database.DB_connect import DBConnect
from model.classi import Genre,Vertici,Archi,Peso


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_genre():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                    SELECT DISTINCT g.GenreId , g.Name
                    FROM genre g
                    ORDER BY g.Name
                    """
            cursor.execute(query)
            for row in cursor:
                result.append(Genre(row["GenreId"], row["Name"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_vertici(genere):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                        SELECT DISTINCT a.ArtistId , a.Name
                        FROM artist a , album alb, track t
                        WHERE a.ArtistId = alb.ArtistId AND alb.AlbumId = t.AlbumId
                        AND t.GenreId = %s
                        """
            cursor.execute(query,(genere,))
            for row in cursor:
                result.append(Vertici(row["ArtistId"], row["Name"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_archi(genere):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                        WITH acquisto_cliente_artista AS (
                        SELECT DISTINCT c.CustomerId , a.ArtistId
                        FROM customer c , artist a , album alb , track t , invoiceline il , invoice i
                        WHERE c.CustomerId = i.CustomerId AND i.InvoiceId = il.InvoiceId AND
                        il.TrackId = t.TrackId AND t.AlbumId = alb.AlbumId AND alb.ArtistId = a.ArtistId
                        AND t.GenreId = %s
                        GROUP BY c.CustomerId, a.ArtistId
                        )
                        SELECT DISTINCT a1.ArtistId AS art1, a2.ArtistId AS art2
                        FROM  acquisto_cliente_artista a1 , acquisto_cliente_artista a2 
                        WHERE a1.ArtistId < a2.ArtistId AND a1.CustomerId = a2.CustomerId
                        """
            cursor.execute(query,(genere,))
            for row in cursor:
                result.append(Archi(row["art1"], row["art2"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_peso(genere):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                    SELECT DISTINCT a.ArtistId , SUM(il.quantity) AS tot
                    FROM artist a , album alb, track t , invoiceline il
                    WHERE  il.TrackId = t.TrackId AND t.AlbumId = alb.AlbumId AND 
                    alb.ArtistId = a.ArtistId AND t.GenreId = %s
                    GROUP BY a.ArtistId
                    """
            cursor.execute(query,(genere,))
            for row in cursor:
                result.append(Peso(row["ArtistId"],row["tot"]))
            cursor.close()
            cnx.close()
        return result
