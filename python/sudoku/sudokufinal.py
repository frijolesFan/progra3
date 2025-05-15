#genera cada celda del sudoku

debug = True

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

with open(r"c:\Users\USER\Desktop\Semestre 4\progra3\rep3\python\sudoku\tab1.txt") as fd: 
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
#bucle principal de resolución aplicando unicamente consistencia
prev_count = -1
while True:
    eliminar_valores_fijos(const, Vars)
    
    varsWithoutValue = [value for var, value in Vars.items() if len(value) > 1]
    current_count = len(varsWithoutValue)
    
    if current_count == prev_count:
        break
    prev_count = current_count

print(f"{separador()}Resultado final:\n\n{Vars}") if debug else None  