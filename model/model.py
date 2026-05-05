import datetime
from random import weibullvariate

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() # Tutte le fermate del database
        self._grafo = nx.DiGraph()  # istanza del Grafo orientato, semplice, non pesatp
        self._idMapFermate = {}  #dizionario per collegare id_fermata --> oggetto fermata

        # PER RECUPERARE L'OGGETTO DATO L'ID (in questo caso
        # la chiave primaria della tabella)
        for  f in self._fermate:
            # interrogo il diz con questa chiave
            self._idMapFermate[f.id_fermata] = f

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)   # aggiungo i nodi (finora nulla di nuovo

        # cosa cambia: come aggiungo gli archi
        self.addEdgesPesati()



    def addEdgesPesati(self):
        # con questo metodo sto semplificando la query
        # riutilizzo il principio di funzionamento del metodo addEdges3()
        # ma contando quante volte provo ad aggiungere l'arco
        self._grafo.clear_edges()
        all_edges = DAO.getAllEdges()
        for connessione in all_edges:
            u = self._idMapFermate[connessione.id_stazP]
            v = self._idMapFermate[connessione.id_stazA]
            if self._grafo.has_edge(u, v): # se c'è già un arco tra u e v
                self._grafo[u][v]["weight"] += 1  # incremento il peso
            else:
                self._grafo.add_edge(u,v, weight=1)  # altrimenti lo creo, con peso = 1


        # ALTRIMENTI POSSO FARE QUESTO NEL DAO --> se la query non è complicata


    def addEdgesPesatiV2(self):
        # delega il calcolo del peso alla query sql, invece di usare il metodo adEdgesPesati()
        self._grafo.clear_edges()
        allEdgesWithPeso = DAO.getAllEdgesPesati()
        # (id_stazP, id_stazA, peso)  --> ho una tupla
        for e in allEdgesWithPeso:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = e[2]
            self._grafo.add_edge(u,v,weight=peso)


    def archiPesoMaggiore(self):
        # restituisce gli archi con peso > 1
        edges = self._grafo.edges(data=True) # metodo di _grafo
        # data = True, stampa gli archi con il loro peso
        edgesMaggiori = []
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1:  # uso il metodo della libreria per filtrare
                # self._grafo[e[0]][e[1]]["weight"]
                edgesMaggiori.append(e)
        return edgesMaggiori
# ================== BFS ================================================
    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source)
        # produce archi BFS: (a,b), (b,c)....
        nodiBFS = []
        for u, v in archi: # ignoro il primo nodo(source lo aggiungo io)
            nodiBFS.append(v)  # aggiungo solo i nodi raggiunti
        return nodiBFS

    # versione ALTERNATIVA, più semplice
    def getBFSNodesFromTree(self, source):
        # costruisce direttamente un ALBERO BFS
        tree = nx.bfs_tree(self._grafo, source)
        #archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi

#=================== DFS =================================
    # ALBERTO DFS, visita in profondità
    # va il più lontano possibile su un ramo
    # poi torna indietro
    # poi esplora altri rami
    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source) # albero di visita
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi # restituisce i nodi visitati


    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source)
        nodiDFS = []
        for u, v in archi:
            nodiDFS.append(v)
        return nodiDFS  # stessi identici elementi, cambia solo l'ORDINE!

# ===================COSTRUZIONE GRAFO ================================

    def buildGraph(self):
        # instanzio il grafo
        # inizilializzato nel metodo __init__()
        # 1) pulisco
        self._grafo.clear()
        # 2) popolo il grafico con la lista delle fermate
        self._grafo.add_nodes_from(self._fermate) # aggiungo tutte le fermate come nodi
        tic = datetime.now()
        self.addedges3()  # aggiungo gli archi con il metodo migliore tra i 3!
        toc = datetime.now()
        print("Tempo impiegato da modo 3:", toc - tic)

# ==========================================================================

    # 1) metodo PEGGIORE --> lento
    #  faccio una query per ogni singolo arco (aggiungo 1 arco alla volta)
    # quando uso questa implementazione?  Quando i GRAFI SONO PICCOLI !!!!
    def addedges1(self):
        # 619^2 fermate (doppio ciclo) -> poco efficiente e lenta
        # prendo tutte le possibili coppie di fermate
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate:
                if DAO.hasConnexion(u,v): # se True
                    self._grafo.add_edge(u,v)

    # 2) METODO INTERMEDIO
    def addedges2(self):
        self._grafo.clear_edges()
        # data una fermata, prendo quelle vicine
        for u in self._fermate:   # guardo i suoi vicini adiacenti
            for connessione in DAO.getVicini(u):
                v = self._idMapFermate[connessione.id_stazA]
                self._grafo.add_edge(u,v)

    # 3)  MIGLIORE !!!
    def addedges3(self):
        self._grafo.clear_edges() # restano solo i nodi, gli archi vengono ricreati da zero
        all_edges = DAO.getAllEdges() # 1 query sola, prendo tutti gli archi
        for conn in all_edges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u,v)


# attenzione
# NUM CONNESSIONI (DEL DATABASE) != NUM DI ARCHI AGGIUNTI
# QUESTO SUCCEDE PERCHE' CI SONO ALCUNE FERMATE SERVITE DA PIU' LINEE !!
    # questa cosa non succederebbe se avessimo un MultiGraph() --> 2^ richiesta dell'esercizio



    # ==========================================================================
    # ACCEDO AI PARAMTERI DEL GRAFO

    def get_numnodi(self):
        return len(self._grafo.nodes())


    def get_numArchi(self):
        return len(self._grafo.edges())


    # permette accesso controllato dalla View
    @property
    def fermate(self):
        return self._fermate