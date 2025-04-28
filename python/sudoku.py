import itertools as it
import os

Dom = set(range(1,10))
IdCols = "ABCDEFGHI"
keys = list(it.product(range(1,10),IdCols))
strKeys=[f"{key[1]}{key[0]}" for key in keys]

Vars={key:Dom.copy() for key in strKeys}

# Obtener la ruta del directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'mi_archivo.txt')

with open(file_path, 'r') as f:
  for key in Vars.keys():
    valor=f.readline().strip()
    if valor.isdigit() and len(valor) == 1:  # Verifica si es un solo dígito
      #print(f"{key}={valor}")
      Vars[key]={int(valor)}
Vars['A1'].discard(1)
print(Dom)
Vars