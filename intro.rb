#
# See https://learnxinyminutes.com/docs/ruby/
#

puts("1. hello world") # print a "hello world" statement to stdout
puts("2. hello world"); # use of the semicolon to end a statement is optional (rather, ruby looks for the end of line
puts("3. hello"); puts("world"); # puts injects a special newline character (\n)

# single vs. double-quotes
puts('\t4. hello world\n');
puts("\t5. hello world\n");

# braces may be omitted (braces hint at puts being a method, of a
# hidden, global / main object)
puts "6. hello world"

# variables: naming convention

first_name = "russ"
lastName = "sobernig"
_full_name = first_name + " " + lastName # string concatenation

puts(first_name)
puts(lastName)
puts(_full_name)

# multi-line expressions

x = 2 + 3 +
  4 + 5

puts(x)

_full_name = first_name + " " + \
  lastName

puts(_full_name)

# CONSTANTS

POUNDS_PER_KILOGRAM = 2.2
StopToken = 'stop'

puts("StopToken -> " + StopToken)

# redefining a CONSTANT is prohibited
# StopToken = 'end' # throws 'already initialized constant StopToken'

# Structured and non-structured (primitive) datatypes are all
# represented as objects

puts(7.class)
puts("hello world".class)

seven_as_string = 7.to_s # to-string conversion
y = seven_as_string.class.to_s + " -> " + seven_as_string
puts(y)

# basic control structures

# if-else-end

if 1 
  puts("7. hello world!");
end

if 0
  puts("8. hello world!");
end

# expressions

weight = 50

if(weight < 1)
  puts('very light')
elsif(weight < 10)
  puts('a bit of a load')
elsif weight < 100 # braces are, again, optional
  puts('heavy')
else
  puts('way too heavy')
end

# variable references + substitution
# in-brace vs. out-brace substitution

x = "someVar"
puts("x -> " + x) # out-brace
puts("x -> #{x}") # in-brace

puts("arbitrary expressions -> #{(3*4).to_s + "---" + first_name}") # in-brace

# loops

# 1. while
i = 0
while(i < 4)
  puts("i = #{i}")
  i = i + 1; # i += 1
end

# 2. for

some_array = ['first' , 'second' , 3 ]
for element in some_array
  puts("#{element}")
end
             
# iterators (handy!)

some_array.each do |element|
  puts(element);
end

# symbols (immutable strings, used as identifiers (object identifiers,
# object members)

# container data structures: arrays

x = []
y = Array.new()
some_array = ['first' , 'second' , 3 ]

puts(some_array[0])
puts(some_array[1])
puts(some_array[2])

puts(some_array.length()) # length introspection
puts(some_array.size()) # size introspection

some_array[2] = "three" # positional assigment

some_array[3] = 4 # positional append
some_array << 5 # relative append

# containder data structures: hashes

h = {}
h['first_name'] = ' Albert'
h['last_name'] = ' Einstein'
h['first_name']     # Is ' Albert'
h['last_name']      # Is Einstein

h = {'first_name' => ' Albert' , 'last_name' => 'Einstein'}

h.each do |key,value|
  puts(key + " -> " + value)
end

# a simple function (call)

def square(x)
	return x*x
end

puts square(2); # returns/ prints '4'
