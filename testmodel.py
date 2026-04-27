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
