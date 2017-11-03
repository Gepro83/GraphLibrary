    

nx::Class create Node 
		
nx::Class create Edge {
	:property node1:object,type=::Node,required
	:property node2:object,type=::Node,required
}
		
nx::Class create Graph {
	:variable edges {}
			
	:public method add {
		newNode1:object,type=::Node,required
		newNode2:object,type=::Node,required} {
		Edge create newEdge -node1 $newNode1 -node2 $newNode2
		foreach edge :edges {
			puts "TEST"
			#if {[edge cget -node1] == $newNode1 && [edge cget -node2] == $newNode2} {
			#	puts "edge exists"
			#	return $edge
			#}
			#if {[edge cget -node1] == $newNode2 && [edge cget -node2] == $newNode1} {
			#	puts "edge exists"
			#	return $edge
			#}
	}
		lappend :edges newEdge
	}
			
	:public method numEdges {} {
		llength :edges
	}
}
		
		
::Node create n1
::Node create n2
::Node create n3
::Graph create G
G add n1 n2
G add n2 n3
G numEdges
	