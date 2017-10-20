/*
 * See https://learnxinyminutes.com/docs/javascript/
 *
 */
print("hello world")
print("hello world"); // single-line comment: again, semicolons are optional
/* a multi-line comment: 
   using /explicit/ line break
*/
putstr("hello "); putstr("world\n");

/* variables: naming convention
   first character: letter, underscore, $
   second+ character: letter, underscore, $, digit
 */

first_name = "russ";
lastName = "sobernig";
$str = "someString";
_full_name = first_name + " " + lastName; // string concatenation

print(first_name)
print(lastName)
print($str)
print(_full_name)

greeting = "Welcome to my blog, owned by" + " " + _full_name;
print(greeting)

/* variable declarations:
   variables prefixed by "var" are permanent (they cannot be deleted on demand)
 */

var i; // until assigned, undefined value
var sum = 0, message, course = "oo1"; // until assigned, undefined value
print(delete(sum)); // returns 'false'

// single vs. double-quotes: semantically equivalent
print('\t4. hello world');
print("\t5. hello world");
// mix quotations
print("\t6. 'hello world'");

/* Structured and non-structured (primitive) datatypes are all
   represented as objects
*/

var n = 100; 
var s = n + " bottles of beer on the wall."; // automatic (implicit) conversion

var seven = 7
var seven_as_string = seven.toString(); // explicit to-string conversion
var seven_as_string = String(seven); // explicit to-string conversion
y = "seven_as_string -> " + seven_as_string;
print(y)

var product = "21" * "2"; // yields 42; implicit conversion
print(product)
var result = seven_as_string - 5; // yields 2
print(result)

// explicit string-to.number conversion
var product = Number("21") * Number("2");
print(product)

// basic control structures

// if statements

if (1)
    print("7. hello world!");

if (1) print("7. hello world!");


if (0) {
    print("8. hello world!");
 }


// expressions

var weight = 50;

if(weight < 1)
    print('very light');
 else if (weight < 10)
     print('a bit of a load');
 else if (weight < 100)
     print('heavy');
 else
     print('way too heavy');
	 
// loops

// 1. while
var i = 0;
while (i < 4) {
    print("i = " + i);
    i++;
 }

// 2. for loop
for (var i = 0 ; i < 4 ; i++)
    print("i = " + i);

// 3. for/in loop

var some_array = new Array("first", "second" , 3);
for (idx in some_array)
    print(idx + " -> " + some_array[idx]);


// container data structures: arrays

var x = [];
var y = new Array();
var some_array = new Array("first", "second" , 3);
var y = new Array(10); // specifies an array of length 10
var some_array = ['first' , 'second' , 3 ]; // array literal notation

print(some_array[0]);
print(some_array[1]);
print(some_array[2]);

print(some_array.length); // length introspection

some_array[2] = "three"; // positional assigment

some_array[3] = 4; // positional append
some_array[some_array.length] = 5 // relative append
print(some_array[4]);

// containder data structures: hashes (maps)

var h = {}; // hash (object) literal notation
h["first_name"] = "Albert";
h["last_name"] = "Einstein";
print(h["first_name"]); // Is ' Albert'
print(h['last_name']); // Is Einstein

h = {'first_name': 'Albert' , 'last_name': 'Einstein'}

for (key in h)
    print("value of '"+ key + "' -> " + h[key]);

/*
  functions: TODOs
*/

function square(x){
	return x * x;
}

print(square(4)); // -> returns/ prints '16'
