# Coherence samples (auto-generated, labels in coherence_labels.csv)


## POS lib-csv#p002 @char 745: `arguments can be given to override in`


### A: A:lib-csv:p002:c001

```text
l *dialect* parameter can be
   given which is used to define a set of parameters specific to a
   particular CSV dialect.  It may be an instance of a subclass of the
   "Dialect" class or one of the strings returned by the
   "list_dialects()" function.  The other optional *fmtparams* keyword
   arguments can be given to override individual formatting parameters
   in the current dialect.  For full details about the dialect and
   formatting parameters, see section Dialects and Formatting
   Pa
```


### B: B:lib-csv:p002:c000

```text
[Module Contents]
The "csv" module defines the following functions:

csv.reader(csvfile, /, dialect='excel', **fmtparams)

   Return a reader object that will process lines from the given
   *csvfile*.  A csvfile must be an iterable of strings, each in the
   reader's defined csv format. A csvfile is most commonly a file-like
   object or list. If *csvfile* is a file object, it should be opened
   with "newline=''". [1]  An optional *dialect* parameter can be
   given which is used to define a set of parameters specific to a
   particular CSV dialect.  It may be an instance of a subclass of the
   "Dialect" class or one of the strings returned by the
   "list_dialects()" function.  The other optional *fmtparams* keyword
   arguments can be given to override individual formatting parameters
   in the current dialect.  For full details about the dialect and
   formatting parameters, see section Dialects and Formatting
   Parameters.
```


## POS lib-functools#p002 @char 822: `The *cached_property* decorator only`


### A: A:lib-functools:p002:c001

```text
rs):
              self._data = tuple(sequence_of_numbers)

          @cached_property
          def stdev(self):
              return statistics.stdev(self._data)

   The mechanics of "@cached_property" are somewhat different from
   "@property".  A regular property blocks attribute writes unless a
   setter is defined. In contrast, a *cached_property* allows writes.

   The *cached_property* decorator only runs on lookups and only when
   an attribute of the same name doesn't exist.  When it d
```


### B: B:lib-functools:p002:c001

```text
["functools" --- Higher-order functions and operations on callable objects (cont.)]
   The *cached_property* decorator only runs on lookups and only when
   an attribute of the same name doesn't exist.  When it does run, the
   *cached_property* writes to the attribute with the same name.
   Subsequent attribute reads and writes take precedence over the
   *cached_property* method and it works like a normal attribute.

   The cached value can be cleared by deleting the attribute.  This
   allows the *cached_property* method to run again.
```


## POS lib-json#p002 @char 1303: `>>> json.loads('1.1', parse_float=dec`


### A: A:lib-json:p002:c002

```text
gIO('["streaming API"]')
   >>> json.load(io)
   ['streaming API']

Customizing JSON object decoding:

   >>> import json
   >>> def as_complex(dct):
   ...     if '__complex__' in dct:
   ...         return complex(dct['real'], dct['imag'])
   ...     return dct
   ...
   >>> json.loads('{"__complex__": true, "real": 1, "imag": 2}',
   ...     object_hook=as_complex)
   (1+2j)
   >>> import decimal
   >>> json.loads('1.1', parse_float=decimal.Decimal)
   Decimal('1.1')

Extending "JSONEncoder":
```


### B: B:lib-json:p002:c001

```text
["json" --- JSON encoder and decoder (cont.)]
   >>> import json
   >>> json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
   ['foo', {'bar': ['baz', None, 1.0, 2]}]
   >>> json.loads('"\\"foo\\bar"')
   '"foo\x08ar'
   >>> from io import StringIO
   >>> io = StringIO('["streaming API"]')
   >>> json.load(io)
   ['streaming API']

Customizing JSON object decoding:

   >>> import json
   >>> def as_complex(dct):
   ...     if '__complex__' in dct:
   ...         return complex(dct['real'], dct['imag'])
   ...     return dct
   ...
   >>> json.loads('{"__complex__": true, "real": 1, "imag": 2}',
   ...     object_hook=as_complex)
   (1+2j)
   >>> import decimal
   >>> json.loads('1.1', parse_float=decimal.Decimal)
   Decimal('1.1')

Extending "JSONEncoder":
```


## POS lib-venv#p002 @char 740: `Changed in version 3.5: The use of "venv`


### A: A:lib-venv:p002:c001

```text

a copy or symlink of the Python executable (as appropriate for the
platform or arguments used at environment creation time). It also
creates a "lib/pythonX.Y/site-packages" subdirectory (on Windows, this
is "Lib\site-packages"). If an existing directory is specified, it
will be re-used.

Changed in version 3.5: The use of "venv" is now recommended for
creating virtual environments.

Deprecated since version 3.6, removed in version 3.8: **pyvenv** was
the recommended tool for creating virtual en
```


### B: B:lib-venv:p002:c000

```text
[Creating virtual environments]
Virtual environments are created by executing the "venv" module:

   python -m venv /path/to/new/virtual/environment

This creates the target directory (including parent directories as
needed) and places a "pyvenv.cfg" file in it with a "home" key
pointing to the Python installation from which the command was run. It
also creates a "bin" (or "Scripts" on Windows) subdirectory containing
a copy or symlink of the Python executable (as appropriate for the
platform or arguments used at environment creation time). It also
creates a "lib/pythonX.Y/site-packages" subdirectory (on Windows, this
is "Lib\site-packages"). If an existing directory is specified, it
will be re-used.

Changed in version 3.5: The use of "venv" is now recommended for
creating virtual environments.
```


## POS tut-controlflow#p002 @char 970: `4 lamb

In most such cases, however,`


### A: A:tut-controlflow:p002:c002

```text
  ...     print(i, a[i])
   ...
   0 Mary
   1 had
   2 a
   3 little
   4 lamb

In most such cases, however, it is convenient to use the "enumerate()"
function, see Looping Techniques.

A strange thing happens if you just print a range:

   >>> range(10)
   range(0, 10)

In many ways the object returned by "range()" behaves as if it is a
list, but in fact it isn't. It is an object which returns the
successive items of the desired sequence when you iterate over it, but
it doesn't really make the
```


### B: B:tut-controlflow:p002:c000

```text
[4.3. The "range()" Function]
If you do need to iterate over a sequence of numbers, the built-in
function "range()" comes in handy.  It generates arithmetic
progressions:

   >>> for i in range(5):
   ...     print(i)
   ...
   0
   1
   2
   3
   4

The given end point is never part of the generated sequence;
"range(10)" generates 10 values, the legal indices for items of a
sequence of length 10.  It is possible to let the range start at
another number, or to specify a different increment (even negative;
sometimes this is called the 'step'):

   >>> list(range(5, 10))
   [5, 6, 7, 8, 9]

   >>> list(range(0, 10, 3))
   [0, 3, 6, 9]

   >>> list(range(-10, -100, -30))
   [-10, -40, -70]

To iterate over the indices of a sequence, you can combine "range()"
and "len()" as follows:

   >>> a = ['Mary', 'had', 'a', 'little', 'lamb']
   >>> for i in range(len(a)):
   ...     print(i, a[i])
   ...
   0 Mary
   1 had
   2 a
   3 little
   4 lamb
```


## POS tut-datastructures#p002 @char 812: `>>> fruits.append('grape')
   >>> fru`


### A: A:tut-datastructures:p002:c001

```text
 = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
   >>> fruits.count('apple')
   2
   >>> fruits.count('tangerine')
   0
   >>> fruits.index('banana')
   3
   >>> fruits.index('banana', 4)  # Find next banana starting at position 4
   6
   >>> fruits.reverse()
   >>> fruits
   ['banana', 'apple', 'kiwi', 'banana', 'pear', 'apple', 'orange']
   >>> fruits.append('grape')
   >>> fruits
   ['banana', 'apple', 'kiwi', 'banana', 'pear', 'apple', 'orange', 'grape']
   >>> fruits.sor
```


### B: B:tut-datastructures:p002:c001

```text
[5. Data Structures > 5.1. More on Lists (cont.)]
   >>> fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
   >>> fruits.count('apple')
   2
   >>> fruits.count('tangerine')
   0
   >>> fruits.index('banana')
   3
   >>> fruits.index('banana', 4)  # Find next banana starting at position 4
   6
   >>> fruits.reverse()
   >>> fruits
   ['banana', 'apple', 'kiwi', 'banana', 'pear', 'apple', 'orange']
   >>> fruits.append('grape')
   >>> fruits
   ['banana', 'apple', 'kiwi', 'banana', 'pear', 'apple', 'orange', 'grape']
   >>> fruits.sort()
   >>> fruits
   ['apple', 'apple', 'banana', 'banana', 'grape', 'kiwi', 'orange', 'pear']
   >>> fruits.pop()
   'pear'

You might have noticed that methods like "insert", "remove" or "sort"
that only modify the list have no return value printed -- they return
the default "None". [1]  This is a design principle for all mutable
data structures in Python.
```


## POS tut-errors#p002 @char 861: `of the "try" statement is finished.

*`


### A: A:tut-errors:p002:c001

```text
...     try:
   ...         x = int(input("Please enter a number: "))
   ...         break
   ...     except ValueError:
   ...         print("Oops!  That was no valid number.  Try again...")
   ...

The "try" statement works as follows.

* First, the *try clause* (the statement(s) between the "try" and
  "except" keywords) is executed.

* If no exception occurs, the *except clause* is skipped and execution
  of the "try" statement is finished.

* If an exception occurs during execution of the "
```


### B: B:tut-errors:p002:c000

```text
[8.3. Handling Exceptions]
It is possible to write programs that handle selected exceptions. Look
at the following example, which asks the user for input until a valid
integer has been entered, but allows the user to interrupt the program
(using "Control"-"C" or whatever the operating system supports); note
that a user-generated interruption is signalled by raising the
"KeyboardInterrupt" exception.

   >>> while True:
   ...     try:
   ...         x = int(input("Please enter a number: "))
   ...         break
   ...     except ValueError:
   ...         print("Oops!  That was no valid number.  Try again...")
   ...

The "try" statement works as follows.

* First, the *try clause* (the statement(s) between the "try" and
  "except" keywords) is executed.

* If no exception occurs, the *except clause* is skipped and execution
  of the "try" statement is finished.
```


## POS tut-inputoutput#p002 @char 917: `representation using either function.  S`


### A: A:tut-inputoutput:p002:c001

```text
 "str()" function is meant to return representations of values
which are fairly human-readable, while "repr()" is meant to generate
representations which can be read by the interpreter (or will force a
"SyntaxError" if there is no equivalent syntax).  For objects which
don't have a particular representation for human consumption, "str()"
will return the same value as "repr()".  Many values, such as numbers
or structures like lists and dictionaries, have the same
representation using either funct
```


### B: B:tut-inputoutput:p002:c001

```text
[7. Input and Output > 7.1. Fancier Output Formatting (cont.)]
The "str()" function is meant to return representations of values
which are fairly human-readable, while "repr()" is meant to generate
representations which can be read by the interpreter (or will force a
"SyntaxError" if there is no equivalent syntax).  For objects which
don't have a particular representation for human consumption, "str()"
will return the same value as "repr()".  Many values, such as numbers
or structures like lists and dictionaries, have the same
representation using either function.  Strings, in particular, have
two distinct representations.

Some examples:
```


## POS tut-modules#p002 @char 1448: `There is even a variant to import all na`


### A: A:tut-modules:p002:c003

```text
m which the imports are
taken in the local namespace (so in the example, "fibo" is not
defined).

There is even a variant to import all names that a module defines:

   >>> from fibo import *
   >>> fib(500)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377

This imports all names except those beginning with an underscore
("_"). In most cases Python programmers do not use this facility since
it introduces an unknown set of names into the interpreter, possibly
hiding some things you have already define
```


### B: B:tut-modules:p002:c001

```text
[6.1. More on Modules]
Modules can import other modules.  It is customary but not required to
place all "import" statements at the beginning of a module (or script,
for that matter).  The imported module names, if placed at the top
level of a module (outside any functions or classes), are added to the
module's global namespace.

There is a variant of the "import" statement that imports names from a
module directly into the importing module's namespace.  For example:

   >>> from fibo import fib, fib2
   >>> fib(500)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377

This does not introduce the module name from which the imports are
taken in the local namespace (so in the example, "fibo" is not
defined).

There is even a variant to import all names that a module defines:

   >>> from fibo import *
   >>> fib(500)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377
```


## POS tut-venv#p002 @char 837: `package name  followed by "==" and the v`


### A: A:tut-venv:p002:c001

```text
.)

You can install the latest version of a package by specifying a
package's name:

   (tutorial-env) $ python -m pip install novas
   Collecting novas
     Downloading novas-3.1.1.3.tar.gz (136kB)
   Installing collected packages: novas
     Running setup.py install for novas
   Successfully installed novas-3.1.1.3

You can also install a specific version of a package by giving the
package name  followed by "==" and the version number:

   (tutorial-env) $ python -m pip install requests==2.6.0
```


### B: B:tut-venv:p002:c000

```text
[12.3. Managing Packages with pip]
You can install, upgrade, and remove packages using a program called
**pip**.  By default "pip" will install packages from the Python
Package Index.  You can browse the Python Package Index by going to it
in your web browser.

"pip" has a number of subcommands: "install", "uninstall", "freeze",
etc.  (Consult the Installing Python modules guide for complete
documentation for "pip".)

You can install the latest version of a package by specifying a
package's name:

   (tutorial-env) $ python -m pip install novas
   Collecting novas
     Downloading novas-3.1.1.3.tar.gz (136kB)
   Installing collected packages: novas
     Running setup.py install for novas
   Successfully installed novas-3.1.1.3

You can also install a specific version of a package by giving the
package name  followed by "==" and the version number:
```
