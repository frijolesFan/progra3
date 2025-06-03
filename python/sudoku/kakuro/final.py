#RESOLUTOR DE KAKURO EN PYTHON MEDIANTE CSP
#Autor: Juan Camilo Guevara Osorio
#Para la asignatura de Programación 3
#Docente Ramiro Andrés Valencia Barrios
#
#Hecho en Python 3.13.2, mediante Trae

#El programa inicializa el tablero de Kakuro, generando cada celda con un conjunto de valores posibles.
#Esto se realiza de igual forma que en el Sudoku.
fullDom = set(range(1,10))

Vars = {}
for row in fullDom:
    for col in "ABCDEFGHI":
        Vars[f"{col}{row}"] = set(range(1,10))

#El programa carga el tablero de Kakuro desde un archivo de texto.
#Este archivo debe contener las restricciones de suma en formato |R/D (r: derecha, d: abajo), los posibles
#valores de cada celda, y los espacios negros con un 0.

def LoadBoard(Vars,file_path):
    with open(file_path, 'r') as file:
        pos = 0
        for line in file:
            if((line.strip().isdigit()) and (int(line) < 10)):  #Asigna inmediatamnte los valores que ya están en el tablero
                Vars[list(Vars.keys())[pos]] = {int(line)}
            else: 
                if(line.startswith('|')):   #Verifica si la celda es una suma, identificando el formato
                    line = line.strip()
                    line = line[1:]
                    Values = line.split('/')
                    for Posc in range(0, len(Values)):
                        if(Values[Posc].isdigit()): #asigna el valor de la suma en su dirección correspondiente
                            Values[Posc] = int(Values[Posc])
                        else:   #si una direccion no tiene suma, se asigna un string vacío
                            Values[Posc] = ' '
                    Vars[list(Vars.keys())[pos]] = {tuple(Values)}
            pos += 1

#almacena el tablero de kakuro
LoadBoard(Vars, 'kakuro/1.txt')

#-------------------------// DEFINICION DE RESTRICCIONES //--------------------------#
#se definen las restricciones de suma, tanto para filas como para columnas

#define las restricciones de suma horizontales
def defineFilas():
    allRows=[]      #almacena las restricciones de filas
    Value = []      #almacena los valores de las sumas para la restriccion  
    Elements = []   #almacena las celdas de cada suma
    Space = []      #almacena las sumas en cada restricción

    for row in fullDom:
        for col in "ABCDEFGHI": 
            if(isinstance(list(Vars[f"{col}{row}"])[0], tuple)):            #verifica si la celda tiene una tupla (osea, una suma))
                if(isinstance(list(list(Vars[f"{col}{row}"])[0])[0], int)): #verifica si tiene un valor, osea una suma de fila
                    #print(f"{col}{row}")
                    if(len(Value) > 0):
                        Space.append(Value)     #agrega el valor de la suma
                        Space.append(Elements)  #agrega las celdas de la suma
                        allRows.append(Space)   #agrega la restricción

                        #Se reinician las variables para la siguiente restricción
                        Elements = []
                        Space = []
                        Value = [list(list(Vars[f"{col}{row}"])[0])[0]]
                    else:   #si no contiene una suma de fila, se continúa con la siguiente celda	
                        Value = [list(list(Vars[f"{col}{row}"])[0])[0]]

            elif(Vars[f"{col}{row}"] == {0}):   #si la celda está vacía
                if(len(Value) > 0):            #y hay una restriccion en proceso, se finaliza
                        Space.append(Value)
                        Space.append(Elements)
                        allRows.append(Space)
                        Elements = []
                        Space = []
                        Value = []

            else:   #si es una celda normal, se agrega a la restriccion
                Elements.append(f"{col}{row}")

    return allRows

#almacena las restricciones de suma verticales, funciona de igual modo que las horizontales
#se hace en fuciones separadas ya que una unificada genera problemas
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

#print(defineFilas())

#crea la lista de restricciones de filas
Filas = []
for list1 in defineFilas():
    Filas.append(list1[1])   #agrega las celdas, que se almacenan en el indice 1

#hace lo mismo para las columnas
Cols = []
for list2 in defineCols():
    Cols.append(list2[1])

#define el diccionario de restricciones
constraint={'AllDif':Filas + Cols,       #combina las restricciones de filas y columnas
            'DomsEqual':Filas + Cols}    #para ambas restricciones

#---------------------------------// CONSISTENCIA //---------------------------------#
#se comienzan a implementar tecnicas de consistencia para reducir el dominio de las
#variables

#elimina los valores que ya están de las demás celdas de la restricción
def AllDif(Vars,constraint):
    anyChange = False   #por defecto, no hay cambios
    for var1 in constraint:
        if len(Vars[var1])==1:  #verifica si la celda tiene valor asignado y lo obtiene
            discardValue=list(Vars[var1])[0]    
            for var2 in constraint: #para cada celda de la restricción
                if not(var1==var2): #verifica que no es la misma celda
                    oldValue=Vars[var2].copy()          #guarda el dominio anterior
                    Vars[var2].discard(discardValue)    #elimina el valor de la celda
                    if not(oldValue==Vars[var2]):       #y si el dominio cambió
                        anyChange=True                  #se indica el cambio
    return anyChange

#elimina los dominios que se repiten en dos variables de las demás celdas de la restricción	
def DomsEqual(Vars,constraint):
    anyChange=False #por defecto, no hay cambios
    for var1 in constraint:
        if len(Vars[var1])==2:      #busca celdas con un dominio de dos valores
            for var2 in constraint: #busca otra variable de las restriccion
                if not(var1==var2): #diferente de si misma
                    if Vars[var1]==Vars[var2]:  #si tienen el mismo dominio
                        for var3 in constraint:                     #busca otra celda de la restriccion     
                            if not(var1==var3) and not(var2==var3): #diferente a las dos ya obtenidas
                                oldValue=Vars[var3].copy()              #guarda el dominio anterior
                                Vars[var3].discard(list(Vars[var1])[0]) #elimina los dos valores de la celda
                                Vars[var3].discard(list(Vars[var1])[1])
                                if not(oldValue==Vars[var3]):   #si el dominio cambió
                                    anyChange=True              #se indica el cambio
    return anyChange

#encuentra las combinaciones posibles de valores que sumen la suma de la restricción
def findCombinations(numElements, targetSum):
    def backtrack(start, path, currentSum): #esto se logra mediante backtracking 
        if len(path) == numElements:        #caso base: si se tiene el numero correcto de valores
            if currentSum == targetSum:     #y la suma es la correcta
                results.append(path.copy()) #se agrega a la lista de resultados
            return
        
        #prueba numeros del 1 al 9
        for i in range(start, 10):
            if currentSum + i > targetSum:  #regresa si la suma es mayor que el objetivo
                break                      
            path.append(i)                          #agrega el valor a la ruta
            backtrack(i + 1, path, currentSum + i)  # i + 1 asegura números únicos
            path.pop()                              #retrocede removiendo el ultimo valor

    results = []            #lista donde se almacenan los resultados
    backtrack(1, [], 0)     #inicia el backracking
    return results

#asigna los valores posibles de acuerdo a las restricciones de suma
def SumConstraint():
    Options = set()     #almacena las combinaciones posibles
    Spaces = []         #lista que contiene filas y columnas
    Spaces.append(defineFilas())    #agrega las filas
    Spaces.append(defineCols())     #agrega las columnas

    for Route in Spaces:    #para cada fila y columna
        for i in range(0, len(Route)): 

            #calcula las posibles combinaciones de numeros que cumplen con la restriccion de suma
            combinations = findCombinations(len((Route[i])[1]), ((Route[i])[0])[0])

            for j in range(0, len(combinations)):   #busca cada combinacion
                Options.update(combinations[j])     #y la almacena

            for var in (Route[i])[1]:                       #toma cada celda de la restriccion
                Vars[var] = Vars[var].intersection(Options) #y actualiza su dominio mediante la interseccion

            #reinicia la variable para la siguiente restriccion
            Options = set()

#actualiza el dominio de las variables de forma iterativa hasta que no haya más cambios
def Refresh(Vars, constraint):
    anyChange=True #se inicializa en true para que se inicie el bucle
    iteration=1
    
    #continúa mientras se sigan produciendo cambios en las restricciones
    while anyChange:
        anyChange=False
        for const in constraint:                #itera sobre cada tipo de restricción
            for varsList in constraint[const]:  #y la lista de variables asociadas a esa restricción
                #ejecuta la función de restricción correspondiente y actualiza la bandera segun si hay cambios
                anyChange=eval(f"{const}(Vars,varsList)") if not(anyChange) else True
        iteration+=1

#--------------------------// SOLUCION DEL KAKURO //------------------------------#
#se aplican las funciones de consistencia anteriormente creadas como primer paso
#para preparar el tablero para su resolucion

Refresh(Vars, constraint) #aplica las funciones de consistencia

for Constraint in constraint['AllDif']: #para cada restriccion de tipo AllDif
    SumConstraint()                     #se aplica la restriccion de suma
    Refresh(Vars, constraint)           #y se actualiza el dominio

#ahora, se crea una copia del tablero para realizar el backtracking lamada base
Base = Vars.copy()

#se eliminan las celdas que no tienen restricciones ni son celdas vacías
items_to_delete = []    #lista para almacenar las celdas a eliminar
for var in Base:
    if isinstance(list(Base[var])[0], tuple) or Base[var] == {0}:   #si la celda es una celda vacia o una suma
        items_to_delete.append(var)                                 #se agrega a la lista
    elif len(Base[var]) != 1:   #si la celda tiene mas de un valor posible
        Base[var] = {0}         #se marca como celda vacia

#elimina las celdas que habiamos determinado
for var in items_to_delete:
    del Base[var]

#--------// FUNCION PRINCIPAL PARA LA SOLUCION DEL KAKURO USANDO BACKTRACKING //---------#

def SolveKakuro(Vars, Base, constraint):
    if IsComplete(Base):    #por caso base verifica si el tablero está completo
        return Base         #y lo retorna si es así
    Current = EmptyCell(Base)   #se obtiene la siguiente celda vacía
    if Current is None:         #si no hay mas celdas vacías, retorna None
        return None
    
    Posibilities = list(Vars[Current])  #se obtienen los posibles valores para la celda actual
    for Posc in Posibilities:           
        Base[Current] = {Posc}  #se asigna uno a uno de forma tempora para probaro
        if ValidMovement(Base, constraint): #se verifica que el valor cumpla con las restricciones
            result = SolveKakuro(Vars, Base, constraint)    #llamada recursiva con el nuevo estado del tablero
            if result is not None:  #si se encuencuentra una solución, se retorna
                return result
        Base[Current] = {0} #si la asignación no es válida, se deshace
    return None

#/*-----*/#/*-----*// UTILIDADES PARA EL BACKTRACKING //*-----*/#/*-----*/#

#función para identificar una celda vacía en el tablero
def EmptyCell(Base):
    for Var in Base:
        if (list(Base[Var])[0] == 0):
            return Var

#función para verificar si el tablero actual es válido según las restricciones establecidas
def ValidMovement(Base, constraint):
    all_rows = defineFilas()    #obtiene las filas
    all_cols = defineCols()     #obtiene las columnas
    for Const in constraint['AllDif']:  #recorre todas las restricciones AllDif
        values = set()  #set para almacenar los valores de las celdas en la restricción
        is_row = constraint['AllDif'].index(Const) < len(all_rows) #determina si la restricción es una fila o columna

        for var1 in Const:                      #recorre todas las celdas en la restricción
            cell_value = list(Base[var1])[0]    #obtiene el valor de la celda
            if cell_value == 0:                 #si el valor es 0, se ignora
                continue                        #y pasa a la siguiente celda
            if cell_value in values:            #si el valor ya está en el set, se retorna False
                return False                    #ya que no cumple con la restricción
            values.add(cell_value)              #agrega el valor al set 

        if is_row:  #si la restricción es una fila
            target_sum = all_rows[constraint['AllDif'].index(Const)][0][0]  #obtiene la suma de la fila
        else:       #si la restricción es una columna
            target_sum = all_cols[constraint['AllDif'].index(Const) - len(all_rows)][0][0]  #obtiene la suma de la columna

        result = [list(Base[var2])[0] for var2 in Const if list(Base[var2])[0] != 0]    #lista de valores de las celdas en la restricción
        if sum(result) > target_sum:    #si la suma de los valores es mayor que la suma de la fila o columna
            return False                #se retorna False
        if len(result) == len(Const) and sum(result) != target_sum:     #si la suma de los valores es igual a la suma de la fila o columna
            return False                                                #pero no todas las celdas tienen un valor asignado se retorna False                   
    #si no ha ocurrido ningun problema, se retorna True ya que la asignación ha sido válida
    return True

#función para verificar si el tablero está completo, es decir, si todas las celdas tienen un valor asignado
def IsComplete(Base):
    for Var in Base:
        if(list(Base[Var])[0] == 0):
            return False
    return True

#-------------------------// RESOLVER EL TABLERO //-------------------------------#

SolveKakuro(Vars, Base, constraint)

#-------------------------// IMPRIMIR EL TABLERO //-------------------------------#

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
    print('   ' + ''.join(f' {j+1}  ' for j in range(9)))
    print('  ┌' + '─' * 36 + '┐')
    cont = 0
    for var in Vars_N:
        if cont % 9 == 0:
            if cont != 0:
                if cont < 81:
                    print('\n  ├' + '─' * 36 +'┤')
            print(f'\n{(cont // 9) + 1} │', end='')
        valor = list(Vars_N[var])[0]
        if valor == '/':
            print('███│', end='')
        elif valor == ' ':
            print('███│', end='')
        else:
            print(f' {valor} │', end='')
        cont += 1
    print('\n  └' + '─' * 36 + '┘')

PrintKakuro(Vars_N)