#genera cada celda del sudoku

debug = False

def separador():
  print('\n',"-"*50,'\n')
  return ''

cols="ABCDEFGHI"
filas={i for i in range(1,10)}

#asigna un dominio a cada celda
Vars={}
for col in cols:
  for fila in filas:
    Vars[f"{col}{fila}"]=filas.copy()

print(f"{separador()}Genera el dominio de cada celda:\n\n{Vars}") if debug else None

#genera las restricciones para filas y columnas
const=[]
for col in cols:
  vars=set()
  for fila in filas:
    vars.add(f"{col}{fila}")
  const.append(vars)

for fila in filas:
  vars=set()
  for col in cols:
    vars.add(f"{col}{fila}")
  const.append(vars)

print(f"{separador()}Genera las restricciones por columna y por fila:\n\n{const}") if debug else None

#genera las restricciones para cada cuadro 3x3

for box_x in range(0, 9, 3): 
    for box_y in range(0, 9, 3):
        vars = set()
        for row in range(1 + box_x, 4 + box_x):
            for col in "ABCDEFGHI"[box_y:box_y + 3]:
                vars.add(f"{col}{row}")
        const.append(vars)

print(f"{separador()}Genera la Restricción por cajas:\n\n{const}") if debug else None

#abre el archivo del sudoku y asigna los valores iniciales

with open(r"c:\Users\USER\Desktop\Semestre 4\progra3\rep3\python\sudoku\tab11.txt") as fd: 
  for fila in filas:
    for col in cols:
      value=int(fd.readline())
      if value<10 and value:
        Vars[f"{col}{fila}"]={value}

print(f"{separador()}Asigna los valores iniciales:\n\n{Vars}") if debug else None

#elimina los valores fijos de las celdas

def eliminar_valores_fijos(const, Vars):
    for constraint in const: 
        for key in constraint: 
            if len(Vars[key]) == 1: 
                fixed_value = next(iter(Vars[key]))
                for other_key in constraint: 
                    if other_key != key and len(Vars[other_key]) > 1: 
                        Vars[other_key].discard(fixed_value) 

print(f"{separador()}Elimina los valores fijos:\n\n{Vars}") if debug else None

#asigna valores unicos a las celdas si ese valor no está en los dominios de otras celdas en la misma restricción

def asignar_valores_unicos(const, Vars): 
    for constraint in const: 
        currentDoms = {keyVar: Vars[keyVar] for keyVar in constraint if len(Vars[keyVar]) > 1} 
        
        for key, dom in currentDoms.items(): 
            doms_aux = list(currentDoms.values()).copy() 
            doms_aux.pop(doms_aux.index(dom)) 
            
            difDom = dom.difference(set().union(*doms_aux)) if doms_aux else dom
            
            if len(difDom) == 1: 
                unique_value = list(difDom)[0] 
                
                conflict_found = any(unique_value in Vars[other_key] and len(Vars[other_key]) == 1 
                                   for other_key in constraint if other_key != key) 
                
                if not conflict_found: 
                    Vars[key] = {unique_value} 

print(f"{separador()}Asigna valores unicos:\n\n{Vars}") if debug else None

#reduce el dominio aplicando la técnica de pares ocultos

def pares(const, Vars): 
    for constraint in const: 
        pairs = {key: dom for key, dom in Vars.items() if len(dom) == 2 and key in constraint} 
        
        for key1, dom1 in pairs.items(): 
            for key2, dom2 in pairs.items(): 
                if key1 != key2 and dom1 == dom2:
                    for key in constraint: 
                        if key != key1 and key != key2: 
                            Vars[key] -= dom1 

print(f"{separador()}Aplica pares ocultos:\n\n{Vars}") if debug else None

#reduce el dominio aplicando la técnica de tripletas

def tripletas(const, Vars): 
    for constraint in const: 
        triplets = {key: dom for key, dom in Vars.items() if 2 <= len(dom) <= 3 and key in constraint} 
        
        for key1, dom1 in triplets.items(): 
            for key2, dom2 in triplets.items(): 
                for key3, dom3 in triplets.items(): 
                    if key1 != key2 and key2 != key3 and key1 != key3: 
                        combined_dom = dom1 | dom2 | dom3 
                        if len(combined_dom) == 3:
                            for key in constraint: 
                                if key not in [key1, key2, key3]: 
                                    Vars[key] -= combined_dom 

#aplica la consistencia para reducir el dominio de las celdas
def aplicar_consistencia(const, Vars):
    prev_count = -1
    while True:
        eliminar_valores_fijos(const, Vars)
        asignar_valores_unicos(const, Vars)
        pares(const, Vars)
        tripletas(const, Vars)
        
        varsWithoutValue = [value for var, value in Vars.items() if len(value) > 1]
        current_count = len(varsWithoutValue)
        
        if current_count == prev_count:
            break
        prev_count = current_count
    
    return not any(len(dom) == 0 for dom in Vars.values())

#aplica la consistencia para solucionar el sudoku
aplicar_consistencia(const, Vars)

print(f"{separador()}Resultado final (consistencia):\n\n{Vars}")

#si el resultado no es el sudoku resuelto, aplica la técnica de búsqueda constructiva

def busqueda_constructiva(const, Vars):
    #lista para almacenar el orden de asignación
    orden_asignacion = []
    
    while True:
        #aplica consistencia primero
        if not aplicar_consistencia(const, Vars):
            return False
            
        #verifica si ya está resuelto
        if all(len(dom) == 1 for dom in Vars.values()):
            return True
            
        #encuentra la variable con el dominio más pequeño (mayor a 1)
        var_to_assign = None
        min_domain_size = float('inf')
        
        for key, domain in Vars.items():
            if len(domain) > 1 and len(domain) < min_domain_size:
                min_domain_size = len(domain)
                var_to_assign = key
        
        if var_to_assign is None:
            return False
            
        #ordena los valores del dominio por el número de conflictos
        domain = Vars[var_to_assign]
        value_scores = []
        
        for value in domain:
            conflicts = 0
            #cuenta cuántas variables relacionadas tienen este valor en su dominio
            for constraint in const:
                if var_to_assign in constraint:
                    for other_var in constraint:
                        if other_var != var_to_assign and value in Vars[other_var]:
                            conflicts += 1
            value_scores.append((value, conflicts))
        
        #ordena valores por menor número de conflictos
        value_scores.sort(key=lambda x: x[1])
        
        #asigna el valor con menos conflictos
        best_value = value_scores[0][0]
        Vars[var_to_assign] = {best_value}
        orden_asignacion.append((var_to_assign, best_value))

#muestra el sudku si encuentra una solucion
if busqueda_constructiva(const, Vars):
    print(f"Solución encontrada:\n\n{Vars}{separador()}")
    print("\nTablero resuelto:\n")
    print("    ", end="")
    for col in "ABCDEFGHI":
        print(f" {col:^7}", end="")
    print("\n" + "-" * 80)
    
    for fila in range(1, 10):
        print(f"{fila} |", end="")
        for col in "ABCDEFGHI":
            celda = Vars[f"{col}{fila}"]
            if len(celda) == 1:
                valor = next(iter(celda))
                print(f" {valor:^7}", end="")
            else:
                print(" {:^7}".format("".join(map(str, sorted(celda)))), end="")
        print()
else:
    print(f"{separador()}No se encontró solución")