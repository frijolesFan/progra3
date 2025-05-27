fullDom = set(range(1,10))

Vars = {}
for row in fullDom:
    for col in "ABCDEFGHI":
        Vars[f"{col}{row}"] = fullDom.copy()

def LoadBoard(Vars,file_path):
    with open(file_path, 'r') as file:
        pos = 0
        for line in file:
            if((line.strip().isdigit()) and (int(line) < 10)):
                Vars[list(Vars.keys())[pos]] = {int(line)}
            else: 
                if(line.startswith('|')):
                    line = line.strip()
                    line = line[1:]
                    Values = line.split('/')
                    for Posc in range(0, len(Values)):
                        if(Values[Posc].isdigit()):
                            Values[Posc] = int(Values[Posc])
                        else:
                            Values[Posc] = ' '
                    Vars[list(Vars.keys())[pos]] = {tuple(Values)}
            pos += 1

LoadBoard(Vars, 'kakuro/2.txt')

def defineRows():
    allRows=[]
    Value = []
    Elements = []
    Space = []

    for row in fullDom:

        for col in "ABCDEFGHI":

            if(isinstance(list(Vars[f"{col}{row}"])[0], tuple)):
                if(isinstance(list(list(Vars[f"{col}{row}"])[0])[0], int)):
                    #print(f"{col}{row}")
                    if(len(Value) > 0):
                        Space.append(Value)
                        Space.append(Elements)
                        allRows.append(Space)
                        Elements = []
                        Space = []
                        Value = [list(list(Vars[f"{col}{row}"])[0])[0]]
                    else:
                        Value = [list(list(Vars[f"{col}{row}"])[0])[0]]

            elif(Vars[f"{col}{row}"] == {0}):
                if(len(Value) > 0):
                        Space.append(Value)
                        Space.append(Elements)
                        allRows.append(Space)
                        Elements = []
                        Space = []
                        Value = []

            else:
                Elements.append(f"{col}{row}")

    return allRows

def defineCols():
    allCols = []
    Value = []
    Elements = []
    Space = []

    for col in "ABCDEFGHI":
        
        for row in fullDom:
            if(isinstance(list(Vars[f"{col}{row}"])[0], tuple)):
                if(isinstance(list(list(Vars[f"{col}{row}"])[0])[1], int)):
                    if(len(Value) > 0):
                        Space.append(Value)
                        Space.append(Elements)
                        allCols.append(Space)
                        Elements = []
                        Space = []
                        Value = [list(list(Vars[f"{col}{row}"])[0])[1]]
                    else:
                        Value = [list(list(Vars[f"{col}{row}"])[0])[1]]

            elif(Vars[f"{col}{row}"] == {0}):
                if(len(Value) > 0):
                        Space.append(Value)
                        Space.append(Elements)
                        allCols.append(Space)
                        Elements = []
                        Space = []
                        Value = []

            else:
                Elements.append(f"{col}{row}")
    
    return allCols

Rows = []
for list1 in defineRows():
    Rows.append(list1[1])

Cols = []
for list2 in defineCols():
    Cols.append(list2[1])


constraint={'AllDif':Rows + Cols,
            'DomsEqual':Rows + Cols}

def AllDif(Vars,constraint):
    anyChange = False
    for var1 in constraint:
        if len(Vars[var1])==1:
            discardValue=list(Vars[var1])[0]
            for var2 in constraint:
                if not(var1==var2):
                    oldValue=Vars[var2].copy()
                    Vars[var2].discard(discardValue)
                    if not(oldValue==Vars[var2]):
                        anyChange=True
    return anyChange

def DomsEqual(Vars,constraint):
    anyChange=False
    for var1 in constraint:
        if len(Vars[var1])==2:
            #discardValue=list(Vars[var1])[0]
            for var2 in constraint:
                if not(var1==var2):
                    if Vars[var1]==Vars[var2]:
                        for var3 in constraint:
                            if not(var1==var3) and not(var2==var3):
                                oldValue=Vars[var3].copy()
                                Vars[var3].discard(list(Vars[var1])[0])
                                Vars[var3].discard(list(Vars[var1])[1])
                                if not(oldValue==Vars[var3]):
                                    anyChange=True
    return anyChange

def findCombinations(numElements, targetSum):
    def backtrack(start, path, currentSum):
        if len(path) == numElements:
            if currentSum == targetSum:
                results.append(path.copy())
            return
        
        for i in range(start, 10):  # Números del 1 al 9
            if currentSum + i > targetSum:
                break
            path.append(i)
            backtrack(i + 1, path, currentSum + i)  # i + 1 asegura números únicos
            path.pop()

    results = []
    backtrack(1, [], 0)
    return results


def SumConstraint():
    Options = set()
    Spaces = []
    Spaces.append(defineRows())
    Spaces.append(defineCols())


    for Route in Spaces:
        for i in range(0, len(Route)):
            combinations = findCombinations(len((Route[i])[1]), ((Route[i])[0])[0])

            for j in range(0, len(combinations)):
                Options.update(combinations[j])

            for var in (Route[i])[1]:
                Vars[var] = Vars[var].intersection(Options)

            Options = set()

def Refresh(Vars, constraint):
  anyChange=True
  iteration=1
  while anyChange:
    anyChange=False
    for const in constraint:
      for varsList in constraint[const]:
        anyChange=eval(f"{const}(Vars,varsList)") if not(anyChange) else True
    iteration+=1

Refresh(Vars, constraint)

for Constraint in constraint['AllDif']:
    SumConstraint()
    Refresh(Vars, constraint)

Base = Vars.copy()

# Crear una lista de ítems a eliminar
items_to_delete = []

for var in Base:
    if isinstance(list(Base[var])[0], tuple) or Base[var] == {0}:
        items_to_delete.append(var)
    elif len(Base[var]) != 1:
        Base[var] = {0}

# Eliminar los ítems del diccionario
for var in items_to_delete:
    del Base[var]

# Función principal para la solución del Kakuro utilizando backtracking
def SolveKakuro(Vars, Base, constraint):
    # Verificar si el tablero está completo
    if IsComplete(Base):
        return Base  # Devolver el tablero si está completo

    # Identificar una celda vacía en el tablero
    Current = EmptyCell(Base)

    # Si no hay celdas vacías, el tablero está completo pero no resuelto
    if Current is None:
        return Base

    # Obtener las posibles cifras que pueden ir en la celda actual
    Posibilities = list(Vars[Current])

    # Recorrer todas las posibilidades para la celda actual
    for Posc in Posibilities:
        # Asignar la posibilidad actual a la celda
        Base[Current] = {Posc}

        # Verificar si la asignación es válida
        if ValidMovement(Base, constraint):
            # Realizar llamada recursiva para continuar con la solución
            result = SolveKakuro(Vars, Base, constraint)

            # Si la llamada recursiva devuelve una solución, devolverla
            if result is not None:
                return result

        # Restaurar la celda a vacía si la asignación no es válida
        Base[Current] = {0}

    # Si ninguna posibilidad lleva a una solución válida, devolver None
    return None

# Función para identificar una celda vacía en el tablero
def EmptyCell(Base):
    for Var in Base:
        if (list(Base[Var])[0] == 0):
            return Var

# Función para verificar si el tablero actual es válido según las reglas del Kakuro
def ValidMovement(Base, constraint):
    # Iterar sobre cada conjunto de celdas en las restricciones (filas y columnas)
    all_rows = defineRows()
    all_cols = defineCols()

    for Const in constraint['AllDif']:
        values = set()
        is_row = constraint['AllDif'].index(Const) < len(all_rows)

        for var1 in Const:
            cell_value = list(Base[var1])[0]
            if cell_value == 0:
                continue
            if cell_value in values:
                return False
            values.add(cell_value)

        if is_row:
            target_sum = all_rows[constraint['AllDif'].index(Const)][0][0]
        else:
            target_sum = all_cols[constraint['AllDif'].index(Const) - len(all_rows)][0][0]

        result = [list(Base[var2])[0] for var2 in Const if list(Base[var2])[0] != 0]
        if sum(result) > target_sum:
            return False
        if len(result) == len(Const) and sum(result) != target_sum:
            return False

    return True

def IsComplete(Base):
    for Var in Base:
        if(list(Base[Var])[0] == 0):
            return False
    return True

SolveKakuro(Vars, Base, constraint)
#ValidMovement(Base, constraint)

Vars_N = Vars.copy()

for var in Base:
    Vars_N[var] = Base[var]

for var in Vars_N:
        if (isinstance(list(Vars_N[var])[0], tuple)):
            Vars_N[var] = {'/'}
        if(Vars_N[var] == {0}):
            Vars_N[var] = {' '}
        if(len(Vars_N[var]) != 1):
            Vars_N[var] = {0}


def PrintKakuro(Vars_N):
    # Imprimir números de columna
    print('   ' + ''.join(f' {j+1}  ' for j in range(9)))
    print('  ┌' + '─' * 36 + '┐')
    
    cont = 0
    for var in Vars_N:
        # Inicio de nueva fila
        if cont % 9 == 0:
            if cont != 0:
                if cont < 81:  # Si no es la última fila
                    print('\n  ├' + '─' * 36 +'┤')
            print(f'\n{(cont // 9) + 1} │', end='')
        
        # Imprimir celda
        valor = list(Vars_N[var])[0]
        if valor == '/':
            print('███│', end='')
        elif valor == ' ':
            print('███│', end='')
        else:
            print(f' {valor} │', end='')
            
        cont += 1
    
    # Imprimir línea final
    print('\n  └' + '─' * 36 + '┘')
PrintKakuro(Vars_N)