from writeOnFiles import writeText

#@graph is the graph (matrix) to be displayed
#All these functions write a DOT code

filename,data
#For non-oriented graphs
def graphNO(graph):
    n = len(graph)
    

let grapheno g = 
  let n=Array.length g in
  print "graph g { \n";
  for i=0 to (n-1) do
     let rec affiche liste = match liste with
      |[] -> ()
      |(b,c)::q -> print "%d -- %d [label=%d]; \n" i b c;affiche q
     in affiche g.(i);
  done;print " } \n";;

(* version orientée *)

let grapheo g = 
  let n=Array.length g in
  print "digraph g { \n";
  for i=0 to (n-1) do
     let rec affiche liste = match liste with
      |[] -> ()
      |(b,c)::q -> print "%d -> %d [label=%d]; \n" i b c;affiche q
     in affiche g.(i);
  done; print " } \n";;

(* version avec liste d'arêtes, non orienté *)

let graphelno g =
   print "graph g { \n";
   let rec affiche liste = match liste with
     |[] -> print " } \n"
     |(i,j,poids)::q -> print "%d -- %d [label=%d]; \n" i j poids;affiche q
   in affiche g;;

(* version avec liste d'arêtes, orienté *)

let graphelo g =
   print "digraph g { \n";
   let rec affiche liste = match liste with
     |[] -> print " } \n"
     |(i,j,poids)::q -> print "%d -> %d [label=%d]; \n" i j poids;affiche q
   in affiche g;;
