import flet as ft
# GRAFO SEMPLICE, ORIENTATO, NON PESATO
# ogni vertice = "Fermata"
# due fermate sono collegate se esiste una connessione tra di esse

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._fermataPartenza = None   # stato temporaneo scelto dall'utente


    # CHIAMATO DAL PULSANTE "Crea Grafo"
    def handleCreaGrafo(self,e):
        self._model.buildGraph() # funzione che costruisce il grafo
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Grafo correttamente creato"))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo ha {self._model.get_numnodi()} nodi e {self._model.get_numArchi()} archi "))
        self._view.update_page()



    # attivato dal bottone "Calcola Raggiungibili"
    def handleCercaRaggiungibili(self,e):
        if self._fermataPartenza is None:  # gestione errore UI --> evita crash logico
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Attenzione non è stata scelta la stazione di partenza",
                                                          color="red"))
            self._view.update_page()
            return
        # se invece l'utente ha scelto la fermata dii partenza (source)
        # BFS visita in ampiezza
        # parte dalla fermata selezionata e ritorna la lista di nodi raggiungibili
        nodes = self._model.getBFSNodesFromEdges(self._fermataPartenza)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"DI seguito i nodi raggiungibili da {self._fermataPartenza}"))
        for n in nodes:
            self._view.lst_result.controls.append(ft.Text(n))
        self._view.update_page()


    # RIEMPIE DUE DIVERSI DROPDOWN
    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate  # lista di tutte le stazioni metro

        # Secondo il campo di testo in cui è stata selezionata la fermata
        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,  # quello che vede l'utente
                                                     data=f, # oggetto Fermata reale
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome, # stringa visualizzata
                                                     data=f, #oggetto Fermata
                                                     on_click=self.read_DD_Arrivo ))
                                                    # fz chiamata quando chiamo quel campo

    # SALVA LA FERMATA SCELTA DALL'UTENTE
    def read_DD_Partenza(self,e):
        print("read_DD_Partenza called ")
        if e.control.data is None:
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self,e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data



    # =========== BOTTONE - TROVA PERCORSO ============================
    def handleTrovaPercorso(self, e):
        # recupero i dati che mi servono
        if self._fermataPartenza is None or self._fermataArrivo is None :
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Attenzione, necessario"
                                                          " selezionare fermate di partenza ed arrivo",
                                                          color="red"))
            self._view.update_page()
            return
        tot_time , optPath = self._model.getShortestPath(self._fermataPartenza, self._fermataArrivo)
        # se non trovo il percorso --> l'algoritmo restituisce un cammino vuoto
        if optPath ==[]:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text(f"Non ho trovato un cammino fra"
                                                          f" {self._fermataPartenza} e {self._fermataArrivo} ",
                                                          color="orange"))
            self._view.update_page()
            return
        # se invece ho trovato il cammino
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text(f"Ho trovato un cammino fra"
                                                      f" {self._fermataPartenza} e {self._fermataArrivo} "
                                                      f"che impiega {tot_time} minuti",
                                                      color="green"))
        self._view.lst_result.controls.append(ft.Text("Di seguito la lista di fermate"))
        for v in optPath:
            # stampo la sequenza di nodi
            self._view.lst_result.controls.append(ft.Text(v))
        self._view.update_page()
