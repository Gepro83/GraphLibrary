#
# See https://learnxinyminutes.com/docs/python3/
#
print("1. hello world") # print a "hello world" statement to stdout
print("2. hello world"); # use of the semicolon to end a statement is optional (rather, ruby looks for the end of line
print("3a. hello"); print("world"); # puts injects a special newline character (end="\n")
print("3b. hello", end=" "); print("world");

# single vs. double-quotes: no difference when it comes to control characters
print('\t4. hello world\n');
print("\t5. hello world\n");

# to escape control characters from being interpreted, prefix the string using "r" or "R" as for "raw"
print(r"\t5. hello world\n");

# BEWARE: braces may *not* be omitted (as in Python 2)
# print "6. hello world"; # WRONG!

# All names in Python are *case-sensitive*
first_name = "russ"; # preferred style by convention: lower case and underscore as separator
lastName = "sobernig"; # mixedCase is possible, but should be avoided

_full_name = first_name + " " + lastName # string concatenation

print(first_name)
print(lastName)

print(_full_name)
print(first_name, lastName, sep=" ")

#
# CONSTANTS are written (by convention) in upper case; but there are
# no semantics attached to them
#

POUNDS_PER_KILOGRAM = 2.2

#
# Multi-line strings using triple-quote notation:
#
x = """This is a very long string, 
containing commas, that I split up
into multiple line"""

print(x)

#
# Multi-line strings using brace (tuple) notation:
#

x = ("This is a very long string "
    "containing commas, that I split up "
    "into multiple line")

print(x)

#
# Multi-line strings using break-line notation:
#

x = "This is a very long string " \
  "containing commas, that I split up " \
  "into multiple line"

print(x)
  
# Multi-line expressions using break lines

x = 2 + 3 + \
  4 + 5

print(x)

_full_name = first_name + " " + \
  lastName

print(_full_name)


# Structured and non-structured (primitive) datatypes are all
# represented as objects

print(type(7))
print(type("hello world"))

seven_as_string = str(7) # to-string conversion
print(type(seven_as_string))

print(type(int(seven_as_string))) # string-to-number conversion


# basic control structures

# if-else-end

if 1: 
  print("7. hello world!");

if True: 
  print("7. hello world!");

if 0:
  print("8. hello world!");

if False:
  print("8. hello world!");

# expressions

weight = 50

if weight < 1:
  print('very light')
elif weight < 10:
  print('a bit of a load')
elif weight < 100:
  print('heavy')
else:
  print('way too heavy')

# loops

# 1. while
i = 0
while i < 4:
  print("i = " + str(i))
  i = i + 1; # i += 1

# 2. for

some_list = ['first' , 'second' , 3 ]
for element in some_list:
  print(element)
  
# container data structures: lists

x = [] # empty list
some_list = ['first' , 'second' , 3 ]

print(some_list)
print(some_list[0])
print(some_list[1])
print(some_list[2])
print(some_list[-1]) # backward positional lookup

print(len(some_list)) # length introspection

some_list[2] = "three" # positional assignment

# some_list[3] = 4 # WRONG: positional append
some_list.append(5) # relative append
some_list.extend([6, 7, "eight"]) # relative extend, each element is added
some_list.append([6, 7, "eight"]) # append vs. extend, append argument is added as one element

print(some_list)

del some_list[1]; # remove a list element; by index
some_list.remove('first'); # remove a list element; by value

# Python has alternative list-like data structures:
# - tuples: immutable list
# - set: unordered bags of elements

# container data structures: dictionaries

h = {}
h['first_name'] = ' Albert'
h['last_name'] = ' Einstein'
h['first_name']     # Is ' Albert'
h['last_name']      # Is Einstein

h = {'first_name' : ' Albert' , 'last_name' : 'Einstein'}

print(h)

# TODO: Implement a square routine

def square(x):
    return x * x

print(square(4));
print(square(x = 4));

raise SystemExit
