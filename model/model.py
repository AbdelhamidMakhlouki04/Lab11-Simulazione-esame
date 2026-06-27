import copy

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

    def trova_nome_vertice(self,id):
        for i in self.vertici:
            if id==i.artist_id:
                return i.artist_name

    def get_archi(self,genere):
        self.archi=DAO.get_archi(genere)

    def get_peso(self,genere):
        peso={}
        p=DAO.get_peso(genere)
        for i in p:
            peso[i.artist_id] = i.quantity
        self.peso=peso

    def crea_grafo(self):
        grafo=nx.DiGraph()
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

    def get_maggior_influente(self):
        best = None
        best_score = float("-inf")

        for n in self.grafo.nodes():
            out_w = sum(self.grafo[n][v]["weight"] for _, v in self.grafo.out_edges(n))
            in_w = sum(self.grafo[u][n]["weight"] for u, _ in self.grafo.in_edges(n))
            score = out_w - in_w
            if score > best_score:
                best_score = score
                best = n

        nome=self.trova_nome_vertice(best)
        return nome,best_score

    def get_top_5(self):
        top5 = sorted(
            self.grafo.edges(data=True),
            key=lambda x: x[2]["weight"],
            reverse=True
        )[:5]
        lista_finale=[]
        for i in top5:
            nome1=self.trova_nome_vertice(i[0])
            nome2=self.trova_nome_vertice(i[1])
            lista_finale.append([nome1,nome2,i[2]["weight"]])
        return lista_finale




    def getPesoArco(self, u, v):
        return self.grafo[u][v]["weight"]


    def score(self, parziale):
        score = 0
        for i in range(len(parziale) - 1):
            score += self.grafo[parziale[i]][parziale[i + 1]]["weight"]
        return score


    def getPath(self, v0):
    # Inizializzo le variabili generiche
        parziale = [v0]
        self._bestPath = []
        self._costoCammino = -1

    # Esploriamo i vicini del nodo di partenza v0
    # Con grafo diretto --> successors()
    # Con grafo non diretto --> neighbors
        for v in self.grafo.successors(v0):
            parziale.append(v)
        # Avvio la ricorsione
            self.ricorsione(parziale)
        # Effettuo il meccanismo di backtracking: rimuoviamo il vicino per trovare le altre strade del ciclo
            parziale.pop()
        return self._bestPath, self._costoCammino


    def ricorsione(self, parziale):
    # Verifico se la soluzione parziale è meglio del BestCase utilizzando la funzione score
        punteggio_attuale = self.score(parziale)
        if punteggio_attuale > self._costoCammino:
            self._bestPath = copy.deepcopy(parziale)
            self._costoCammino = punteggio_attuale

    # Verifico quindi se ha senso continuare ad andare avanti con la ricerca di un cammino ottimale - Nel caso ci
    # fossero vincoli di terminazione

    # Effettuo quindi il mio meccanismo di ricorsione per lavorare sul nodo successivo
        nodo_corrente = parziale[-1]
    # Recupero i vicini dell'ultimo modo inserito all'interno della mia lista parziale
        for v in self.grafo.successors(nodo_corrente):
            if v not in parziale:
            # verifico che il peso del potenziale arco che andremo ad aggiungere sia maggiore del precedente
                pesoE = self.grafo[nodo_corrente][v]["weight"]
                nodo_precedente = parziale[-2]
                pesoP = self.grafo[nodo_precedente][nodo_corrente]["weight"]
                if pesoE > pesoP:
                    parziale.append(v)
                    self.ricorsione(parziale)
                    parziale.pop()


