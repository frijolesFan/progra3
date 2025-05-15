#genera cada celda del sudoku

debug = True
ntab = 1

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

with open(f'tab{ntab}.txt') as fd: 
  for fila in filas:
    for col in cols:
      value=int(fd.readline())
      if value<10 and value:
        Vars[f"{col}{fila}"]={value}