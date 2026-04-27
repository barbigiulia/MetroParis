from dataclasses import dataclass

@dataclass
class Connessione:
    id_connessione: int
    id_linea: int
    id_stazP: int
    id_stazA: int

    def __hash__(self):
        return hash(self.id_connessione)

    # non ho il metodo str() perchè ho solo interi

    def __eq__(self, other):
        return self.id_connessione == other.id_connessione
