import itertools as it
from unicodedata import digit

letras = set("SEND MORE MONEY")
letras.discard(" ")
digitos = set(range(0,10))
digitos.discard(1)

perms = list(it.permutations(digitos, len(letras) - 1))
dic = {k: None for k in letras}
def posM(dic):
    p = 0
    for i in dic.keys():
        if i == "M":
            return p
            break
        p += 1

print(posM(dic))