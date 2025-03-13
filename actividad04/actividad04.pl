%Suponemos definida la siguiente base de datos de
%relaciones familiares:
progenitor(clara, jose).
progenitor(tomas, jose).
progenitor(tomas, isabel).
progenitor(jose, ana).
progenitor(jose, patricia).
progenitor(patricia, jaime).

%Ejercicio 1.1
%Dada la base de datos familiar, se pode la respuesta
%de PROLOG y el enunciado verbal de las siguientes
%Preguntas

%?-progenitor(jaime,X).
%R:// De quién es progenitor Jaime?
%
%?-progenitor(X, jaime).
%R:// Quién es el progenitor de Jaime?
%
%?-progenitor(clara,X),progenitor(X,patricia).
%R:// Quién es hijo(a) de clara tal que este sea el
%progenitor de patricia?
%
%?-progenitor(tomas,X)progenitor(X,Y),progenitor(Y,Z).
%R:// Quién es el/la bisnieto(a) de tomas?
%
%----------------------------------------------------
%
%Ejercicio 1.2
%Dada la base de datos familiar del ejemplo 1.1,
%formula en PROLOG las siguientes preguntas:
%
%a)Quién es el progenitor de Patricia?
%R:// ?-progenitor(X, patricia).
%
%b)Tiene isabel un hijo o una hija?
%R:// ?-progenitor(isabel, X).
%
%c)Quien es el abuelo de isabel?
%R:// ?-progenitor(X, isabel),progenitor(Y,X).
%
%d)Cuales son los tios de patricia? (no excluir el
%padre)
%R:// ?-progenitor(patricia,X),progenitor(Y,X),
%       progenitor(Y,Z).
%
%----------------------------------------------------
%
%Ejercicio 1.3
%Dada la base de datos familiar y suponiendo deinidas
%las siguientes clausulas:
hombre(tomas).
hombre(jose).
hombre(jaime).
mujer(clara).
mujer(isabel).
mujer(ana).
mujer(patricia).
dif(X,Y):-X\=Y.
%Donde las primeras 3 clausulas se definirán como
%hechos (por tanto no se podrá poner una variable
%como argumento, ya que una variable haría que el
%hecho fuera cierto para cualquier objeto) y la
%última como regla (donde el simbolo \= significa
%distinto). escribir las reglas de PROLOG que
%expresen las siguientes relaciones:
%
%a) es_madre(X).
es_madre(X):-
    progenitor(X, _), mujer(X), !.
%b) es_padre(X).
es_padre(X):-
    progenitor(X, _), hombre(X), !.
%c) es_hijo(X)
es_hijo(X):-
    progenitor(_, X), !.
%d) hermana_de(X,Y).
hermana_de(X,Y):-
    progenitor(Z, X),
    progenitor(Z, Y),
    mujer(Y),
    dif(X, Y).
%e) abuelo_de(X,Y). y abuela_de(X,Y).
abuelo_de(X, Y):-
    progenitor(Z, X),
    progenitor(Y, Z),
    hombre(Y).
abuela_de(X, Y):-
    progenitor(Z, X),
    progenitor(Y, Z),
    mujer(Y).
%f) hermanos(X,Y). Tener el cuenta que una persona
%no es hermano de si mismo
hermanos(X, Y):-
    progenitor(Z, X),
    progenitor(Z, Y),
    dif(X, Y).
%g) tia(X,Y). Excluir a los padres
tia(X, Y):-
    progenitor(Z, X),
    hermanos(Z, Y).