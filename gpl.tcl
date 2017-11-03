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
    	:property node1:object,type=::Base::Node,required
    	:property node2:object,type=::Base::Node,required
    }
    
    nx::Class create Graph {
    	:variable edges {}
    	
    	:public method add {
    		newNode1:object,type=::Base::Node,required
    		newNode2:object,type=::Base::Node,required} {
			::Base::Edge create newEdge -node1 $newNode1 -node2 $newNode2 
 			foreach edge :edges {
 				puts "Test"
 			#	if {[edge cget -node1] == $newNode1 && [edge cget -node2] == $newNode2} {
 			#		puts "edge exists"
 			#		return $edge
 			#	}
 			#	if {[edge cget -node1] == $newNode2 && [edge cget -node2] == $newNode1} {
 			#		puts "edge exists"
 			#		return $edge
 			}
 				
 				lappend :edges $newEdge
 			#	return $newEdge
 			}
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

    test test-5 {} -body {
    	::Base::Node create n1
    	::Base::Node create n2
    	::Base::Node create n3
    	::Base::Node create n4
    	::Base::Node create n5
    	
    	::Base::Graph create G
    	G add n1 n2
    	G add n2 n3
    	G add n3 n4
    } 
    
    # ---------------%<------------------
    # End of my tests
    #    
    cleanupTests
}
namespace delete ::Base::Test









