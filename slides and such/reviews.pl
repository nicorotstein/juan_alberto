

get_dynamics([
attrib_count(_,_), argid(_), review(_,_), defids(_), rids(_), multiple_extensions
]).

:- get_dynamics(D),dynamic(D),[labeling,condlabel].


features([
staff, rooms, location, price, comfort, cleanliness
%, concierge, maid, bed, nightstand, breakfast, butler
%, ambience, restaurant, garage, bar
]).

%features([a,b,c,d,e]).


getid(ID):-
	retract(argid(X)),
	I is X+1,
	atom_concat('r',I,ID),
	assert(argid(I)).

opinion(['+','-']).

%activities([
%farming, tourism, timetravel,
%nodding, laughing, transport,
%lodging, brewing, fighting,
%assembling, advising, winking
%]).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% CREATE REVIEWS +AMOUNT OF BUSINESSES, +AMOUNT OF ONTOLOGY RELATIONS %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

cr(QRev):-

	get_dynamics(D),
	forall(member(M,D),retractall(M)),
	assert(argid(0)),
	
writeln('creating reviews'),
	findall(
		Rev,
		(
		 between(1,QRev,I),
		 create_review(I,Rev)
		),
		Revs
	),
	
	flatten(Revs,RevsF),
	list_to_ord_set(RevsF,Args),
writeln('counting attributes'),
	count_attributes(Args,RevsF),
	
	findall(
		Q:Rev,
		(
		 member(Rev,Revs),
		 findall(Sum,(member(A,Rev),attrib_count(Sum,A)),SumQ),
		 sumlist(SumQ,Q)
		),
		RevsQ
	),
	
	findall(
		Q:A,
		(member(A,Args),attrib_count(Q,A)),
		ArgsQ
	),
writeln('finding conflicts'),
	find_hilevel_conflicts(RevsQ,RevDefs),

	find_conflicts(ArgsQ,Defs),
writeln('computing warranted arguments'),
%	cp(Args,Defs,Ws),
%	member(W,Ws),!,
%writeln(aloha),
	cp(RevsQ,RevDefs,RevWs),
	(length(RevWs,LW),LW>1 -> assert(multiple_extensions) ; true),
	member(RevW,RevWs),!,

	findall(RQid,(member(_:RV,RevsQ),review(RQid,RV)),RIDs),
%	findall(Wid,(member(_:RV,RevW),review(Wid,RV)),WIDs),

	findall(Aid -> Bid,(member(_:A -> _:B,RevDefs),review(Aid,A),review(Bid,B)),A1),
	findall(Aid -> Bid,(member(_:B <- _:A,RevDefs),review(Aid,A),review(Bid,B)),A2),
	findall([Aid -> Bid, Bid -> Aid],(member(_:A <-> _:B,RevDefs),review(Aid,A),review(Bid,B)),A3),
	flatten(A3,FA3),
	append(A1,A2,A12),
	append(A12,FA3,RDIDs),
	assert(rids(RIDs)),
	assert(defids(RDIDs)),
%writeln('building conditional labels'),
%	pm(RIDs,RDIDs,CLabels),
%	
%	forall(member(L,CLabels),writeln(L)),
writeln('building visualisation'),
	show(revs,RevsQ,RevDefs,RevW),
	%show(ids,RIDs,RDIDs,WIDs),
	
	findall(X,member(_:X,RevW),RW1),
	flatten(RW1,RWF),
	list_to_ord_set(RWF,AcceptedTruth),
%	writeln('accepted truth: '),
%	forall(
%		member(AT,AcceptedTruth),
%		write_att_and_opposite(AT)),
	
	findall(Q:[O:Sorry],
		member(Q:O:Sorry,ArgsQ),
		ArgsSorry),
	findall(Q1:[O1:Sorry1]<->Q2:[O2:Sorry2],
		member(Q1:O1:Sorry1<->Q2:O2:Sorry2,Defs),
		DefsSorry),
	findall(Q:[Ow:SorryW],
		(member(Ow:SorryW,AcceptedTruth),attrib_count(Q,Ow:SorryW)),
		WSorry),
	show(feats,ArgsSorry,DefsSorry,WSorry),!.
		
		
write_att_and_opposite(Opinion:Feat):-
	attrib_count(Q,Opinion:Feat),write(Q:Opinion:Feat),write(' // '),
	(Opinion = + -> OppOp = - ; OppOp = +),
	(attrib_count(Qopp,OppOp:Feat),writeln(Qopp:OppOp:Feat),! ; writeln(0-OppOp:Feat)).


count_attributes([],_).
count_attributes([A|As],Rs):-
	how_many(A,Rs,Q),
	assert(attrib_count(Q,A)),
	count_attributes(As,Rs).
	
how_many(_,[],0).
how_many(X,[X|Xs],N):-!,how_many(X,Xs,N1),N is N1+1.
how_many(X,[_|Xs],N):-how_many(X,Xs,N).


find_hilevel_conflicts([],[]).
find_hilevel_conflicts([O:R|Revs],RevDefs):-
	findall(
		Def,
		(member(O1:R1,Revs),in_hilevel_conflict(R,R1),get_defeat(O:R,O1:R1,Def)),
		RDtemp
		),	
	find_hilevel_conflicts(Revs,RevDefs1),
	append(RDtemp,RevDefs1,RevDefs).
	
	
get_defeat(O:Rx,O1:Ry,O:Rx->O1:Ry):-O>O1,!.
get_defeat(O:Rx,O1:Ry,O1:Ry->O:Rx):-O<O1,!.	
get_defeat(O:Rx,O:Ry,Def):-
	findall(
		(QX,QY),
		(member(X:Feat,Rx),member(Y:Feat,Ry),X\=Y,
		 attrib_count(QX,X:Feat),attrib_count(QY,Y:Feat)),
		PairSums
	),
	findall(
		X,
		member((X,_),PairSums),
		XSumL),
	sumlist(XSumL,XSum),
	findall(
		Y,
		member((_,Y),PairSums),
		YSumL),
	sumlist(YSumL,YSum),
	get_defeat_direction(XSum,YSum,Arrow),
	Def =.. [Arrow,O:Rx,O:Ry].
%	(Arrow = '<->',length(PairSums,2)->writeln(yeah);true).


get_defeat_direction(N,N,'<->'):-!.
get_defeat_direction(N,M,'->'):-N>M,!.
get_defeat_direction(N,M,'<-'):-N<M.
	

in_hilevel_conflict(Uno,Dos):-
	member(U,Uno),member(D,Dos),
	in_conflict(U,D),!.


find_conflicts([],[]).
find_conflicts([O:A|As],Ds):-
	findall(
		O:A <-> O1:A1,
		(member(O1:A1,As),in_conflict(A,A1)),
		Ds1
	),
	find_conflicts(As,Ds2),
	append(Ds1,Ds2,Ds).
	
in_conflict('+':F,'-':F).
in_conflict('-':F,'+':F).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% CREATION %%% CREATION %%% CREATION %%% CREATION %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

create_review(_Num,Review):-
	pick_random(features,1,2,Features),

	findall(
		O:F,
		(
		 member(F,Features),
		 pick_random(opinion,0,1,[O])
		),
		Review
	),
	
	getid(ID),
	assert(review(ID,Review)).
%	writeln(ID-Review).
	

pick_random(What,LowerLimit,Quantity,Set):-
	List =.. [What,Things],
	List,
	length(Things,Length),
	HowMany is random(Quantity)+LowerLimit,

	findall(
		E,
		(
		 between(0,HowMany,_),
		 En is random(Length),
		 nth0(En,Things,E)
		),
		Set1
	),
	list_to_ord_set(Set1,Set).
	

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% VISUALISATION %%% VISUALISATION %%% VISUALISATION %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

pipe_them([X],X):-!.
pipe_them([A|As],R):-
	pipe_them(As,Rs),
	multi_concat([A,'|',Rs],R).	
	

show(Filename,Args,Defs1,W):-

	list_to_ord_set(Defs1,Defs),
	
	atom_concat(Filename,'.gv',GVFile),
	tell(GVFile),
	write('digraph rev{'),nl,
	write('node[style="roundrectangle,filled" fontname="Sans Serif" fontsize=16];'),nl,
	write('edge[dir=none color=blue arrowsize=1 penwidth=1 fontname="Sans Serif" fontsize=16];'),nl,
%	write('rankdir="LR";'),nl,
%	write('nodesep=0'),nl,

	forall(
		member(O:Attribs,Args),
		(pipe_them(Attribs,Fatts),
		mwritenl(['"',O:Attribs,'" [shape=record label="',O,'|',Fatts,'"];']))
	),
	
	forall(member(Feature,W),mwritenl(['"',Feature,'" [fillcolor=darkgreen,fontcolor=white];'])),
	
	forall(
		member(Feat1->Feat2,Defs),
		mwritenl(['"',Feat1,'" -> "',Feat2,'" [dir=fwd]];'])
	),

	forall(
		member(Feat2<-Feat1,Defs),
		mwritenl(['"',Feat1,'" -> "',Feat2,'" [dir=fwd]];'])
	),

	forall(
		member(Feat1<->Feat2,Defs),
		(
		 mwritenl(['"',Feat1,'" -> "',Feat2,'" [dir=both color=red]];'])
		)
	),

%	write('layout=circo;'),nl,
	write('}'),nl,
	told,

	atom_concat('open /Applications/Graphviz.app --background ',GVFile,CALL),
	shell(CALL).
	

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%% AUXXXXXXXXXXXXX %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

cr_in_lists([],'').
cr_in_lists([L|Ls],LCR):-
	atom_concat('\\n',L,CR),
	cr_in_lists(Ls,LsCR),
	atom_concat(CR,LsCR,LCR).
	
multi_append([],[]).
multi_append([X|Xs],App):-
	multi_append(Xs,Ys),
	append(X,Ys,App).

mwritenl([X]):-write(X),nl,!.
mwritenl([X|Xs]):-write(X),mwritenl(Xs).

multi_concat([],'').
multi_concat([X:Y|Xs],Concat):-
	multi_concat(Xs,Cs),!,
	atom_concat(X,Y,X2),
	atom_concat(X2,Cs,Concat).
multi_concat([X|Xs],Concat):-
	multi_concat(Xs,Cs),
	atom_concat(X,Cs,Concat).




% EOF