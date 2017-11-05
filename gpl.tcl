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
    nx::Class create Node 
    
    nx::Class create Edge {
    	:property -accessor public node1:object,type=::Base::Node,required
    	:property -accessor public node2:object,type=::Base::Node,required
    }
    
    nx::Class create Graph {
    	:variable edges {}
    	:variable nodes {}
    	
 		:public method numEdges {} {
    		return [llength ${:edges}]
		}
		
		:public method size {} {
			return [llength ${:nodes}]
		}
		
		:public method nodeID {node:object,type=::Base::Node,required} {
			return [lsearch ${:nodes} $node] 
		}
		
		:public method edges {} {
			return ${:edges} 
		}
    	
    	:public method add {
    		newNode1:object,type=::Base::Node,required
    		newNode2:object,type=::Base::Node,required
    	} {
			set e [Edge new -node1 $newNode1 -node2 $newNode2]
			#check for double edges
			foreach edge ${:edges} {
				if {[$edge cget -node1] == $newNode1 && [$edge cget -node2] == $newNode2} {
 					return $edge
 				}
 				if {[$edge cget -node1] == $newNode2 && [$edge cget -node2] == $newNode1} {
 					return $edge
 				}
 			}
 			#add edge
 			lappend :edges $e
 			#only add new nodes
 			if {[lsearch ${:nodes} $newNode1] == -1} {
 				lappend :nodes $newNode1
 			}
 			if {[lsearch ${:nodes} $newNode2] == -1} {
 				lappend :nodes $newNode2
 			}
 			
 			return $e
 		}
	}
	
	proc DOTprint {G} {
		if {[$G info class] != "::Base::Graph"} {
			puts "This is not a graph object!"
			return
		}
		#start a graph
		set DOTstring "graph g\{
node\[label=\"\"\];
"
		set edges [$G edges]
		foreach edge $edges {
			#the names of the nodes are the index in the nodeslist in the graph
			set node1 [$G nodeID [$edge cget -node1]]
			set node2 [$G nodeID [$edge cget -node2]]
			#add the edge to the dotstring
			append DOTstring "$node1 -- $node2
"
		}
		append DOTstring "\}"
		return $DOTstring
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

    test checkdoubleedges {} -body {
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
    
    test checkdoublenodes {} -body {
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
    
    test checkDOTprinter {} -body {
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
    	
    	puts [::Base::DOTprint $G]
    	::Base::DOTprint $G
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
    	
    
    # ---------------%<------------------
    # End of my tests
    #    
    cleanupTests
}
namespace delete ::Base::Test









