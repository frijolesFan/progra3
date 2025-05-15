import itertools as it

letras = set("SEND MORE MONEY")
letras.discard(" ")
digitos = set(range(0,10))
digitos.discard(1)
digitos.discard(0)
digitos.discard(9)

perms = list(it.permutations(digitos, len(letras) - 3))
print(len(perms))
dic = {k: None for k in letras}
dic["M"] = 1
dic["O"] = 0
dic["S"] = 9

def validar(Dic):    
    money = Dic["M"] * 10000 + Dic["O"] * 1000 + Dic["N"] * 100 + Dic["E"] * 10 + Dic["Y"]
    send = Dic["S"] * 1000 + Dic["E"] * 100 + Dic["N"] * 10 + Dic["D"]
    more = Dic["M"] * 1000 + Dic["O"] * 100 + Dic["R"] * 10 + Dic["E"]
    return (send + more) == money

for perm in perms:
    p = 0
    for k in dic.keys():
        if k != "M" and k!= "O" and k!= "S":
            dic[k] = perm[p]
            p += 1
    if validar(dic):
        print(dic)
