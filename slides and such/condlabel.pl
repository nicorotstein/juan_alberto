
:-[cnf].

%:-op(100,xfx,and),op(101,xfx,or).


pm(Args,Defs,CLabels):-
	argplus(Args,Defs,Plus),
	argminus(Args,Defs,Minus),
	arg_by_arg(Args,Plus,in,PlusLabels),
	arg_by_arg(Args,Minus,out,MinusLabels),
	append(PlusLabels,MinusLabels,CLabels).


arg_by_arg([],[],_,[]).
arg_by_arg([A|As],[S|Ss],What,[L|Ls]):-
	L =.. [What,A,S],
	arg_by_arg(As,Ss,What,Ls).	
	
argplus(A,D,Plus):-
	findall(
		ArgPlus,
		(
			member(Arg,A),
			findplus(Arg,D,[Arg],ArgPlus)
		),
		Plus).

argminus(A,D,Minus):-
	findall(
		ArgMinus,
		(
			member(Arg,A),
			findminus(Arg,D,[Arg],ArgMinus)
		),
		Minus).

	
findplus(Arg,D,Visited,FormattedArg and ArgPlus):-
	latex_format(Arg,accept,FormattedArg),
	findall(
		BargMinus,
		(
			member(Barg->Arg,D),
			get_attackers_minus(Barg,D,Visited,BargMinus)
		),
		ArgPlus1),
	ArgPlus1 \= [],!,
	conjunctive(ArgPlus1,ArgPlus).
	
findplus(Arg,_,_,FArg):-latex_format(Arg,accept,FArg).


get_attackers_minus(Barg,D,Visited,BargMinus):-
	not(member(Barg,Visited)),!,
	findminus(Barg,D,[Barg|Visited],BargMinus).

get_attackers_minus(Barg,_D,_Visited,BargMinus):-	
	latex_format(Barg,reject,FBarg),
	BargMinus = [FBarg].


conjunctive([A],(A)):-!.
conjunctive([],[]).
conjunctive([A|As], A and Bs):-conjunctive(As,Bs).
disjunctive([A],(A)):-!.
disjunctive([],[]).
disjunctive([A|As], A or Bs):-disjunctive(As,Bs).%,append([A],Bs,ABs).


latex_format(X,reject,~X).

latex_format(X,accept,X).
		

get_attackers_plus(Barg,D,Visited,BargMinus):-
	not(member(Barg,Visited)),!,
	findplus(Barg,D,[Barg|Visited],BargMinus).

get_attackers_plus(Barg,_D,_Visited,BargMinus):-	
	latex_format(Barg,accept,FBarg),
	BargMinus = [FBarg].

		
findminus(Arg,D,Visited,FormattedArg or ArgMinus):-
	latex_format(Arg,reject,FormattedArg),
	findall(
		BargMinus,
		(
			member(Barg->Arg,D),
			get_attackers_plus(Barg,D,Visited,BargMinus)
		),
		ArgMinus1),
	ArgMinus1 \= [],!,
	disjunctive(ArgMinus1,ArgMinus).
%	append([FormattedArg],ArgMinus,FargMinus).
	
findminus(Arg,_,_,FArg):-latex_format(Arg,reject,FArg).


simple(W,L):-list2right(L,R),distrib(W,R,S),!,writeall(S).


writeall(L):-forall(member(M,L),writeln(M)).


list2right([],[]).
list2right([L|Ls],Rs):-is_list(L),list2right(L,R),list2right(Ls,Rs1),append(Rs1,[R],Rs).
list2right([L|Ls],[L|Rs]):-not(is_list(L)),list2right(Ls,Rs).


distrib(and,[],[]).
distrib(and,L,L):-
	longest_prefix(L,_,[]),!.
distrib(and,L,X):-
	longest_prefix(L,Pre,Post),
	findall(DPost,(member(DP,Post),distrib(or,DP,DPost)),DPosts),
	findall(
		D,
		(member(DPost,DPosts),member(M,DPost),append(Pre,[M],D)),
	X).
distrib(or,[],[]).
distrib(or,L,L):-
	longest_prefix(L,_,[]),!.
distrib(or,L,X):-
	longest_prefix(L,Pre,Post),
	findall(DPost,(member(DP,Post),distrib(and,DP,DPost)),DPosts),
%	findall(PreDand,(member(Dand,DPosts),append(Pre,Dand,PreDand)),X).
%	trace,do_result(Pre,DPosts,X),
	
	append(Pre,DPosts,X).
%	append(Pre,DPosts,X2),
%	push_down(X2,X).

	
push_down([],[]).
push_down([L|Ls],[L|Xs]):-
	(not(is_list(L)) ; not((member(M,L),is_list(M)))),!,
	push_down(Ls,Xs).
push_down([L|Ls],Xs):-
	push_down(Ls,Lss),
	append(L,Lss,Xs).


do_result(Pre,DPosts,PD):-length(DPosts,1),append(Pre,DPosts,PD),!.
do_result(Pre,DPosts,PDs):-
	findall(
		PD,
		(member(DPost,DPosts),append(Pre,DPost,PD)),
		PDs).

	
longest_prefix(L,Prei,Post):-
	reverse(L,Li),
	append(Post,Pre,Li),
	flatten(Pre,Pre),!,
	reverse(Pre,Prei).

	
%remove(r3)*keep(r7)*remove(r1)+
%%remove(r3)*keep(r7)*keep(r3)+
%remove(r3)*keep(r7)*keep(r2)*remove(r5)+
%%remove(r3)*keep(r7)*remove(r1)+
%%remove(r3)*keep(r7)*keep(r3)+
%remove(r3)*keep(r7)*keep(r2)
%
%[keep(r7),remove(r3),remove(r1)]
%%[keep(r7),remove(r3),keep(r3)]
%[keep(r7),remove(r3),keep(r2)]
%[keep(r7),remove(r3),remove(r5)]
%%[keep(r7),remove(r3),keep(r2)]
	

%disjunct → conjunct
%disjunct → disjunct ∨ conjunct
%conjunct → literal
%conjunct → (conjunct ∧ literal)
%literal → variable
%literal → ¬variable

%in_dnf(F):-is_conj(F),!.
%in_dnf(F+G):-in_dnf(G),is_conj(F),!.
%is_conj(F):-literal(F),!.
%is_conj(F*G):-literal(F),is_conj(G).
%literal(F):-F\=_+_,F\=_*_.
%
%todnf(F,D):-
%	dnf(F,D),in_dnf(D),!.
%todnf(F,D):-
%	dnf(F,D1),
%	todnf(D1,D).


%todnf(F,D):-
%	dnf(F,D1),
%	findall(
%		C,
%		(member(C1,D1),flatten(C1,C)),
%		D).
%
%dnf(keep(X),[keep(X)]):-!.
%dnf(remove(X),[remove(X)]):-!.
%dnf([keep(X)],[keep(X)]):-!.
%dnf([remove(X)],[remove(X)]):-!.
%dnf(X,Y):-X\=_+_,X\=_*_,(is_list(X)->X=Y;Y=[X]),!.
%
%dnf(P+Q,[Pd,Qd]):-dnf(P,Pd),dnf(Q,Qd).
%dnf(P*Q,F):-dnf(P,Pd),dnf(Q,Qd),trace,cartesian(Pd,Qd,F).
%
%cartesian(L1,L2,L):-
%	findall(
%		[M1,M2],
%		(member(M1,L1),member(M2,L2)),
%		L
%	).
%
%xcartesian(P,Q,PQ):-P\=_+_,one(P,Q,PQ),!.
%xcartesian([P,Ps],Qs,[PQ,PQs]):-
%	one(P,Qs,PQ),
%	cartesian(Ps,Qs,PQs).
%
%one(P,Q,[P,Q]):-Q\=_+_,!.
%one(P,Q+Qs,[[P,Q],PQ]):-
%	cartesian(P,Qs,PQ).


%dnf(P+Q,Pd+Qd):-dnf(P,Pd),dnf(Q,Qd).
%dnf(P*Q,F):-dnf(P,Pd),dnf(Q,Qd),cartesian(Pd,Qd,F).
%
%cartesian(P,Q,PQ):-P\=_+_,one(P,Q,PQ),!.
%cartesian(P+Ps,Qs,PQ+PQs):-
%	one(P,Qs,(PQ)),
%	cartesian(Ps,Qs,PQs).
%
%one(P,Q,P*Q):-Q\=_+_,!.
%one(P,Q+Qs,P*Q+PQ):-
%	cartesian(P,Qs,PQ).
	

%remove(r5)+ 
%keep(r2)*remove(r6)*remove(r3)+
%keep(r2)*remove(r6)*keep(r6)+
%keep(r2)*remove(r6)*keep(r2)+ 
%((keep(r3)*remove(r6)*remove(r2))* (keep(r4)*remove(r3))*keep(r6)+ 
%(keep(r3)*remove(r6)*remove(r2))* (keep(r4)*keep(r6))*keep(r6)+ 
%(keep(r3)*remove(r6)*remove(r2))* (keep(r4)*keep(r2)*remove(r6)*remove(r3))*keep(r6))+
%((keep(r3)*remove(r6)*keep(r6))* (keep(r4)*remove(r3))*keep(r6)+ 
%(keep(r3)*remove(r6)*keep(r6))* (keep(r4)*keep(r6))*keep(r6)+ 
%(keep(r3)*remove(r6)*keep(r6))* (keep(r4)*keep(r2)*remove(r6)*remove(r3))*keep(r6))+ 
%(keep(r3)*remove(r6)*keep(r3))* (keep(r4)*remove(r3))*keep(r6)+ 
%(keep(r3)*remove(r6)*keep(r3))* (keep(r4)*keep(r6))*keep(r6)+ 
%(keep(r3)*remove(r6)*keep(r3))* (keep(r4)*keep(r2)*remove(r6)*remove(r3))*keep(r6)	


%setify(X,[X]):-X\=_+_,X\=_*_,!.
%setify(X*Xs,XXs):-!,setify(X,X1),setify(Xs,Xss),append(X1,Xss,XXs).
%setify(X+Xs,[X1,Xss]):-!,setify(X,X1),setify(Xs,Xss).
%
%
%setit(F,S):-
%	setify(F,S1),
%	writeln(setified(S1)),
%	findall(X,(member(M,S1),flatten(M,X)),S).

	


%EOF