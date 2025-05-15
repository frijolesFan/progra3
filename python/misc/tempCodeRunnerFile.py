import itertools as it

letras = "ABCDEFGHI"
numeros = "123456789"

def partir3(string):
    partes = [string[i:i+3] for i in range(0,9,3)]
    variables = {}
    for i, parte in enumerate(partes):
        variables[i] = parte
    return partes

l3 = partir3(letras)
n3 = partir3(numeros)
print(l3)
print(n3)

#print(recuadros)

# --- Reglas ---
#   - No se pueden repetir numeros en las columnas
#   - No se pueden repetir numeros en las filas
#   - No se pueden repetir numeros en los recuadros
#   - Si en fila o columnas hay dominios repetidos se eliminan de las demas casillas
#       Si existe A1={1,2}, A2 = {1,2}, A3{1,2,4,5}, A5{1,2,7,8} se elimina {1,2} de A3 y A5
