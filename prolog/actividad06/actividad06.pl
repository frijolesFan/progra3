%estructura de personas: persona(Nombre, Padre, Madre, Hijos, Genero)

%1a generacion
persona(nombre(abraham), padre(np), madre(nm), hijos([homero, herbert]), genero(m)).
persona(nombre(mona), padre(np), madre(nm), hijos([homero]), genero(f)).

persona(nombre(clancy), padre(np), madre(nm), hijos([marge, patty, selma]), genero(m)).
persona(nombre(jacqueline), padre(np), madre(nm), hijos([marge, patty, selma]), genero(f)).

%2a generacion
persona(nombre(herbert), padre(abraham), madre(nm), hijos(nh), genero(m)).
persona(nombre(homero), padre(abraham), madre(mona), hijos([bart, lisa, maggie]), genero(m)).

persona(nombre(marge), padre(clancy), madre(jacqueline), hijos([bart, lisa, maggie]), genero(f)).
persona(nombre(patty), padre(clancy), madre(jacqueline), hijos(nh), genero(f)).
persona(nombre(selma), padre(clancy), madre(jacqueline), hijos([ling]), genero(f)).

%3a generacion
persona(nombre(bart), padre(homero), madre(marge), hijos(nh), genero(m)).
persona(nombre(lisa), padre(homero), madre(marge), hijos(nh), genero(f)).
persona(nombre(maggie), padre(homero), madre(marge), hijos(nh), genero(f)).

persona(nombre(ling), padre(np), madre(selma), hijos(nh), genero(f)).

%-----%-----%-----%-----%-----% relaciones %-----%-----%-----%-----%-----%

%hijos
hijo(X, Y) :- persona(nombre(X), padre(_), madre(_), hijos(H), genero(_)), H \= nh, member(Y, H),
    persona(nombre(Y), padre(_), madre(_), hijos(_), genero(m)).
hija(X, Y) :- persona(nombre(X), padre(_), madre(_), hijos(H), genero(_)), H \= nh, member(Y, H),
    persona(nombre(Y), padre(_), madre(_), hijos(_), genero(f)).
hijos(X, Y) :- hijo(X, Y); hija(X, Y).

%padres
padre(X, Y) :- persona(nombre(X), padre(Y), madre(_), hijos(_), genero(_)), Y \= np.
madre(X, Y) :- persona(nombre(X), padre(_), madre(Y), hijos(_), genero(_)), Y \= nm.
padres(X, Y) :- padre(X, Y); madre(X, Y).

%abuelos
abuelo(X, Y) :- padres(X, Z), padre(Z, Y).
abuela(X, Y) :- padres(X, Z), madre(Z, Y).
abuelos(X, Y) :- padres(X, Z), padres(Z, Y).

%hermanos
hermano(X, H) :- 
    findall(Y,(padres(X, Z), hijo(Z, Y), X \= Y), Lista),
    sort(Lista, Z),
    member(H, Z).
hermana(X, H) :-
    findall(Y,(padres(X, Z), hija(Z, Y), X \= Y), Lista),
    sort(Lista, Z),
    member(H, Z).
hermanos(X, H) :- hermano(X, H); hermana(X, H).

%tios
tio(X, Y) :- padres(X, Z), hermano(Z, Y).
tia(X, Y) :- padres(X, Z), hermana(Z, Y).
tios(X, Y) :- padres(X, Z), hermanos(Z, Y).
