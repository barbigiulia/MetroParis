from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() # riempita con tutte le fermate
        self._grafo = nx.DiGraph()  # istanza del Grafo diretto
        self._idMapFermate = {}  #dizionario
        # PER RECUPERARE L'OGGETTO DATO L'ID (in questo caso
        # la chiave primaria della tabella)
        for  f in self._fermate:
            # interrogo il diz con questa chiave
            self._idMapFermate[f.id_fermata] = f

    def getBFSNodesFromEdges(self, source):
        # parto dal nodo source
        # esploro con la logica bread first
        archi = nx.bfs_edges(self._grafo, source)
        nodiBFS = [source]
        for u, v in archi:
            # u è il nodo da cui parto
            nodiBFS.append(v)
        return nodiBFS


    def getBFSNodesFromTree(self, source):
        # chiede l'albero di visita
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi


    def getDFSNodesFromTree(self, source):
        # chiede l'albero di visita
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi


    def getDFSNodesFromEdges(self, source):
        # parto dal nodo source
        # esploro con la logica bread first
        archi = nx.dfs_edges(self._grafo, source)
        nodiDFS = []
        for u, v in nodiDFS:
            # u è il nodo da cui parto
            nodiDFS.append(v)
        return nodiDFS # stessi identici elementi, cambia solo l'ORDINE!



    def buildGraph(self):
        # instanzio il grafo
        # inizilializzato nel metodo __init__()
        # 1) pulisco
        self._grafo.clear()
        # 2) popolo il grafico con la lista delle fermate
        self._grafo.add_nodes_from(self._fermate) # aggiungo nodi
        self.addedges3() # aggiungo gli archi (metodo migliore)

# ==========================================================================

    # 1) metodo INEFFICIENTE --> lento
    #  faccio una query per ogni singolo arco (aggiungo 1 arco alla volta)
    # quando uso questa implementazione?  Quando i GRAFI SONO PICCOLI !!!!
    def addedges(self):
        # 619^2 fermate (doppio ciclo) -> poco efficiente e lenta
        # prendo tutte le possibili coppie di fermate
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasConnexion(u,v): # se True
                    self._grafo.add_edge(u,v)

    # 2) METODO PIU' EFFICIENTE del primo
    def addedges2(self):
        self._grafo.clear_edges()
        # data una fermata, prendo quelle vicine
        for u in self._fermate:   # guardo i suoi vicini adiacenti
            for connessione in DAO.getVicini(u):
                v = self._idMapFermate[connessione.id_stazA]
                self._grafo.add_edge(u,v)

    # 3)  MIGLIORE !!!
    def addedges3(self):
        self._grafo.clear_edges()
        all_edges = DAO.getAllEdges()
        for conn in all_edges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u,v)


# attenzione
# prima di aggiungere N archi ho M nodi
# dopo averli aggiunti spesso il numero di nodi cambia.......


    # ==========================================================================
    # ACCEDOA AI PARAMTERI DEL GRAFO

    def get_numnodi(self):
        return len(self._grafo.nodes())


    def get_numArchi(self):
        return len(self._grafo.edges())


    @property
    def fermate(self):
        return self._fermate