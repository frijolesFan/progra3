#genera cada celda del sudoku
cols="ABCDEFGHI"
rows={i for i in range(1,10)}

#asigna un dominio a cada celda
Vars={}
for col in cols:
  for row in rows:
    Vars[f"{col}{row}"]=rows.copy()

#genera las restricciones para filas y columnas
const=[]
for col in cols:
  vars=set()
  for row in rows:
    vars.add(f"{col}{row}")
  const.append(vars)

for row in rows:
  vars=set()
  for col in cols:
    vars.add(f"{col}{row}")
  const.append(vars)

print(Vars)