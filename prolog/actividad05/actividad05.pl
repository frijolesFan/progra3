%1: hombre, 2: mujer
hijos(abraham, [homero, herbert], 1).
hijos(mona, [homero], 2).

hijos(clancy, [marge, patty, selma], 1).
hijos(jacqueline, [marge, patty, selma], 2).

hijos(homero, [bart, lisa, maggie], 1).
hijos(marge, [bart, lisa, maggie], 2).

hijos(selma, [ling], 2).


padre(X, Y) :- hijos(Y, Z, 1), member(X, Z).
madre(X, Y) :- hijos(Y, Z, 2), member(X, Z).
%consulta independiente del genero
padres(X, Y) :- hijos(Y, Z, _), member(X, Z).

abuelo(X, Y) :- padres(X, Z), padre(Z, Y).
abuela(X, Y) :- padres(X, Z), madre(Z, Y).
%consulta independiente del genero
abuelos(X, Y) :- padres(X, Z), padres(Z, Y).

hermanos_padre(X, Y) :- padres(X, Z), hijos(Z, H, 1), member(X, H), member(Y, H),  X \= Y.
hermanos_madre(X, Y) :- padres(X, Z), hijos(Z, H, 2), member(X, H), member(Y, H),  X \= Y.
%consulta independiente del genero del padre
hermanos(X, Y) :- hermanos_padre(X, Y); hermanos_madre(X, Z), Z \= Y.

tios_padre(X, Y) :- padre(X, Z), hermanos(Z, Y).
tios_madre(X, Y) :- madre(X, Z), hermanos(Z, Y).
%consulta independiente del genero del padre
tios(X, Y) :- padres(X, Z), hermanos(Z, Y).