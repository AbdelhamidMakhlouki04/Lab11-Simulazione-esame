from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.vertici=None
        self.archi=None
        self.peso=None
        self.grafo=None

    def get_all_genre(self):
        return DAO.get_all_genre()

    def get_vertici(self,genere):
        self.vertici=DAO.get_vertici(genere)

    def get_archi(self,genere):
        self.archi=DAO.get_archi(genere)

    def get_peso(self):
        peso={}
        p=DAO.get_peso()
        for i in p:
            peso[i.artist_id] = i.quantity
        self.peso=peso

    def crea_grafo(self):
        grafo=nx.DiGraph()
        self.get_peso()
        for i in self.vertici:
            grafo.add_node(i.artist_id)
        for i in self.archi:
            peso1=self.peso[i.artist_id1]
            peso2=self.peso[i.artist_id2]
            pesoTot=peso1+peso2
            if peso1>peso2:
                grafo.add_edge(i.artist_id1, i.artist_id2, weight=pesoTot)
            if peso1<peso2:
                grafo.add_edge(i.artist_id2, i.artist_id1, weight=pesoTot)
            if peso1==peso2:
                grafo.add_edge(i.artist_id1, i.artist_id2, weight=pesoTot)
                grafo.add_edge(i.artist_id2, i.artist_id1, weight=pesoTot)
        self.grafo=grafo

    def get_num_grafo(self):
        return len(self.grafo.nodes()),len(self.grafo.edges())