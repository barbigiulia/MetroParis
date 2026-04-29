from model.fermata import Fermata
from model.model import Model

model = Model()  #istanza del modello


# mi aspetto : 0
print("Numero nodi: ", model.get_numnodi())
print("Numero archi: ", model.get_numArchi())

# testo la funzione
model.buildGraph()
# mi aspetto un numero > 0
print("Numero nodi: ", model.get_numnodi())
print("Numero archi: ", model.get_numArchi())

# source = oggetto di tipo Fermata
#source = Fermata(2,"Abbesses",2.33855  ,  48.8843)

source = Fermata(2,	"Abbesses",	2.33855,	48.8843)
nodiBFS = model.getBFSNodesFromEdges(source)
print(len(nodiBFS))
for i in range(0,10): #stampo i primi 10
    print(nodiBFS[i])


nodiDFS = model.getDFSNodesFromEdges(source)
print(len(nodiDFS))
for j in range(0,10): #stampo i primi 10
    print(nodiDFS[j])
