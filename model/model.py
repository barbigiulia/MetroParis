from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() # riempita con tutte le fermate
        self._grafo = nx.DiGraph()
        self._idMapFermate = {}  #dizionario
        for  f in self._fermate:
            # interrogo il diz con questa chiave
            self._idMapFermate[f.id_fermata] = f

    def buildGraph(self):
        # instanzio il grafo
        # inizilializzato nel metodo __init__()

        # 1) pulisco
        self._grafo.clear()
        # 2) popolo il grafico con la lista delle fermate
        self._grafo.add_nodes_from(self._fermate)
        self.addedges2() # chiamo quello più efficiente

    def addedges(self):
        # 619^2 fermate (doppio ciclo) -> poco efficiente e lenta
        # prendo tutte le possibili coppie di fermate
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasConnexion(u,v): # se True
                    self._grafo.add_edge(u,v)

    # METODO PIU' EFFICIENTE
    def addedges2(self):
        # data una fermata, prendo quelle vicine
        for u in self._fermate:   # guardo i suoi vicini adiacenti
            for connessione in DAO.getVicini(u):
                v = self._idMapFermate[connessione.id_stazA]
                self._grafo.add_edge(u,v)

    def addedges3(self):
        all_edges = DAO.getAllEdges()
        for conn in all_edges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]



    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numArchi(self):
        return len(self._grafo.edges())


    @property
    def fermate(self):
        return self._fermate