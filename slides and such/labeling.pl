
:- op(1000,xfx,'<->'),op(1000,xfx,'->'),op(1000,xfx,'<-').

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% LABELING %%% LABELING %%% LABELING %%% LABELING %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


cp(Args, Attacks, Exts):-
	findall((A,B),member(A -> B,Attacks),A1),
	findall((B,A),member(A <- B,Attacks),A2),
	findall([(A,B),(B,A)],member(A <-> B,Attacks),A3),
	flatten(A3,FA3),
	append(A1,A2,A12),
	append(A12,FA3,A4),
	computePreferred((Args,A4), Exts1),
	give_me_in(Exts1,Exts).
	
give_me_in([],[]).
give_me_in([(In,_,_)|Xs],[In|Ins]):-
	give_me_in(Xs,Ins).

computePreferred((A,Att),Extensions):-
  labellings((A,Att),(A,[],[]),[],Extensions),!.

  

labellings(_,(In,_,_),Candidates,Candidates):- %11
  member((C,_,_),Candidates),
  subset(In,C).

labellings(AF,(In,Out,Undec),Candidates,NewCandidates):- %13
  forall(member(X,In),legallyIn(AF,(In,Out,Undec),X)),
  findall((IC,OC,UC),(member((IC,OC,UC),Candidates),subset(IC,In),not(subtract(In,IC,[]))),ToRemove),
  subtract(Candidates,ToRemove,TCand),
  append(TCand,[(In,Out,Undec)],NewCandidates).

labellings(AF,L,Candidates,NewCandidates):- %27
  superIllegallyIn(AF,L,X),
  transitionStep(AF,L,X,NL),
  labellings(AF,NL,Candidates,NewCandidates).

labellings(AF,L,Candidates,NewCandidates):- %31
  findall(X,illegallyIn(AF,L,X),ILIN),
  proceduralLoop(AF,ILIN,L,Candidates,NewCandidates).


%for each X that is illegally IN.... so we need the argument framework AF, the
%List of illegally Ins, the current labelling L, the set of candidates C and
%"return" the new candidates NC
%proceduralLoop(AF,List,L,C,NC):-
%  proceduralLoop(AF,List,L,C,NC).

proceduralLoop(_,[],_,N,N).
proceduralLoop(AF,[H|T],L,O,N):-
  transitionStep(AF,L,H,NL),
  labellings(AF,NL,O,Tmp),
  proceduralLoop(AF,T,L,Tmp,N).
  
transitionStep((_,Att),(In,Out,Undec),X,(NewIn,NewOut,NewUndec)):-
  subtract(In,[X],NewIn),
  append([X],Out,TmpOut),
  findall(A,member((X,A),Att),Attacked),
  append([X],Attacked,PosIlOut),
  findall(O,(member(O,PosIlOut),illegallyOut((_,Att),(NewIn,TmpOut,Undec),O)),IllegalOut),
  subtract(TmpOut,IllegalOut,NewOut),
  append(IllegalOut,Undec,NewUndec).

illegallyOut((_,Att),(In,Out,_),Argument):-
  member(Argument,Out),
  not((member(X,In),member((X,Argument),Att))).

%arg is legally in if it is in and all attacks against it are out
legallyIn((_,Att),(In,Out,_),X):-
   member(X,In),
   forall(member((Y,X),Att),member(Y,Out)). 

illegallyIn((_,Att),(In,Out,_),X):-
  member(X,In),
  not(forall(member((Y,X),Att),member(Y,Out))).

legallyUndec((_,Att),(In,_,Undec),X):-
  member(X,Undec),
  not(member(Y,In),member((Y,X),Att)),
  member(Z,Undec),
  member((Z,X),Att).

superIllegallyIn((_,Att),(In,Out,Undec),Arg):-
  illegallyIn((_,Att),(In,Out,Undec),Arg),
  member(X,In),
  member((X,Arg),Att),
  legallyIn((_,Att),(In,Out,Undec),X).

superIllegallyIn((_,Att),(In,Out,Undec),Arg):-
  illegallyIn((_,Att),(In,Out,Undec),Arg),
  member(X,In),
  member((X,Arg),Att),
  legallyUndec((_,Att),(In,Out,Undec),X).


% EOF