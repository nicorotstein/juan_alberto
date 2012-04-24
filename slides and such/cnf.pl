%DEFINICION DE LOS OPERADORES DEL LENGUAJE
:-op(100,fy,~).
:-op(101,xfy,or).
:-op(102,xfy,and).
:-op(103,xfy,^).
:-op(104,xfx,=>).
:-op(105,xfx,<=).


%LETRA(+C), TIENE EXITO SI C ES UNA LETRA PROPOSICIONAL
letra(C):-C\=top,C\=bottom,atom(C),C\= (_ or _),C\= (_ and _).%atom_chars(C,X),X>=97,X=<122.


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
fbf(F1 => F2):- fbf(F1),fbf(F2).
fbf(F1 <= F2):- fbf(F1),fbf(F2).


%NORMALC(+F1,-F2), INSTANCIA F2 CON LA FORMULA F1 TRANSFORMADA A FORMA NORMAL CONJUNTIVA
	%CASOS TRIVIALES
normalC(top,top).
normalC(bottom,bottom).
normalC(F1,F1):-F1\=top,F1\=bottom,min(F1).
normalC(F1 or F1,F1).
	%DEFINICION DE LOS OPERADORES
		%IMPLICANCIA
normalC(F1 => F2,F):- normalC(~F1 or F2,F).
normalC(F1 <= F2,F):- normalC(F2 => F1,F). 
		%NOR
normalC(F1 ^ F2, F):- normalC(~(F1 or F2),F).
		%OR
normalC(F1 or F2,E1 or E2):-
	F1\=F2,
	F1\=(~F2),F2\=(~F1),
	F2\=(F3 and F4),
	F1\=(F3 and F4),
	F1\=(F3 or F4), 
	F1\=top,
	F2\=top,	
	normalC(F1,E1),
	normalC(F2,E2).
		%AND
normalC(F1 and F2,E1 and E2):-
	F1\=(_F3 and _F4),
	normalC(F1,E1),
	normalC(F2,E2),
	F1\=top,
	F1\=bottom,
	F2\=top,
	F2\=bottom,
	E1\=top,
	E1\=bottom,
	E2\=top,
	E2\=bottom.
		%NOT
normalC(~(F1=>F2),F):-normalC(F1 and ~F2,F).           
normalC(~(F2<=F1),F):-normalC(F1 and ~F2,F).			
normalC(~(~F1),F):-normalC(F1,F).
normalC(~(P or Q),F):-normalC(~P and ~Q,F).
normalC(~(P and Q),F):-normalC(~P or ~Q,F).
	%CONSIDERACIONES ESPECIALES CON TOP Y BOTTOM
		%OR
normalC(_F1 or top, top).
normalC(top or F1, top):-F1\=top.
normalC(F1 or bottom, F1).
normalC(bottom or F1, F1):-F1\=bottom.
normalC(F1 or ~F1,top).
normalC(~F1 or F1,top).
		%AND
normalC(F1 and top,F):-normalC(F1,F).
normalC(_F1 and bottom,bottom).%:-normalC(F1,F).
normalC(top and F1,F):-F1\=top,normalC(F1,F).
normalC(bottom and F1,bottom):-F1\=bottom.%,normalC(F1,F).
		%NOT
normalC(~(bottom),top).
normalC(~(top),bottom).
	%PROPIEDADES ALGEBRAICAS
		%DISTRIBUTIVA
normalC(F1 or (F2 and F3),F):-normalC(F1 or F2 and F1 or F3,F).
normalC((F1 and F2) or F3,F):-normalC(F1 or F3 and F3 or F2,F).
		%ASOCIATIVA
normalC((F1 or F2) or F3,E1):-normalC(F1 or F2 or F3,E1).
normalC((F1 and F2) and F3,E1):-
	F1\=F2,
	F1\=(~F2),
	F2\=(~F1),
	normalC(F1 and (F2 and F3),E1).
	%CONSIDERACIONES ESPECIALES EN LAS QUE F1 O F2 SE REDUCEN A TOP EN UNA CONJUNCION
normalC(F1 and F2,E1):-
	normalC(F1,E1),
	normalC(F2,top),
	F1\=top,
	F1\=bottom,
	F2\=top,
	F2\=bottom,
	E1\=top,
	E1\=bottom.
normalC(F1 and F2,E2):-
	normalC(F1,top),
	normalC(F2,E2),
	F1\=top,
	F1\=bottom,
	F2\=top,
	F2\=bottom,
	E2\=top,
	E2\=bottom.



%FNCR(+X,-H), CHEQUEA LA ENTRADA (VERIFICA QUE SEA FBF) E INSTANCIA A H CON X EN FORMA NORMAL CONJUNTIVA REDUCIDA
fncr(X,H):-
	normalC(X,X),
	reducir(X,H).
fncr(X,F):-
	fbf(X),
	normalC(X,C),
	X\=C,
	fncr(C,F).


%REDUCIR(+F1,-X1), INSTANCIA X1 CON F1 CON SUS CLAUSULAS REDUCIDAS
reducir(F1,X1):-
	F1\=(_F2 and _F3),
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
buscar(A,A or _C).
buscar(A,B or C):-
	A\=B,
	buscar(A,C).


%NOBUSCAR(+A,+F), TIENE EXITO SI LA LETRA PROPOSICIONAL A NO ESTA CONTENIDA EN LA CLAUSULA F
nobuscar(A,B):-
	A\=B,
	B\=(_C or _D).
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
evaluar(_I,top,1).
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
pertenece(X,[X|_T]).
pertenece(X,[Y|T]):-
	X\=Y,
	pertenece(X,T).


%NOPERTENECE(+X,+L), TIENE EXITO SI LA LETRA PROPOSICIONAL X NO PERTENECE A LA LISTA L
nopertenece(_X,[]).
nopertenece(X,[Y|T]):-
	Y\=X,
	nopertenece(X,T).


%THE END
