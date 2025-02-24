nacionalidad(coronel_west, estadounidense).
enemigos(corea_del_sur, estados_unidos).
vende_misiles(coronel_west, corea_del_sur).

criminal(X) :-
    nacionalidad(X, estadounidense),
    enemigos(Y, estados_unidos),
    vende_misiles(X, Y),
    !.
