#
# See https://learnxinyminutes.com/docs/tcl/
#

# comments - there is only the concept of single-line comments
# each line of a multi-line comment block must be introduced by a "#"

puts "hello world"; # inline comments require a preceding ";"
puts {hello world}; # grouping words by "{}" makes them literal strings (there is no variable substitution etc.)

# variable operations: naming, assignment, substitution
set x "hello world"
puts "x = $x"
puts {x = $x}; # no variable replacement occurs -> $x is printed, rather than 'hello world'
# 1. "[...]" blocks are evaluation blocks which are evaluated (executed)
# before printing the final string (kind of a #{...} block in ruby,
# but more powerful)
# 2. [set x] corresponds to $x, i.e., the [set] command acts a
# variable setter when supplied with two arguments and as a getter
# when there is only a single argument
puts "x = [set x]";



# variable naming: there are no syntactic conventions, except for
# using "$" as first character in a variable name (such as in
# javascript)
set first_name "russ"
set lastName "sobernig"

# in Tcl, there are no operators like + etc. for string manipulation,
# but there are various commands a [string] command

set _full_name "$first_name $lastName"; # string concatenation (within quotes)

puts "1. $_full_name"

# ... or the [append] and [string commands]
# http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/append.htm
# http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/string.htm

append _full_name2 $first_name " " $lastName

puts "2. $_full_name2"

# arithmetic operations must be performed by a special command: [expr]
# http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/expr.htm

set x [expr {2 + 3 + 4 + 5}]
puts "x->$x"

# multi-line assignments
# `- multi-line strings: just a newline

set _full_name "$first_name 
lastName"

puts "_full_name->$_full_name"

# `- multi-line commands (!): use the backslash to bind lines
# NOTE: there must not be a white space following the "\" !!!

append _full_name2 $first_name \
    " " $lastName

puts "_full_name2->$_full_name2"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Home assignment: Complete the following tasks (based on the equivalent
# JavaScript and Ruby examples)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# if statements
# see http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/if.htm
if {1} {puts "Hi"}
if {true} {puts "Hi"}
if {false} {puts "Hi"}
if {0} {puts "Hi"}

set two 2
if {$two == 1} {
	puts "One"
} elseif {$two == 4} {
	puts "Four"
} else {
	puts "Two"
}

# while loop
# see http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/while.htm
set i 5
while {$i > $two} {
	puts "$i"
	incr i -1
}

# for loop
# see http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/for.htm

for {set c 0} {$c < 5} {incr c} {
	puts "$c"
}

array set some_array {
	"first" 1
	second 2
	3 3
}

# for/in loop
# see http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/foreach.htm

foreach element [array names some_array] {
  puts "$element"
}


# Container data structures: list (corresponds to arrays in other
# javascript and ruby)
# see http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/list.htm
# Note, there are individual commands for list management, i.e.,
# [llength], [lsort], [lappend]!

set l { one }
lappend l two three
llength $l

# Container data structures: arrays or dicts (Tcl array are associative arrays,
# i.e., hashes. The name is misleading!
# see http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/array.htm

# define a proc "square()":
# see http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/proc.htm
# see http://docs.activestate.com/activetcl/8.6/tcl/TclCmd/return.htm

proc square {x} {
	return [expr $x * $x]
}

square 2