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
    set DEFAULT_WEIGHT 0
    
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
    	:property -accessor public [list weight:double $::Base::DEFAULT_WEIGHT] 
    }
    
    nx::Class create Edge {
    	:property -accessor public a:object,type=::Base::Node,required
    	:property -accessor public b:object,type=::Base::Node,required
    }
    
    nx::Class create WeightedEdge -superclass Edge {
    	:property -accessor public [list weight:double $::Base::DEFAULT_WEIGHT] 
    	
    }
    
    nx::Class create Graph {
    	:property -accessor public {edges:0..* {}}
   	    :property -accessor public {nodes:0..* {}}
    	:property {directed:boolean false} {
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set [:value=get $obj $prop]
				}
				return $r
				}
		}
    	:property {weighted:boolean false} {
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set [:value=get $obj $prop]
				}
				return $r
				}
		}
    	:property -accessor public {printable:boolean true} {
			:public object method value=set {obj prop value} {
				if {![$obj eval [list info exists :$prop]]} {
					set r [next]
				} else {
					set [:value=get $obj $prop]
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
					set [:value=get $obj $prop]
				}
				return $r
			}
		} 
    	
 		:public method numEdges {} {
 			if {${:representation} eq $::Base::EDGE} {
 				return [llength ${:edges}]
 			} else {
 				return "" 				
 			}
		}
		
		:public method size {} {
			return [llength ${:nodes}]
		}
		
		:public method nodeID {node:object,type=::Base::Node,required} {
			return [lsearch -exact ${:nodes} $node] 
		}
    	
		#add an edge
		#in digraphs the direction is from newNode1 to newNode2
		#if no weight is given in a weighted graph DEFAULT_WEIGHT is used as a default value
        #only non-negative weights are allowed, negative weights will be corrected to the default
    	:public method add {
    		m:object,type=::Base::Node,required
    		n:object,type=::Base::Node,required
    		{weight:double,substdefault $::Base::DEFAULT_WEIGHT} 
    	} {
    		if {${:weighted}} {
    			if {$weight < 0} {
    				set weight $::Base::DEFAULT_WEIGHT
    			}
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
    		{weight:double,substdefault $::Base::DEFAULT_WEIGHT} 
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
    		{weight:double,substdefault $::Base::DEFAULT_WEIGHT} 
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
 				return ""
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
 		#HOW DEFAULT WEIGHT for parameter?
 		:private method singleDOTedge {
 			node1:object,type=::Base::Node,required
    		node2:object,type=::Base::Node,required
    		{weight:double,substdefault $::Base::DEFAULT_WEIGHT} 
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
    	[$G add $n1 $n2] info class
	} -result {::Base::WeightedEdge}
	
	test weightedN {} -body {
		set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	set G [::Base::Graph new -weighted true -representation $::Base::NEIGHBOUR]
    	[$G add $n1 $n2] info class
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
    	
    	puts [$G DOTprint]
    	$G DOTprint
    } -result {digraph g{
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
    	set e1 [$G add $n1 $n2]
    	set e2 [$G add $n1 $n2]
    	set e3 [$G add $n2 $n1]

    	if {$e1 eq $e2} {
    		set result a
    	}
    	if {$e2 ne $e3} {
    		append result b
    	}
    	if {[$G size] == 2} {
    		append result c
    	}
    	
    	#undirected
    	set n1 [::Base::Node new]
    	set n2 [::Base::Node new]
    	
    	set G [::Base::Graph new -representation $::Base::NEIGHBOUR -weighted true]
    	set e1 [$G add $n1 $n2 2]
    	set e2 [$G add $n2 $n1 4]
    	
    	if {[$e2 opposite get] eq $n1} {
    		append result d
    	}
    	if {[$G size] == 2} {
    		append result e
    	}
    	if {[$e1 weight get] == 2} {
    		append result f
    	}
    	set result
	} -result {abcdef}
	
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
    	
    	puts [$G DOTprint]
    	$G DOTprint
	} -result {digraph g{
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
    	$G DOTprint
	} -result {}
	
	
    # ---------------%<------------------
    # End of my tests
    #    
    cleanupTests
}
namespace delete ::Base::Test









