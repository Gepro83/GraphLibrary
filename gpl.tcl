#
# My Graph Library implementation in NX/Tcl
#
# Georg Prohaska h0325904@wu.ac.at
#
# How to run: `tclsh gpl.tcl` or `tclkit gpl.tcl`
#


#
# Prerequisites
#

package require nx
package require tcltest

namespace eval ::Base {
    #
    # Begin of my implementation
    # ---------------%<------------------
    #
    #"Constants"
    
    set NEIGHBOUR neighbour
    set EDGE edge
	set DFS dfs
	set BFS bfs
    
    nx::Class create Node {
    	:property -accessor public {neighbours:0..* {}}
    	
    	:public method addNeighbour {neighbour:object,type=::Base::Neighbour,required} {
    		lappend :neighbours $neighbour
    	}
    }
    
    nx::Class create Neighbour {
    	:property -accessor public opposite:object,type=::Base::Node,required
    }
    
    nx::Class create WeightedNeighbour -superclass Neighbour {
    	:property -accessor public weight:double,required
    }
    
    nx::Class create Edge {
    	:property -accessor public a:object,type=::Base::Node,required
    	:property -accessor public b:object,type=::Base::Node,required
    }
    
    nx::Class create WeightedEdge -superclass Edge {
    	:property -accessor public weight:double,required
    }

	#Manages the apropriate data structure (queue and stack) for BFS/DFS graph traversal
	nx::Class create TraversalStore {
			:variable store {}
			:property -accessor public [list traversalMode:modes $Base::DFS] {
    		:object method type=modes {prop value} {
	    		set validOpts [list $Base::DFS $Base::BFS]
	    		if {$value ni $validOpts} {
	    			return -code error "'$value' is not a valid for '[namespace tail [self]]', available are: ::Base::DFS, ::Base::BFS"
	    		}
	    		return
			}
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set r [:value=get $obj $prop]
				}
				return $r
			}
		}
		#add item to the store
		:public method add {item} {
			lappend :store $item
		}
		#get and remove the proper item from the store
		:public method get {} {
			if {[:empty]} { return "" }
			if {${:traversalMode} eq $Base::DFS} {
				set lastIndex [expr {[llength ${:store}] - 1}]
				set lastItem [lindex ${:store} $lastIndex]
				#delete last item
				set :store [lreplace ${:store} $lastIndex $lastIndex]
				return $lastItem
			} else {
				set firstItem [lindex ${:store} 0]
				#delete frist item
				set :store [lreplace ${:store} 0 0]
				return $firstItem
			}
		}
		#checks whether store is empty
		:public method empty {} {
			if {[llength ${:store}]} {
				return false
			} else {
				return true
			}
		}
	}
    
    nx::Class create Graph {
		#edges is a read only property
    	:property -accessor public {edges:0..* {}} {
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set r [:value=get $obj $prop]
				}
				return $r
			}
			#in neighbour representation the edge-list is recomputed for every read (so we dont keep both in memory all the time)
			:public object method value=get {obj prop} {
				if {[$obj representation get] eq $::Base::EDGE} {
					set r [next]
				} else {
					set edges {}
					set visited {}
					foreach node [$obj nodes get] {
						foreach neighbour [$node neighbours get] {
							if {[$neighbour opposite get] in $visited} { continue }
							if {[$obj weighted get]} {
								set newEdge [::Base::WeightedEdge new -a $node -b [$neighbour opposite get] -weight [$neighbour weight get]]
							} else {
								set newEdge [::Base::Edge new -a $node -b [$neighbour opposite get] -weight [$neighbour weight get]]
							}
							lappend edges $newEdge
							if {![$obj directed get]} { lappend visited $node }
						}
					}
					set r $edges
				}
				return $r
			}
		}
   	    :property -accessor public {nodes:0..* {}}
    	:property -accessor public {directed:boolean false} {
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set r [:value=get $obj $prop]
				}
				return $r
				}
		}
    	:property -accessor public {weighted:boolean false} {
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set r [:value=get $obj $prop]
				}
				return $r
				}
		}
    	:property -accessor public {printable:boolean true} {
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set r [:value=get $obj $prop]
				}
				return $r
			}
		}
    	:property -accessor public [list representation:representations $Base::EDGE] {
    		:object method type=representations {prop value} {
	    		set validOpts [list $::Base::NEIGHBOUR $::Base::EDGE]
	    		if {$value ni $validOpts} {
	    			return -code error "'$value' is not a valid for '[namespace tail [self]]', available are: ::Base::NEIGHBOUR, ::Base::EDGE"
	    		}
	    		return
			}
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set r [:value=get $obj $prop]
				}
				return $r
			}
		}
		:property -accessor public [list traversal:modes {}] {
    		:object method type=modes {prop value} {
	    		set validOpts [list $Base::DFS $Base::BFS ""]
	    		if {$value ni $validOpts} {
	    			return -code error "'$value' is not a valid for '[namespace tail [self]]', available are: ::Base::DFS, ::Base::BFS, {}"
	    		}
	    		return
			}
		} 
    	:property -accessor public {MST:boolean false} {
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set r [:value=get $obj $prop]
				}
				return $r
				}
		}
		:property -accessor public {SSSP:boolean false} {
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set r [:value=get $obj $prop]
				}
				return $r
				} 
		}
 		:public method numEdges {} {
 			if {${:representation} eq $::Base::EDGE} {
 				return [llength ${:edges}]
 			} elseif {${:representation} eq $::Base::NEIGHBOUR} {
				set edgeCounter 0
				foreach node ${:nodes} {
					incr edgeCounter [llength [$node neighbours get]]
				}
				if {!${:directed}} {
					return [expr {$edgeCounter / 2}]
				} else {
					return $edgeCounter
				}
 			} else {
				 error "Unknown representation!"
			 }
		}
		:public method size {} {
			return [llength ${:nodes}]
		}
		
		:public method nodeID {node:object,type=::Base::Node,required} {
			return [lsearch -exact ${:nodes} $node] 
		}
		#returns an edge object (the internal object if the graph-representatio is an edge-list) between node1 and node2, "" if it does not exist in the graph
		#in directed graphs this checks for edges from node1 to node2
		:public method edge {
			node1:object,type=::Base::Node,required
    		node2:object,type=::Base::Node,required} {
			if {$node1 ni ${:nodes} || $node2 ni ${:nodes}} { return "" }
			if {${:representation} eq $::Base::NEIGHBOUR} {
				foreach neighbour [$node1 neighbours get] {
					if {[$neighbour opposite get] eq $node2} {
						if {${:weighted}} {
							return [WeightedEdge new -a $node1 -b [$neighbour opposite get] -weight [$neighbour weight get]]
						} else {
							return [Edge new -a $node1 -b [$neighbour opposite get]]
						}
					}
				}
				return ""
			} elseif {${:representation} eq $::Base::EDGE} {
				foreach edge ${:edges} {
					if {[$edge a get] eq $node1 && [$edge b get] eq $node2} {
						return $edge
					}
					if {!${:directed}} {
						if {[$edge a get] eq $node2 && [$edge b get] eq $node1} {
							return $edge
						}	
					}
				}
				return ""
			} else {
				error "Unknown representation!"
			}
		}
		#add an edge
		#in digraphs the direction is from newNode1 to newNode2
        #only non-negative weights are allowed
    	:public method add {
    		m:object,type=::Base::Node,required
    		n:object,type=::Base::Node,required
    		weight:double,optional
    	} {
    		if {${:weighted}} {
				if {[info exists weight]} {
					if {$weight < 0} {
						error "Expected positive weight"
					}	
				} else {
					error "Expected weighted edge"
				}
			} else {
				set weight ""
			}
			#use different method for neighbour representation
			if {${:representation} eq $::Base::NEIGHBOUR} {
				return [: -local addNeighbourEdge $m $n $weight]
			}
			#check for double edges
			foreach edge ${:edges} {
				if {[$edge a get] eq $m && [$edge b get] eq $n} {
 					return $edge
 				}
 				if {!${:directed}} {
					if {[$edge a get] eq $n && [$edge b get] eq $m} {
						return $edge
					}
 				}
 			}
 			#add edge
 			if {${:weighted}} {
 				set e [WeightedEdge new -a $m -b $n -weight $weight]
 			} else {
				set e [Edge new -a $m -b $n]
 			}
 			
 			lappend :edges $e
 			#add nodes
 			: -local addNode $m
 			: -local addNode $n 			
 			return $e
 		}
 		
 		:private method addNode {node:object,type=::Base::Node,required} {
 			#only add nodes that do not exist in the graph yet
 			if {$node ni ${:nodes}} {
 				lappend :nodes $node
 			}
 		}
 		
 		:private method addNeighbourEdge {
 			m:object,type=::Base::Node,required
    		n:object,type=::Base::Node,required
    		weight:required 
    	} {
    		#check if edge already exists
    		foreach neighbour [$m neighbours get] {
    			if {[$neighbour opposite get] eq $n} {
    				: -local addNode $m
    				: -local addNode $n
    				return $neighbour
    			}
    		}
    		: -local addNode $m
    		: -local addNode $n
    		#add neighbours
    		set mNeighbour [: -local addNeighbour $m $n $weight]
    		if {!${:directed}} {
    			: -local addNeighbour $n $m $weight
    		}
    		return $mNeighbour
    	}
    	
    	#adds the correct type of neighbour object to the node
    	:private method addNeighbour {
 			m:object,type=::Base::Node,required
    		n:object,type=::Base::Node,required
    		weight:required
    	} {
    		if {${:weighted}} {
    			set mNeighbour [WeightedNeighbour new -opposite $n -weight $weight] 
    			$m addNeighbour $mNeighbour
    		} else {
    			set mNeighbour [Neighbour new -opposite $n] 
    			$m addNeighbour $mNeighbour
    		}
    		return $mNeighbour
    	}
 		
 		:public method DOTprint {} {
 			if {!${:printable}} {
 				error "Unprintable graph!"
 			}
 			#start a graph
 			if {${:directed}} {
 				set DOTstring "digraph g\{
node\[label=\"\"\];
"
			} else {
				set DOTstring "graph g\{
node\[label=\"\"\];
"
			}
			if {${:representation} eq $::Base::EDGE} {
				append DOTstring [: -local DOTedges]
			} elseif {${:representation} eq $::Base::NEIGHBOUR} {
				append DOTstring [: -local DOTneighbour]
			}
			#finish graph
			append DOTstring "\}"
			return $DOTstring
 		}
 		
 		#returns a string containing dot syntax of the edges in edge representation
 		:private method DOTedges {} {
 			set DOTstring ""
 			foreach edge ${:edges} {
				#add the edge to the dotstring
				if {${:weighted}} {
					append DOTstring [: -local singleDOTedge [$edge a get] [$edge b get] [$edge weight get]]
				} else {
					append DOTstring [: -local singleDOTedge [$edge a get] [$edge b get]]
				}
			}
			return $DOTstring
 		}
 		
 		#returns a string containing dot syntax of the edges in neighbour representation
 		:private method DOTneighbour {} {
 			set DOTstring ""
 			set visited {}
 			foreach node ${:nodes} {
 				if {${:directed}} {
 					foreach neighbour [$node neighbours get] {
 						if {${:weighted}} {
 							append DOTstring [: -local singleDOTedge $node \
 							[$neighbour opposite get] [$neighbour weight get]]
 						} else {
 							append DOTstring [: -local singleDOTedge $node [$neighbour opposite get]]
 						}
 					}
 				} else {
 					foreach neighbour [$node neighbours get] {
 						if {[$ neighbour opposite get] in $visited} {
 							continue
 						}
 						if {${:weighted}} {
 							append DOTstring [: -local singleDOTedge $node \
 							[$neighbour opposite get] [$neighbour weight get]]
 						} else {
 							append DOTstring [: -local singleDOTedge $node [$neighbour opposite get]]
 						}
 					}
 				}
 				lappend visited $node
 			}
 			return $DOTstring
 		}
 		
 		#returns the correct DOT representation for the current graph of a single edge
 		#followed by a linebreak
 		:private method singleDOTedge {
 			node1:object,type=::Base::Node,required
    		node2:object,type=::Base::Node,required
    		weight:optional 
    	} {
    		#the names of the nodes are the index in the nodeslist in the graph
    		set edgeString [:nodeID $node1]
    		if {${:directed}} {
    			append edgeString " -> "
    		} else {
    			append edgeString " -- "
    		}
    		append edgeString [:nodeID $node2]
    		
    		if {${:weighted}} {
    			append edgeString " \[ label = \"" $weight "\" ];"
    		}
    		append edgeString "\n"
    		return $edgeString
    	}
		#uses the selected search algorithm to determine wether goalNode can be reached from startNode
        #throws exception if nodes are not part of the graph
		:public method search {
			startNode:object,type=::Base::Node,required
    		goalNode:object,type=::Base::Node,required
		} {
			if {${:traversal} eq ""} {
				error "Traversal mode currently turned off!"
			}
			if {$startNode ni ${:nodes} || $goalNode ni ${:nodes}} {
				error "Either start or goal are not part of this grap!"
			}
			#initialise suitable data structure and add startNode
			set visited {}
			set store [::Base::TraversalStore new -traversalMode ${:traversal}]
			$store add $startNode
			lappend visited $startNode

			while {![$store empty]} {
				set node [$store get]
				if {$node eq $goalNode} { return true }

				foreach neighbour [: getNeighbourhood $node] {
					if {$neighbour ni $visited} {
						$store add $neighbour
						lappend visited $neighbour
					}
				}
			}
			return false
		}
		#returns a list of all nodes that are adjacent to node
		:public method getNeighbourhood {node:object,type=::Base::Node,required} {
			if {$node ni ${:nodes}} { error "Node not in graph!" }

			set neighbourhood {}
			if {${:representation} eq $::Base::EDGE} {
				foreach edge ${:edges} {
					if {[$edge a get] eq $node} {
						lappend neighbourhood [$edge b get]
					} elseif {[$edge b get] eq $node} {
						#directed edges point from a to b
						if {!${:directed}} {
							lappend neighbourhood [$edge a get]
						}
					}
				}
			} elseif {${:representation} eq $::Base::NEIGHBOUR} {
				foreach neighbour [$node neighbours get] {
					lappend neighbourhood [$neighbour opposite get]
				}
			} else {
				error "Unknown representation!"
			}
			return $neighbourhood
		}
		#returns a Graph object containing the minimum spanning tree of this object, will throw an exception if Graphtype is wrong             
		:public method MST {} {
			if {${:MST}} {
				set alg [::Base::MST new -graph [self]]
				return [$alg execute]
			} else {
				error "MST disabled for this graph"
			}
		}
		#returns a Graph object containing a directed tree rooted at the startnode. The edges represent the shortest path between the source and each node (weights stay the same)
        :public method SSSP {start:object,type=::Base::Node,required} {
			if {${:SSSP}} {
				set alg [::Base::SSSP new -graph [self]]
				return [$alg execute $start]
			} else {
				error "SSSP disabled for this graph"
			}
		}
	}
	#class for the MST algorithm, uses kruskals algorithm 
	nx::Class create MST {
		:property -accessor public graph:object,type=::Base::Graph,required {
			:public object method value=set {obj prop value} {
				if {[$value directed get] || ![$value weighted get]}  {
					error "MST works only for undirected weighted graphs"
				}
				return [next]
			}
		}
		:variable parent [dict create]
		:variable rank [dict create]

		:private method makeSet {node} {
			dict set :parent $node $node
			dict set :rank $node 0
		}
		:private method find {node} {
			if {[dict get ${:parent} $node] ne $node} {
				dict set :parent $node [: -local find [dict get ${:parent} $node]]
			}
			return [dict get ${:parent} $node]
		}
		:private method union {node1 node2} {
			set root1 [: -local find $node1]
			set root2 [: -local find $node2]

			if {$root1 eq $root2} { return }

			if {[dict get ${:rank} $root1] < [dict get ${:rank} $root2]} {
				dict set :parent $root1 $root2
			} elseif {[dict get ${:rank} $root1] > [dict get ${:rank} $root2]} {
				dict set :parent $root2 $root1
			} else {
				dict set :parent $root2 $root1
				dict set :rank $root1 [expr {[dict get ${:rank} $root1] + 1}]
			}
		}
		:public method execute {} {
			foreach node [${:graph} nodes get] {
				: -local makeSet $node
			}
			set mst [::Base::Graph new -directed false -weighted true -traversal $::Base::DFS]
			proc compareEdges {e1 e2} {
				if {[$e1 weight get] < [$e2 weight get]} { return -1}
				if {[$e1 weight get] > [$e2 weight get]} { return 1}
				return 0
			}
			foreach edge [lsort -command compareEdges [${:graph} edges get]] {
				if {[: -local find [$edge a get]] ne [: -local find [$edge b get]]} {
					: -local union [$edge a get] [$edge b get]
					$mst add [$edge a get] [$edge b get] [$edge weight get]
				}
			}
			return $mst
		}
	}
	#class for SSSP, uses Dijkstras algorithm
	nx::Class create SSSP {
		:property -accessor public graph:object,type=::Base::Graph,required {
			:public object method value=set {obj prop value} {
				if {![$value directed get] || ![$value weighted get]}  {
					error "SSSP works only for directed weighted graphs"
				}
				return [next]
			}
		}
		:public method execute {start:object,type=::Base::Node,required} {
			#Dijkstra
			set dist [dict create]
			set prev [dict create]
			set Q {}

			foreach node [${:graph} nodes get] {
				dict set dist $node Inf
				dict set prev $node ""
				lappend Q $node
			}
			dict set dist $start 0

			proc sortDictByValue {dict args} {
				set lst {}
				dict for {k v} $dict {lappend lst [list $k $v]}
				return [concat {*}[lsort -index 1 {*}$args $lst]]
			}

			while {[llength $Q] != 0} {
				set dist [sortDictByValue $dist]
				set i 0
				while {true} {
					set node [lindex $dist $i]
					incr i
					set nodeIndex [lsearch -exact $Q $node]
					if {$nodeIndex != -1} { break }
				}
				set Q [lreplace $Q $nodeIndex $nodeIndex]

				foreach neighbour [${:graph} getNeighbourhood $node] {
					set wEdge [${:graph} edge $node $neighbour]
					set alt [expr {[dict get $dist $node] + [$wEdge weight get]}]
					if {$alt < [dict get $dist $neighbour]} {
						dict set dist $neighbour $alt
						dict set prev $neighbour $node
					}
				}
			}
			#Create graph from dist and prev
			set G [::Base::Graph new -directed true -weighted true -traversal $::Base::DFS]
			dict for {node previous} $prev {
				if {$previous eq ""} { continue }
				set wEdge [${:graph} edge $previous $node]
				$G add [$wEdge a get] [$wEdge b get] [$wEdge weight get]
			}

			return $G
		}
	}
    # 
    # ---------------%<------------------
    # End of my implementation
    #
}

#
# Test suite
#

namespace eval ::Base::Test {
    namespace import ::tcltest::*
    #
    # Acceptance tests
    #
    test test-1 {} -body {
        nx::Class info instances ::Base::Graph
    } -result {::Base::Graph}
    test test-2 {} -body {
	nx::Class info instances ::Base::Edge
    } -result {::Base::Edge}
    test test-3 {} -body {
	nx::Class info instances ::Base::Node
    } -result {::Base::Node}
    test test-4 {} -constraints {[info commands ::Base::Graph] ne ""} -body {
	::Base::Graph info methods add
    } -result {add}
    
    #
    # Begin of my tests
    # See also http://www.tcl.tk/man/tcl/TclCmd/tcltest.htm
    # ---------------%<------------------

    test doubleedges {} -body {
    	set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set n3 [::Base::Node new]
    	set n4 [::Base::Node new]
    	
    	set G [::Base::Graph new]
    	
    	$G add $n1 $n2
    	$G add $n2 $n1
    	$G add $n2 $n3
    	$G add $n3 $n4
    	$G add $n3 $n2
    	$G numEdges
    }  -result {3}
    
    test doublenodes {} -body {
    	set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set n3 [::Base::Node new]
    	set n4 [::Base::Node new]
    	
    	set G [::Base::Graph new]
    	
    	$G add $n1 $n2
    	$G add $n2 $n1
    	$G add $n2 $n3
    	$G add $n3 $n4
    	$G add $n3 $n2
    	$G size
    }  -result {4}
    
    test DOTprinterStep1 {} -body {
    	#create graph from assignment
    	set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set n3 [::Base::Node new]
    	set n4 [::Base::Node new]
    	set n5 [::Base::Node new]
    	set n6 [::Base::Node new]
    	set n7 [::Base::Node new]
    	set n8 [::Base::Node new]
    	
    	set G [::Base::Graph new]
    	
    	$G add $n1 $n2
    	$G add $n1 $n3
    	$G add $n1 $n4
    	$G add $n1 $n5
    	$G add $n5 $n6
    	$G add $n5 $n7
    	$G add $n5 $n8
    	
    	puts [$G DOTprint]
    	$G DOTprint
    } -result {graph g{
node[label=""];
0 -- 1
0 -- 2
0 -- 3
0 -- 4
4 -- 5
4 -- 6
4 -- 7
}}
	test exactGraphNoPrint {} -body {
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set n3 [::Base::Node new]
    	set n4 [::Base::Node new]
    	set n5 [::Base::Node new]
    	set n6 [::Base::Node new]
    	set n7 [::Base::Node new]
    	set n8 [::Base::Node new]
    	
    	set G [::Base::Graph new -printable false]
    	
    	$G add $n1 $n2
    	$G add $n1 $n3
    	$G add $n1 $n4
    	$G add $n1 $n5
    	$G add $n5 $n6
    	$G add $n5 $n7
    	$G add $n5 $n8
    	
    	set result [$G size]
    	append result [$G numEdges]
		set result
	} -result {87}
    
	test weightedE {} -body {
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set G [::Base::Graph new -weighted true]
    	[$G add $n1 $n2 3] info class
	} -result {::Base::WeightedEdge}
	
	test weightedN {} -body {
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set G [::Base::Graph new -weighted true -representation $::Base::NEIGHBOUR]
    	[$G add $n1 $n2 3] info class
	} -result {::Base::WeightedNeighbour}
	
	test unweightedE {} -body {
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set G [::Base::Graph new]
    	[$G add $n1 $n2] info class
	} -result {::Base::Edge}
	
	test unweightedN {} -body {
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set G [::Base::Graph new -representation $::Base::NEIGHBOUR]
    	[$G add $n1 $n2] info class
	} -result {::Base::Neighbour}
	
	test directedWeightedEdgeRepr {} -body {
    	set n3 [::Base::Node new]
    	set n4 [::Base::Node new]
    	set n5 [::Base::Node new]
    	set n6 [::Base::Node new]
    	set n7 [::Base::Node new]
    	set n8 [::Base::Node new]
    	
    	set G [::Base::Graph new -directed true -representation $::Base::EDGE -weighted true]
    	$G add $n1 $n2 1
    	$G add $n2 $n3 4
    	$G add $n2 $n4 5
    	$G add $n2 $n5 1
    	$G add $n6 $n5 10
    	$G add $n5 $n7 2
    	$G add $n5 $n8 7
    	
    	set result [catch {$G add $n3 $n2}]
    	append result [$G DOTprint]
    } -result {1digraph g{
node[label=""];
0 -> 1 [ label = "1" ];
1 -> 2 [ label = "4" ];
1 -> 3 [ label = "5" ];
1 -> 4 [ label = "1" ];
5 -> 4 [ label = "10" ];
4 -> 6 [ label = "2" ];
4 -> 7 [ label = "7" ];
}}

	test neighbourRepr {} -body {
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	
    	set G [::Base::Graph new -directed true -representation $::Base::NEIGHBOUR -weighted true]
    	set e1 [$G add $n1 $n2 1]
    	set e2 [$G add $n1 $n2 2]
    	set e3 [$G add $n2 $n1 3]

		set result [expr {$e1 eq $e2}]
    	append result [expr {$e2 ne $e3}]
		append result [expr {[$G size] == 2}]
    	
    	#undirected
    	set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	
    	set G [::Base::Graph new -representation $::Base::NEIGHBOUR -weighted true]
    	set e1 [$G add $n1 $n2 2]
    	set e2 [$G add $n2 $n1 4]
    	
    	append result [expr {[$e2 opposite get] eq $n1}]
    	append result [expr {[$G size] == 2}]
		append result [expr {[$e1 weight get] == 2}]
	} -result {111111}
	
	test directedWeightedNeighbourRepr {} -body {
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set n3 [::Base::Node new]
    	set n4 [::Base::Node new]
    	set n5 [::Base::Node new]
    	set n6 [::Base::Node new]
    	set n7 [::Base::Node new]
    	set n8 [::Base::Node new]
    	
    	set G [::Base::Graph new -directed true -representation $::Base::NEIGHBOUR -weighted true]
    	$G add $n1 $n2 1
    	$G add $n2 $n3 4
    	$G add $n2 $n4 5
    	$G add $n2 $n5 1
    	$G add $n6 $n5 10
    	$G add $n5 $n7 2
    	$G add $n5 $n8 7
		
		set result [catch {$G add $n3 $n2}]
    	append result [$G DOTprint]
	} -result {1digraph g{
node[label=""];
0 -> 1 [ label = "1" ];
1 -> 2 [ label = "4" ];
1 -> 3 [ label = "5" ];
1 -> 4 [ label = "1" ];
4 -> 6 [ label = "2" ];
4 -> 7 [ label = "7" ];
5 -> 4 [ label = "10" ];
}}
	test unprintableGraph {} -body {
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	
    	set G [::Base::Graph new -printable false]
    	$G add $n1 $n2
    	$G add $n2 $n3
		catch {$G DOTprint}
	} -result {1}
	
	test setfixedParams {} -body {
		set G [::Base::Graph new -directed true -representation $::Base::NEIGHBOUR -weighted true -printable true]
		set result [$G directed set false]
		append result [$G representation set $::Base::EDGE]
		append result [$G weighted set false]
		append result [$G printable set false]
	} -result [string cat true $::Base::NEIGHBOUR true true]

	test numEdges {} -body {
		set G [::Base::Graph new -directed true -representation $::Base::NEIGHBOUR]
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
		set n3 [::Base::Node new]
    	set n4 [::Base::Node new]
		$G add $n1 $n2
		$G add $n2 $n1
		$G add $n2 $n3
		$G add $n3 $n4
		$G add $n4 $n3
		$G numEdges
	} -result {5}

	test traversalStore {} -body {
		set result [catch {::Base::TraversalStore new -traversalMode 3}]
		
		set S [::Base::TraversalStore new -traversalMode $::Base::DFS]
		$S add a
		$S add b
		$S add c
		
		append result [$S empty]
		append result [$S get]
		append result [$S get]
		append result [$S get]
		append result [$S empty]

		set S [::Base::TraversalStore new -traversalMode $::Base::BFS]
		$S add a
		$S add b
		$S add c
		
		append result [$S get]
		append result [$S get]
		append result [$S get]
		
	} -result {1falsecbatrueabc}

	#test edges property for neighbour rep
	test edges {} -body {
		set G [::Base::Graph new -directed true -representation $::Base::NEIGHBOUR -weighted true -printable true]
		set n0 [::Base::Node new]
    	set n1 [::Base::Node new]
		set n2 [::Base::Node new]
    	set n3 [::Base::Node new]

		$G add $n0 $n1 3
		$G add $n0 $n2 2
		$G add $n1 $n2 5
		$G add $n2 $n3 2
		$G add $n3 $n1 1

		set result [llength [$G edges get]]
		set sum 0
		foreach edge [$G edges get] {
			incr sum [$edge weight get]
		}
		append result $sum
	} -result {513}

	test edge {} -body {
		set G [::Base::Graph new -directed false -representation $::Base::NEIGHBOUR -weighted true]
		set n0 [::Base::Node new]
    	set n1 [::Base::Node new]
		set n2 [::Base::Node new]

		$G add $n0 $n1 3
		$G add $n0 $n2 2
		$G add $n1 $n2 5

		set edge [$G edge $n0 $n1]
		set result [expr {$n0 eq [$edge a get] || $n0 eq [$edge b get]}]

		set edge [$G edge $n1 $n0]
		append result [expr {$n1 eq [$edge a get] || $n1 eq [$edge b get]}]

		append result [[$G edge $n1 $n2] weight get]

		set G [::Base::Graph new -directed true -representation $::Base::NEIGHBOUR -weighted true]
		set n0 [::Base::Node new]
    	set n1 [::Base::Node new]
		set n2 [::Base::Node new]

		$G add $n0 $n1 3
		$G add $n0 $n2 2
		$G add $n1 $n2 5

		set edge [$G edge $n0 $n1]
		append result [expr {$n0 eq [$edge a get] && $n1 eq [$edge b get]}]

		set edge [$G edge $n1 $n0]
		append result [expr {"" eq [$G edge $n1 $n0]}]

		set G [::Base::Graph new -directed true -representation $::Base::EDGE -weighted true]
		
		set e1 [$G add $n0 $n1 3]
		set e2 [$G add $n0 $n2 2]
		set e3 [$G add $n1 $n2 5]
		append result [expr {$e1 eq [$G edge $n0 $n1]}]
		append result [expr {"" eq [$G edge $n1 $n0]}]

	} -result {1151111}
	
	test undirSearch {} -body {
		#BFS - edge-rep
		set G [::Base::Graph new -traversal $::Base::BFS]
		set n1 [::Base::Node new]
		set n2 [::Base::Node new]
		set n3 [::Base::Node new]
		set n4 [::Base::Node new]
		set n5 [::Base::Node new]
		set n6 [::Base::Node new]
		set n7 [::Base::Node new]
		set n8 [::Base::Node new]

		$G add $n1 $n2
		$G add $n2 $n3
		$G add $n3 $n4
		$G add $n5 $n6
		$G add $n6 $n7
		$G add $n7 $n8

		set result [$G search $n1 $n4]
		append result [$G search $n5 $n8]
		append result [$G search $n1 $n5]
		append result [$G search $n3 $n7]

		#DFS -edge-rep
		$G traversal set $::Base::DFS

		append result [$G search $n1 $n4]
		append result [$G search $n5 $n8]
		append result [$G search $n1 $n5]
		append result [$G search $n3 $n7]

		#BFS - neigh-rep
		set G [::Base::Graph new -traversal $::Base::BFS -representation $::Base::NEIGHBOUR]

		$G add $n1 $n2
		$G add $n2 $n3
		$G add $n3 $n4
		$G add $n5 $n6
		$G add $n6 $n7
		$G add $n7 $n8

		append result [$G search $n1 $n4]
		append result [$G search $n5 $n8]
		append result [$G search $n1 $n5]
		append result [$G search $n3 $n7]

		#DFS - neigh-rep
		$G traversal set $::Base::DFS

		append result [$G search $n1 $n4]
		append result [$G search $n5 $n8]
		append result [$G search $n1 $n5]
		append result [$G search $n3 $n7]


	} -result {truetruefalsefalsetruetruefalsefalsetruetruefalsefalsetruetruefalsefalse}

	proc _MST {repr} {
		set G [::Base::Graph new -representation $repr -MST true -weighted true]
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set n3 [::Base::Node new]
    	set n4 [::Base::Node new]
    	set n5 [::Base::Node new]
    	set n6 [::Base::Node new]
    	set n7 [::Base::Node new]

    	$G add $n1 $n2 7
		$G add $n1 $n4 5
		$G add $n2 $n3 8
		$G add $n2 $n4 9
		$G add $n2 $n5 7
		$G add $n3 $n5 5
		$G add $n4 $n5 15
		$G add $n4 $n6 6
		$G add $n5 $n6 8
		$G add $n5 $n7 9
		$G add $n6 $n7 11
		
		set MST [$G MST]

		set result [$MST numEdges]
		append result [$MST weighted get]
		append result [$MST directed get]
		#do edges add up to minimum weight?
		set sum 0
		foreach edge [$MST edges get] {
			incr sum [$edge weight get]
		}
		append result $sum
    	#is it connected?
		#pick any startNode
		set startNode [lindex [$MST nodes get] 0]
		set nodeCounter 0
		foreach node [$MST nodes get] {
			#can we reach all nodes from this node?
			if {$node eq $startNode} { continue }
			if {[$MST search $startNode $node]} {
				incr nodeCounter
			}
		}
		append result $nodeCounter
	}
	test MST {} -body {
		set result [_MST $::Base::EDGE]
		append result [_MST $::Base::NEIGHBOUR]
	} -result {6truefalse3966truefalse396}

	proc _SSSP {repr} {
		set G [::Base::Graph new -representation $repr -SSSP true -weighted true -directed true]
		set n0 [::Base::Node new]
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set n3 [::Base::Node new]
    	set n4 [::Base::Node new]
    	set n5 [::Base::Node new]
    	set n6 [::Base::Node new]
    	
		$G add $n0 $n1 5
		$G add $n1 $n0 1
		$G add $n0 $n2 20
		$G add $n0 $n3 3
		$G add $n2 $n4 6
		$G add $n2 $n3 15
		$G add $n3 $n4 1
		$G add $n4 $n5 3
		$G add $n4 $n6 12
		$G add $n5 $n6 3

		set sssp [$G SSSP $n0]
		set result [llength [$sssp nodes get]]
		append result [$sssp numEdges]
		append result [$sssp weighted get]
		append result [$sssp directed get]
		#do edges add up to correct weight?
		set sum 0
		foreach edge [$sssp edges get] {
			incr sum [$edge weight get]
		}
		append result $sum
		#is it connected?
		set startNode $n0
		set nodeCounter 0
		foreach node [$sssp nodes get] {
			#can we reach all nodes from this node?
			if {$node eq $startNode} { continue }
			if {[$sssp search $startNode $node]} {
				incr nodeCounter
			}
		}
		append result $nodeCounter
		#check other startnode
		set sssp [$G SSSP $n3]
		append result [llength [$sssp nodes get]]
		append result [$sssp numEdges]
		append result [$sssp weighted get]
		append result [$sssp directed get]
		#do edges add up to correct weight?
		set sum 0
		foreach edge [$sssp edges get] {
			incr sum [$edge weight get]
		}
		append result $sum
		#is it connected?
		set startNode $n3
		set nodeCounter 0
		foreach node [$sssp nodes get] {
			#can we reach all nodes from this node?
			if {$node eq $startNode} { continue }
			if {[$sssp search $startNode $node]} {
				incr nodeCounter
			}
		}
		append result $nodeCounter
		return $result
	}
	test SSSP {} -body {
		set result [_SSSP $::Base::EDGE]
		append result [_SSSP $::Base::NEIGHBOUR]
	} -result {76truetrue35643truetrue7376truetrue35643truetrue73}
    # ---------------%<------------------
    # End of my tests
    #    
    cleanupTests
}
namespace delete ::Base::Test









