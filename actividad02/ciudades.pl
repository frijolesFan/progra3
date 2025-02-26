%----- DEFINICION DE RELACIONES -----%
conexion(vancouver, edmonton, 16).
conexion(vancouver, calgary, 13).
conexion(edmonton, saskatoon, 12).
conexion(calgary, edmonton, 4).
conexion(calgary, regina, 14).
conexion(saskatoon, calgary, 9).
conexion(saskatoon, winnipeg, 20).
conexion(regina, saskatoon, 7).
conexion(regina, winnipeg, 4).

%----- DEFINICION DE REGLAS -----%

tiene_aristas(X) :-
    conexion(X, _, _), !.

costo_nodoXYZ(X, Z, C) :-
    conexion(X, Y, C1), conexion(Y, Z, C2),
    C is C1 + C2.