%DEFINICION DE LOS OPERADORES DEL LENGUAJE
:-op(100,fy,~).
:-op(101,xfy,or).
:-op(102,xfy,and).
:-op(103,xfy,^).
:-op(104,xfx,->).
:-op(105,xfx,<-).


%LETRA(+C), TIENE EXITO SI C ES UNA LETRA PROPOSICIONAL
letra(C):-C\=top,C\=bottom,C\= _ and _, C\= _ or _. %atom(C),atom_chars(C,X),X>=97,X=<122.


%MIN(+F1), TIENE EXITO SI F1 ES TOP, BOTTOM O UNA LETRA PROPOSICIONAL
min(top).
min(bottom).
min(F1):- letra(F1).
min(~F1):-letra(F1).


%FBF(+F), TIENE EXITO SI F ES UN FORMULA BIEN FORMADA DEL LENGUAJE
fbf(top).
fbf(bottom).
fbf(F):-letra(F).
fbf(~F1):-fbf(F1).
fbf(F1 and F2):- fbf(F1),fbf(F2).
fbf(F1 or F2):- fbf(F1),fbf(F2).
fbf(F1 ^ F2):- fbf(F1),fbf(F2).
fbf(F1 -> F2):- fbf(F1),fbf(F2).
fbf(F1 <- F2):- fbf(F1),fbf(F2).


%dnf(+F1,-F2), INSTANCIA F2 CON LA FORMULA F1 TRANSFORMADA A FORMA NORMAL CONJUNTIVA
	%CASOS TRIVIALES
dnf(top,top).
dnf(bottom,bottom).
dnf(F1,F1):-min(F1).
dnf(F1 or F1,F):-dnf(F1,F).

	%CONSIDERACIONES ESPECIALES CON TOP Y BOTTOM
		%OR
/*dnf(_ or top, top):-!.
dnf(top or _, top):-!.
dnf(F1 or bottom, F1):-!.
dnf(bottom or F1, F1):-!.
dnf(F1 or ~F1,top):-!.
dnf(~F1 or F1,top):-!.
		%AND
dnf(F1 and top,F):-dnf(F1,F),!.
dnf(_ and bottom,bottom):-!.
dnf(top and F1,F):-dnf(F1,F),!.
dnf(bottom and _,bottom):-!.
		%NOT
dnf(~(bottom),top).
dnf(~(top),bottom).
*/
	%CONSIDERACIONES ESPECIALES EN LAS QUE F1 O F2 SE REDUCEN A TOP EN UNA CONJUNCION
/*dnf(F1 and F2,E1):-
	dnf(F1,E1),
	dnf(F2,top),
	F1\=top,
	F1\=bottom,
	F2\=top,
	F2\=bottom,
	E1\=top,
	E1\=bottom.
dnf(F1 and F2,E2):-
	dnf(F1,top),
	dnf(F2,E2),
	F1\=top,
	F1\=bottom,
	F2\=top,
	F2\=bottom,
	E2\=top,
	E2\=bottom.*/

	%DEFINICION DE LOS OPERADORES
		%IMPLICANCIA
dnf(F1 -> F2,F):- dnf(~F1 or F2,F).
dnf(F1 <- F2,F):- dnf(F2 -> F1,F). 
		%NOR
dnf(F1 ^ F2, F):- dnf(~(F1 or F2),F).
		%OR
dnf(F1 or F2,E1 or E2):-
	dnf(F1,E1),
	dnf(F2,E2),!.
		%AND
dnf(F1 and F2,E1 and E2):-
	min(F1),
	F2 \= (_ or _),
	dnf(F1,E1),
	dnf(F2,E2),!.
		%NOT
dnf(~(F1->F2),F):-dnf(F1 and ~F2,F).           
dnf(~(F2<-F1),F):-dnf(F1 and ~F2,F).			
dnf(~(~F1),F):-dnf(F1,F).
dnf(~(P or Q),F):-dnf(~P and ~Q,F).
dnf(~(P and Q),F):-dnf(~P or ~Q,F).


	%PROPIEDADES ALGEBRAICAS
		%DISTRIBUTIVA
%dnf(F1 or (F2 and F3),F):-dnf(F1 or F2 and F1 or F3,F).
%dnf((F1 and F2) or F3,F):-dnf(F1 or F3 and F3 or F2,F).
dnf(F1 and (F2 or F3),F):-writeln(dandor(F1,(F2,F3))),
	dnf(F1 and F2 or F1 and F3,F),!.
dnf((F1 or F2) and F3,F):-writeln(dorand((F1,F2),F3)),
	dnf(F1 and F3 or F3 and F2,F),!.
	
		%ASOCIATIVA
dnf((F1 or F2) or F3,E1):-writeln(assoc((F1 or F2) or F3)),
	dnf(F1 or F2 or F3,E1),!.
dnf((F1 and F2) and F3,E1):-writeln(assoc((F1 and F2) and F3)),
	F1\=F2,
	F1\=(~F2),
	F2\=(~F1),
	dnf(F1 and F2 and F3,E1),!.









%FNCR(+X,-H), CHEQUEA LA ENTRADA (VERIFICA QUE SEA FBF) E INSTANCIA A H CON X EN FORMA NORMAL CONJUNTIVA REDUCIDA
fncr(X,H):-
	dnf(X,X),
	reducir(X,H).
fncr(X,F):-
	fbf(X),
	dnf(X,C),
	X\=C,
	fncr(C,F).


%REDUCIR(+F1,-X1), INSTANCIA X1 CON F1 CON SUS CLAUSULAS REDUCIDAS
reducir(F1,X1):-
	F1\=(_ and _),
	paso4(F1,X1).
reducir(F1 and F2,X2):-
	paso4(F1,top),
	reducir(F2,X2).                  
reducir(F1 and F2,X1 and X2):-
	paso4(F1,X1),
	X1\=top,
	reducir(F2,X2).                  

%PASO4(+F1,-X1), RECIBE LA CLAUSULA F1 Y LA REDUCE SEGUN EL ALGORITMO, INSTANCIANDO X1
paso4(F1,F1):-letra(F1).
paso4(~F1,~F1):-letra(F1).
paso4(F1,top):-buscar(top,F1).
paso4(F1 or F2,X2):-
	F1\=top,
	buscar(F1,F2),
	paso4(F2,X2).
paso4(F1 or F2,F1 or X2):-
	F1\=top,
	complemento(F1,C1),
	nobuscar(C1,F2),
	nobuscar(F1,F2),
	paso4(F2,X2),
	X2\=top.
paso4(F1 or F2,top):-
	F1\=top,
	nobuscar(F1,F2),
	paso4(F2,top).
paso4(F1 or F2,top):-
	F1\=top,
	complemento(F1,C1),
	buscar(C1,F2).


%COMPLEMENTO(+F1,-F2), INSTANCIA F2 CON EL COMPLEMENTO DE F1
complemento(~F,F):-letra(F).
complemento(F,~F):-letra(F).


%BUSCAR(+A,+F), TIENE EXITO SI LA LETRA PROPOSICIONAL A ESTA CONTENIDA EN LA CLAUSULA F
buscar(A,A).
buscar(A,A or _).
buscar(A,B or C):-
	A\=B,
	buscar(A,C).


%NOBUSCAR(+A,+F), TIENE EXITO SI LA LETRA PROPOSICIONAL A NO ESTA CONTENIDA EN LA CLAUSULA F
nobuscar(A,B):-
	A\=B,
	B\=(_ or _).
nobuscar(A,B or C):-
	A\=B,
	nobuscar(A,C).


%MODELO(+I,+F), TIENE EXITO SI LA FORMULA F ES MODELO DE LA INTERPRETACION I
modelo(I,F):-
	fncr(F,Fncr),
	evaluar(I,Fncr,1).


%TABLAS DE VERDAD DE LAS FUNCIONES LOGICAS OR, AND Y NOT (0 es falso; 1, verdadero)
%FUNCION[OR|AND](+A,+B,-C)
%FUNCIONNOT(+A,-B)
funcionOr(0,0,0).
funcionOr(0,1,1).
funcionOr(1,0,1).
funcionOr(1,1,1).
funcionAnd(0,0,0).
funcionAnd(0,1,0).
funcionAnd(1,0,0).
funcionAnd(1,1,1).
funcionNot(0,1).
funcionNot(1,0).


%EVALUAR(+I,+F,-V), EVALUA LA FORMULA F CON LA INTERPRETACION I E INSTANCIA V CON EL VALOR LOGICO RESULTANTE
evaluar(_,top,1).
evaluar(I,F,1):-letra(F),
	        pertenece(F,I).
evaluar(I,F,0):-letra(F),
	        nopertenece(F,I).
evaluar(I,F1 or F2,F):-
	evaluar(I,F1,E1),
	evaluar(I,F2,E2),
	funcionOr(E1,E2,F).
evaluar(I,F1 and F2,F):-
	F1\=top,
	F2\=top,
	evaluar(I,F1,E1),
	evaluar(I,F2,E2),
	funcionAnd(E1,E2,F).
evaluar(I,top and F2,F):-
	F2\=top,
	evaluar(I,F2,F).
evaluar(I,F1 and top,F):-
	F1\=top,
	evaluar(I,F1,F).
evaluar(I,~F1,F):-
	evaluar(I,F1,E1),
	funcionNot(E1,F).





%PERTENECE(+X,+L), TIENE EXITO SI LA LETRA PROPOSICIONAL X PERTENECE A LA LISTA L
pertenece(X,[X|_]).
pertenece(X,[Y|T]):-
	X\=Y,
	pertenece(X,T).


%NOPERTENECE(+X,+L), TIENE EXITO SI LA LETRA PROPOSICIONAL X NO PERTENECE A LA LISTA L
nopertenece(_,[]).
nopertenece(X,[Y|T]):-
	Y\=X,
	nopertenece(X,T).


%THE END
