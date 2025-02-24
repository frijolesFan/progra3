%relaciones directas ------------

padre(homero, bart).
padre(homero, lisa).
padre(homero, maggie).
padre(abraham, herbert).
padre(abraham, homero).
padre(clancy, marge).
padre(clancy, patty).
padre(clancy, selma).
madre(mona, homero).
madre(marge, bart).
madre(marge, lisa).
madre(marge, maggie).
madre(jacqueline, patty).
madre(jacqueline, selma).
madre(jacqueline, marge).
madre(selma, ling).

%hijo, padre, madre
hijo(herbert, abraham, na).
hijo(homero, abraham, mona).
hijo(bart, homero, marge).
hija(marge, clancy, jacqueline).
hija(patty, clancy, jacqueline).
hija(selma, clancy, jacqueline).
hija(lisa, homero, marge).
hija(maggie, homero, marge).
hija(ling, na, selma).

%relaciones indirectas --------------

abuelo(X, Y) :-
    padre(X, Z), (padre(Z, Y); madre(Z, Y)).

abuela(X, Y) :- 
    madre(X, Z), (padre(Z, Y); madre(Z, Y)).

hermano(X, Y) :-
    (hijo(Y, P, M); hija(Y, P, M)), ((hijo(X, P, _); !); (hijo(X, _, M); !)),
    X \= Y.

hermana(X, Y) :-
    (hijo(Y, P, M); hija(Y, P, M)), ((hija(X, P, _); !); (hija(X, _, M); !)),
    X \= Y.

tio(X, Y) :-
    (padre(Z, Y), hermano(X, Z)) ; (madre(Z, Y), hermano(X, Z)).

tia(X, Y) :-
    (padre(Z, Y), hermana(X, Z)) ; (madre(Z, Y), hermana(X, Z)).

primo(X, Y) :-
    (tia(T, Y); tio(T, Y)), hijo(X, _, T).

prima(X, Y) :-
    (tia(T, Y); tio(T, Y)), hija(X, _, T).