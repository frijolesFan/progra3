import itertools as it

archivo = 'SD1NZURG-muyfacil.txt'
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
  return ColsConstraints

def DefRowsConstraints(IdCols,Dom):
  RowsConstraints=[]
  for i in Dom:
    ConstraintVars=[f"{id}{i}" for id in IdCols]
    RowsConstraints.append(ConstraintVars)
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

def ConsistenceDomsEqual(Constraints,VarDoms):
  anyChange=False
  for var1 in Constraints:
    if len(VarDoms[var1])==2:
      #discardValue=list(Vars[var1])[0]
      for var2 in Constraints:
        if not(var1==var2):
          if VarDoms[var1]==VarDoms[var2]:
            for var3 in Constraints:
              if not(var1==var3) and not(var2==var3):
                oldValue=VarDoms[var3].copy()
                VarDoms[var3].discard(list(VarDoms[var1])[0])
                VarDoms[var3].discard(list(VarDoms[var1])[1])
                if not(oldValue==VarDoms[var3]):
                  anyChange=True
  return anyChange

def DomsEqual(Vars,constraint):
  anyChange=False
  varsEquals={}
  for var1 in constraint:
    if len(Vars[var1])>1:
      for var2 in constraint:
        if not(var1==var2):
          if (Vars[var1]==Vars[var2]):
            if tuple(Vars[var1]) in varsEquals:
              Set_aux=set(varsEquals[tuple(Vars[var1])].copy())
              Set_aux.add(var1)
              Set_aux.add(var2)
              varsEquals[tuple(Vars[var1])]=list(Set_aux)
            else:
              varsEquals[tuple(Vars[var1])]=[var1,var2]
  for domVar in varsEquals:
    if len(domVar)==len(varsEquals[domVar]):
      for var in constraint:
        if not(var in varsEquals[domVar]):
          for value in domVar:
            oldValue=Vars[var].copy()
            Vars[var].discard(value)
            if not(oldValue==Vars[var]):
              anyChange=True
  return anyChange

ConsistenceDifference(ConstraintsVars,Vars)
for const in ConstraintsVars:
  ConsistenceDomsEqual(const,Vars)

constraints = {
    "ConsistenceDifference": ConstraintsVars,
    "ConsistenceDomsEqual": ConstraintsVars,
    "DomsEqual": ConstraintsVars
}

anyChange = True
iteration = 1
while anyChange:
    print(f"iteration # {iteration}")
    anyChange = False
    for const_name, const_vars in constraints.items():
        for varsList in const_vars:
            print(f"consistence of {const_name}")
            anyChange = eval(f"{const_name}(Vars,varsList)") if not(anyChange) else True
    iteration += 1

print(Vars)