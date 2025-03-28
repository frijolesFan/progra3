%relaciones directas----------------------------
padre(homero, [bart, lisa, maggie]).
padre(abraham, [herbert, homero]).
padre(clancy, [marge, patty, selma]).

madre(mona, [homero]).
madre(marge, [bart, lisa, maggie]).
madre(jacqueline, [marge, patty, selma]).
madre(selma, [ling]).

% Definición de relaciones hijo/a usando listas de padres
hijo(herbert, [abraham, na]).
hijo(homero, [abraham, mona]).
hijo(bart, [homero, marge]).
hija(marge, [clancy, jacqueline]).
hija(patty, [clancy, jacqueline]).
hija(selma, [clancy, jacqueline]).
hija(lisa, [homero, marge]).
hija(maggie, [homero, marge]).
hija(ling, [na, selma]).

%relaciones indirectas -------------------------
abuelo(X, Y) :-
    padre(X, Hijos), member(Z, Hijos), (padre(Z, Nietos), member(Y, Nietos); madre(Z, Nietos), member(Y, Nietos)).

abuela(X, Y) :-
    madre(X, Hijos), member(Z, Hijos), (padre(Z, Nietos), member(Y, Nietos); madre(Z, Nietos), member(Y, Nietos)).

hermano(X, Y) :-
    (hijo(Y, [P, M]); hija(Y, [P, M])),
    ((hijo(X, [P, _]); hijo(X, [_, M])); !),
    X \= Y.

hermana(X, Y) :-
    (hijo(Y, [P, M]); hija(Y, [P, M])),
    ((hija(X, [P, _]); hija(X, [_, M])); !),
    X \= Y.

tio(X, Y) :-
    (padre(Z, Hijos), member(Y, Hijos), hermano(X, Z));
    (madre(Z, Hijos), member(Y, Hijos), hermano(X, Z)).

tia(X, Y) :-
    (padre(Z, Hijos), member(Y, Hijos), hermana(X, Z));
    (madre(Z, Hijos), member(Y, Hijos), hermana(X, Z)).

primo(X, Y) :-
    (tia(T, Y); tio(T, Y)), hijo(X, _, [T | _]).

prima(X, Y) :-
    (tia(T, Y); tio(T, Y)), hija(X, _, [T | _]).
