import itertools as it

letras = set("SENDMOREMONEY")
digitos = set(range(10))
#print(digitos)

perms = list(it.permutations(digitos, len(letras)))
print(len(perms))

