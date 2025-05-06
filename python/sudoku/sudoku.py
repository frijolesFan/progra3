import itertools as it

archivo = 'python\sudoku\SD1NZURG-muyfacil.txt'
Dom=set(range(1,10))
IdCols="ABCDEFGHI"
keys=list(it.product(range(1,10),IdCols))
strKeys=[f"{key[1]}{key[0]}" for key in keys]
Vars={key:Dom.copy() for key in strKeys}
with open(archivo, 'r') as f:  # Reemplaza 'mi_archivo.txt' con el nombre de tu archivo
  for linea in f:
    valor = linea.strip()  # Elimina espacios en blanco al principio y al final
    if valor.isdigit() and len(valor) == 1:  # Verifica si es un solo dígito
      print(valor)
with open(archivo, 'r') as f:
  for key in Vars.keys():
    valor=f.readline().strip()
    if valor.isdigit() and len(valor) == 1:  # Verifica si es un solo dígito
      Vars[key]={int(valor)}

def DefColsConstraints(IdCols,Dom):
  ColsConstraints=[]
  for id in IdCols:
    ConstraintVars=[f"{id}{i}" for i in Dom]
    ColsConstraints.append(ConstraintVars)
    #print(ConstraintVars)
  return ColsConstraints

def DefRowsConstraints(IdCols,Dom):
  RowsConstraints=[]
  for i in Dom:
    ConstraintVars=[f"{id}{i}" for id in IdCols]
    RowsConstraints.append(ConstraintVars)
    #print(ConstraintVars)
  return RowsConstraints

def defBoxesContraints(IdCols,Dom):
    allBoxes = []
    for row_start in range(1, 10, 3):
        for col_start in range(0, 9, 3):
            varsBox = []
            for i in range(3):
                for j in range(3):
                    row = row_start + i
                    col = IdCols.index(IdCols[col_start]) + j
                    varsBox.append(f"{IdCols[col]}{row}")
            allBoxes.append(varsBox)
    return allBoxes

ConstraintsVars=DefColsConstraints(IdCols,Dom)+DefRowsConstraints(IdCols,Dom)+defBoxesContraints(IdCols,Dom)
#print(ConstraintsVars)

def ConsistenceDifference(Constraints,VarDoms):
  #recorro todas y cada una de las restricciones
  for constraint in Constraints:
    #y por cada restriccion debo recorrer las variables asociadas, buscando una variable con valor asociado (dominio con un unico valor)
    #y eliminar de los dominios de las otras variables asociadas en la restriccion el valor asociado a la variable actual.
    #Asi sucesivamente con todas y cada una de las variables de la restriccion.
    for var in constraint:
      if len(VarDoms[var])==1:
        for varAux in constraint:
          if varAux!=var:
            VarDoms[varAux].discard(list(VarDoms[var])[0])
  return VarDoms

ConsistenceDifference(ConstraintsVars,Vars)
#print(Vars)

pos=0
for key in strKeys:
  if pos==0:
    listkey=[]
  listkey.append(key)
  pos+=1
  if pos==9:
    print(listkey)
    pos=0