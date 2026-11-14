# Test top-3 sheet (auto-generated, labels in metadata_audit.csv / grounding_labels.csv)


## A t01 filter_applied=None

Q: If both the try block and the finally block contain a return statement, which value is returned?
Gold: [('tut-errors', [6])]


### rank 1 A:tut-errors:p006:c004 score=0.6737 hit=False
source=python-3.13-docs-text/tutorial/errors.txt page=6 page_id=tut-errors#p006 doc_type=tutorial section=8. Errors and Exceptions > 8.7. Defining Clean-up Actions

```text
else"
  clause. Again, the exception is re-raised after the "finally" clause
  has been executed.

* If the "finally" clause executes a "break", "continue" or "return"
  statement, exceptions are not re-raised.

* If the "try" statement reaches a "break", "continue" or "return"
  statement, the "finally" clause will execute just prior to the
  "break", "continue" or "return" statement's execution.

* If a "finally" clause includes a "return" statement, the returned
  value will be the one from t
```


### rank 2 A:tut-errors:p006:c005 score=0.5448 hit=False
source=python-3.13-docs-text/tutorial/errors.txt page=6 page_id=tut-errors#p006 doc_type=tutorial section=8. Errors and Exceptions > 8.7. Defining Clean-up Actions

```text
ement, the returned
  value will be the one from the "finally" clause's "return"
  statement, not the value from the "try" clause's "return" statement.

For example:

   >>> def bool_return():
   ...     try:
   ...         return True
   ...     finally:
   ...         return False
   ...
   >>> bool_return()
   False

A more complicated example:

   >>> def divide(x, y):
   ...     try:
   ...         result = x / y
   ...     except ZeroDivisionError:
   ...         print("division by zero!")
```


### rank 3 A:tut-errors:p006:c002 score=0.5441 hit=False
source=python-3.13-docs-text/tutorial/errors.txt page=6 page_id=tut-errors#p006 doc_type=tutorial section=8. Errors and Exceptions > 8.7. Defining Clean-up Actions

```text
executed under all circumstances.
For example:

   >>> try:
   ...     raise KeyboardInterrupt
   ... finally:
   ...     print('Goodbye, world!')
   ...
   Goodbye, world!
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
       raise KeyboardInterrupt
   KeyboardInterrupt

If a "finally" clause is present, the "finally" clause will execute as
the last task before the "try" statement completes. The "finally"
clause runs whether or not the "try" statement produces an
```


## A t02 filter_applied=None

Q: Which locations is sys.path initialized from?
Gold: [('tut-modules', [3])]


### rank 1 A:tut-modules:p003:c003 score=0.627 hit=False
source=python-3.13-docs-text/tutorial/modules.txt page=3 page_id=tut-modules#p003 doc_type=tutorial section=6. Modules > 6.1. More on Modules > 6.1.2. The Module Search Path

```text
ied).

* "PYTHONPATH" (a list of directory names, with the same syntax as the
  shell variable "PATH").

* The installation-dependent default (by convention including a "site-
  packages" directory, handled by the "site" module).

More details are at The initialization of the sys.path module search
path.

Note:

  On file systems which support symlinks, the directory containing the
  input script is calculated after the symlink is followed. In other
  words the directory containing the symlink i
```


### rank 2 A:lib-venv:p010:c001 score=0.546 hit=False
source=python-3.13-docs-text/library/venv.txt page=10 page_id=lib-venv#p010 doc_type=library section="venv" --- Creation of virtual environments > API (cont.)

```text
 to assist in installing custom
      scripts into the virtual environment.

      *path* is the path to a directory that should contain
      subdirectories "common", "posix", "nt"; each containing scripts
      destined for the "bin" directory in the environment.  The
      contents of "common" and the directory corresponding to
      "os.name" are copied after some text replacement of
      placeholders:

      * "__VENV_DIR__" is replaced with the absolute path of the
        environment dir
```


### rank 3 A:tut-modules:p005:c002 score=0.5457 hit=False
source=python-3.13-docs-text/tutorial/modules.txt page=5 page_id=tut-modules#p005 doc_type=tutorial section=6. Modules > 6.2. Standard Modules

```text

   C> print('Yuck!')
   Yuck!
   C>

These two variables are only defined if the interpreter is in
interactive mode.

The variable "sys.path" is a list of strings that determines the
interpreter's search path for modules. It is initialized to a default
path taken from the environment variable "PYTHONPATH", or from a
built-in default if "PYTHONPATH" is not set.  You can modify it using
standard list operations:

   >>> import sys
   >>> sys.path.append('/ufs/guido/lib/python')

6.3. The "dir()" 
```


## A t03 filter_applied=None

Q: How should a file be opened before passing it to csv.reader?
Gold: [('lib-csv', [2])]


### rank 1 A:lib-csv:p002:c000 score=0.6455 hit=True
source=python-3.13-docs-text/library/csv.txt page=2 page_id=lib-csv#p002 doc_type=library section="csv" --- CSV File Reading and Writing > Module Contents

```text
Module Contents
===============

The "csv" module defines the following functions:

csv.reader(csvfile, /, dialect='excel', **fmtparams)

   Return a reader object that will process lines from the given
   *csvfile*.  A csvfile must be an iterable of strings, each in the
   reader's defined csv format. A csvfile is most commonly a file-like
   object or list. If *csvfile* is a file object, it should be opened
   with "newline=''". [1]  An optional *dialect* parameter can be
   given which is use
```


### rank 2 A:lib-csv:p013:c003 score=0.5627 hit=False
source=python-3.13-docs-text/library/csv.txt page=13 page_id=lib-csv#p013 doc_type=library section="csv" --- CSV File Reading and Writing > Examples

```text
A slightly more advanced use of the reader --- catching and reporting
errors:

   import csv, sys
   filename = 'some.csv'
   with open(filename, newline='') as f:
       reader = csv.reader(f)
       try:
           for row in reader:
               print(row)
       except csv.Error as e:
           sys.exit(f'file {filename}, line {reader.line_num}: {e}')

And while the module doesn't directly support parsing strings, it can
easily be done:

   import csv
   for row in csv.reader(['one,two,th
```


### rank 3 A:lib-csv:p013:c000 score=0.5616 hit=False
source=python-3.13-docs-text/library/csv.txt page=13 page_id=lib-csv#p013 doc_type=library section="csv" --- CSV File Reading and Writing > Examples

```text
Examples
========

The simplest example of reading a CSV file:

   import csv
   with open('some.csv', newline='') as f:
       reader = csv.reader(f)
       for row in reader:
           print(row)

Reading a file with an alternate format:

   import csv
   with open('passwd', newline='') as f:
       reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
       for row in reader:
           print(row)

The corresponding simplest possible writing example is:

   import csv
   with open('
```


## A t04 filter_applied=None

Q: What happens to lru_cache when maxsize is None?
Gold: [('lib-functools', [5])]


### rank 1 A:lib-functools:p006:c002 score=0.677 hit=False
source=python-3.13-docs-text/library/functools.txt page=6 page_id=lib-functools#p006 doc_type=library section="functools" --- Higher-order functions and operations on callable objects (cont.)

```text
   In general, the LRU cache should only be used when you want to
   reuse previously computed values.  Accordingly, it doesn't make
   sense to cache functions with side-effects, functions that need to
   create distinct mutable objects on each call (such as generators
   and async functions), or impure functions such as time() or
   random().

   Example of an LRU cache for static web content:

      @lru_cache(maxsize=32)
      def get_pep(num):
          'Retrieve text of a Python Enhancemen
```


### rank 2 A:lib-functools:p005:c003 score=0.6041 hit=False
source=python-3.13-docs-text/library/functools.txt page=5 page_id=lib-functools#p005 doc_type=library section="functools" --- Higher-order functions and operations on callable objects (cont.)

```text
tiveness of the cache and tune the
   *maxsize* parameter, the wrapped function is instrumented with a
   "cache_info()" function that returns a *named tuple* showing
   *hits*, *misses*, *maxsize* and *currsize*.
```


### rank 3 A:lib-functools:p004:c001 score=0.6003 hit=False
source=python-3.13-docs-text/library/functools.txt page=4 page_id=lib-functools#p004 doc_type=library section="functools" --- Higher-order functions and operations on callable objects (cont.)

```text
tutorial, see Sorting
   Techniques.

   Added in version 3.2.

@functools.lru_cache(user_function)
@functools.lru_cache(maxsize=128, typed=False)

   Decorator to wrap a function with a memoizing callable that saves
   up to the *maxsize* most recent calls.  It can save time when an
   expensive or I/O bound function is periodically called with the
   same arguments.

   The cache is threadsafe so that the wrapped function can be used in
   multiple threads.  This means that the underlying data
```


## A t05 filter_applied=None

Q: In the library reference: why may a dictionary not equal the original after converting it to JSON and back?
Gold: [('lib-json', [5])]


### rank 1 A:lib-json:p001:c001 score=0.4906 hit=False
source=python-3.13-docs-text/library/json.txt page=1 page_id=lib-json#p001 doc_type=library section="json" --- JSON encoder and decoder

```text
term "object" in the context of JSON processing in Python can be
  ambiguous. All values in Python are objects. In JSON, an object
  refers to any data wrapped in curly braces, similar to a Python
  dictionary.

Warning:

  Be cautious when parsing JSON data from untrusted sources. A
  malicious JSON string may cause the decoder to consume considerable
  CPU and memory resources. Limiting the size of data to be parsed is
  recommended.

This module exposes an API familiar to users of the standar
```


### rank 2 A:lib-json:p005:c000 score=0.4733 hit=True
source=python-3.13-docs-text/library/json.txt page=5 page_id=lib-json#p005 doc_type=library section="json" --- JSON encoder and decoder > Basic Usage (cont.)

```text
      * **sort_keys** (*bool*) -- If "True", dictionaries will be
        outputted sorted by key. Default "False".

   Note:

     Keys in key/value pairs of JSON are always of the type "str".
     When a dictionary is converted into JSON, all the keys of the
     dictionary are converted to strings. As a result of this, if a
     dictionary is converted into JSON and then back into a
     dictionary, the dictionary may not equal the original one. That
     is, "loads(dumps(x)) != x" if x has n
```


### rank 3 A:lib-json:p010:c001 score=0.4685 hit=False
source=python-3.13-docs-text/library/json.txt page=10 page_id=lib-json#p010 doc_type=library section="json" --- JSON encoder and decoder > Encoders and Decoders (cont.)

```text
e the document ended.

      This can be used to decode a JSON document from a string that
      may have extraneous data at the end.

class json.JSONEncoder(*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None)

   Extensible JSON encoder for Python data structures.

   Supports the following objects and types by default:

   +------------------------------------------+-----------------+
   | Python               
```


## A t06 filter_applied=None

Q: Following the tutorial, how do I activate a virtual environment on Windows?
Gold: [('tut-venv', [1])]


### rank 1 A:lib-venv:p004:c001 score=0.5902 hit=False
source=python-3.13-docs-text/library/venv.txt page=4 page_id=lib-venv#p004 doc_type=library section="venv" --- Creation of virtual environments > How venvs work

```text
 environment may be "activated" using a script in its binary
directory ("bin" on POSIX; "Scripts" on Windows). This will prepend
that directory to your "PATH", so that running **python** will invoke
the environment's Python interpreter and you can run installed scripts
without having to use their full path. The invocation of the
activation script is platform-specific ("*<venv>*" must be replaced by
the path to the directory containing the virtual environment):

+---------------+--------------+--
```


### rank 2 A:lib-venv:p005:c000 score=0.5834 hit=False
source=python-3.13-docs-text/library/venv.txt page=5 page_id=lib-venv#p005 doc_type=library section="venv" --- Creation of virtual environments > How venvs work (cont.)

```text
Added in version 3.4: **fish** and **csh** activation scripts.

Added in version 3.8: PowerShell activation scripts installed under
POSIX for PowerShell Core support.

You don't specifically *need* to activate a virtual environment, as
you can just specify the full path to that environment's Python
interpreter when invoking Python. Furthermore, all scripts installed
in the environment should be runnable without activating it.

In order to achieve this, scripts installed into virtual environments
```


### rank 3 A:lib-venv:p008:c002 score=0.5134 hit=False
source=python-3.13-docs-text/library/venv.txt page=8 page_id=lib-venv#p008 doc_type=library section="venv" --- Creation of virtual environments > API (cont.)

```text
 - The name of the virtual environment. Used for
        "__VENV_NAME__" in activation scripts (see
        "install_scripts()").

      * "prompt" - The prompt to be used by the activation scripts.
        Used for "__VENV_PROMPT__" in activation scripts (see
        "install_scripts()").

      * "executable" - The underlying Python executable used by the
        virtual environment. This takes into account the case where a
        virtual environment is created from another virtual
        en
```


## B t01 filter_applied=None

Q: If both the try block and the finally block contain a return statement, which value is returned?
Gold: [('tut-errors', [6])]


### rank 1 B:tut-errors:p006:c002 score=0.5563 hit=True
source=python-3.13-docs-text/tutorial/errors.txt page=6 page_id=tut-errors#p006 doc_type=tutorial section=8.7. Defining Clean-up Actions

```text
[8.7. Defining Clean-up Actions]
* An exception could occur during execution of an "except" or "else"
  clause. Again, the exception is re-raised after the "finally" clause
  has been executed.

* If the "finally" clause executes a "break", "continue" or "return"
  statement, exceptions are not re-raised.

* If the "try" statement reaches a "break", "continue" or "return"
  statement, the "finally" clause will execute just prior to the
  "break", "continue" or "return" statement's execution.

* If a "finally" clause includes a "return" statement, the returned
  value will be the one from the "finally" clause's "return"
  statement, not the value from the "try" clause's "return" statement.

For example:

   >>> def bool_return():
   ...     try:
   ...         return True
   ...     finally:
   ...         return False
   ...
   >>> bool_return()
   False

A more complicated example:
```


### rank 2 B:tut-errors:p006:c001 score=0.4685 hit=False
source=python-3.13-docs-text/tutorial/errors.txt page=6 page_id=tut-errors#p006 doc_type=tutorial section=8.7. Defining Clean-up Actions

```text
[8.7. Defining Clean-up Actions]
The "try" statement has another optional clause which is intended to
define clean-up actions that must be executed under all circumstances.
For example:

   >>> try:
   ...     raise KeyboardInterrupt
   ... finally:
   ...     print('Goodbye, world!')
   ...
   Goodbye, world!
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
       raise KeyboardInterrupt
   KeyboardInterrupt

If a "finally" clause is present, the "finally" clause will execute as
the last task before the "try" statement completes. The "finally"
clause runs whether or not the "try" statement produces an exception.
The following points discuss more complex cases when an exception
occurs:

* If an exception occurs during execution of the "try" clause, the
  exception may be handled by an "except" clause. If the exception is
  not handled by an "except" clause, the exception is re-raised after
  the "finally" clause has been executed.
```


### rank 3 B:tut-controlflow:p003:c003 score=0.4395 hit=False
source=python-3.13-docs-text/tutorial/controlflow.txt page=3 page_id=tut-controlflow#p003 doc_type=tutorial section=4.5. "else" Clauses on Loops

```text
[4.5. "else" Clauses on Loops]
When used with a loop, the "else" clause has more in common with the
"else" clause of a "try" statement than it does with that of "if"
statements: a "try" statement's "else" clause runs when no exception
occurs, and a loop's "else" clause runs when no "break" occurs. For
more on the "try" statement and exceptions, see Handling Exceptions.
```


## B t02 filter_applied=None

Q: Which locations is sys.path initialized from?
Gold: [('tut-modules', [3])]


### rank 1 B:tut-modules:p005:c001 score=0.6185 hit=False
source=python-3.13-docs-text/tutorial/modules.txt page=5 page_id=tut-modules#p005 doc_type=tutorial section=6.2. Standard Modules

```text
[6.2. Standard Modules]
The variable "sys.path" is a list of strings that determines the
interpreter's search path for modules. It is initialized to a default
path taken from the environment variable "PYTHONPATH", or from a
built-in default if "PYTHONPATH" is not set.  You can modify it using
standard list operations:

   >>> import sys
   >>> sys.path.append('/ufs/guido/lib/python')
```


### rank 2 B:tut-modules:p003:c002 score=0.5161 hit=False
source=python-3.13-docs-text/tutorial/modules.txt page=3 page_id=tut-modules#p003 doc_type=tutorial section=6.1.2. The Module Search Path

```text
[6.1.2. The Module Search Path]
  On file systems which support symlinks, the directory containing the
  input script is calculated after the symlink is followed. In other
  words the directory containing the symlink is **not** added to the
  module search path.

After initialization, Python programs can modify "sys.path".  The
directory containing the script being run is placed at the beginning
of the search path, ahead of the standard library path. This means
that scripts in that directory will be loaded instead of modules of
the same name in the library directory. This is an error unless the
replacement is intended.  See section Standard Modules for more
information.
```


### rank 3 B:tut-modules:p003:c001 score=0.5066 hit=True
source=python-3.13-docs-text/tutorial/modules.txt page=3 page_id=tut-modules#p003 doc_type=tutorial section=6.1.2. The Module Search Path

```text
[6.1.2. The Module Search Path]
When a module named "spam" is imported, the interpreter first searches
for a built-in module with that name. These module names are listed in
"sys.builtin_module_names". If not found, it then searches for a file
named "spam.py" in a list of directories given by the variable
"sys.path".  "sys.path" is initialized from these locations:

* The directory containing the input script (or the current directory
  when no file is specified).

* "PYTHONPATH" (a list of directory names, with the same syntax as the
  shell variable "PATH").

* The installation-dependent default (by convention including a "site-
  packages" directory, handled by the "site" module).

More details are at The initialization of the sys.path module search
path.

Note:
```


## B t03 filter_applied=None

Q: How should a file be opened before passing it to csv.reader?
Gold: [('lib-csv', [2])]


### rank 1 B:lib-csv:p002:c000 score=0.5886 hit=True
source=python-3.13-docs-text/library/csv.txt page=2 page_id=lib-csv#p002 doc_type=library section=Module Contents

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


### rank 2 B:lib-csv:p013:c000 score=0.5876 hit=False
source=python-3.13-docs-text/library/csv.txt page=13 page_id=lib-csv#p013 doc_type=library section=Examples

```text
[Examples]
The simplest example of reading a CSV file:

   import csv
   with open('some.csv', newline='') as f:
       reader = csv.reader(f)
       for row in reader:
           print(row)

Reading a file with an alternate format:

   import csv
   with open('passwd', newline='') as f:
       reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
       for row in reader:
           print(row)

The corresponding simplest possible writing example is:

   import csv
   with open('some.csv', 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerows(someiterable)

Since "open()" is used to open a CSV file for reading, the file will
by default be decoded into unicode using the system default encoding
(see "locale.getencoding()").  To decode a file using a different
encoding, use the "encoding" argument of open:

   import csv
   with open('some.csv', newline='', encoding='utf-8') as f:
       reader = csv.reader(f)
       for row in reader:
           print(row)
```


### rank 3 B:lib-csv:p008:c001 score=0.5531 hit=False
source=python-3.13-docs-text/library/csv.txt page=8 page_id=lib-csv#p008 doc_type=library section="csv" --- CSV File Reading and Writing > Module Contents (cont.)

```text
["csv" --- CSV File Reading and Writing > Module Contents (cont.)]
   with open('example.csv', newline='') as csvfile:
       dialect = csv.Sniffer().sniff(csvfile.read(1024))
       csvfile.seek(0)
       reader = csv.reader(csvfile, dialect)
       # ... process CSV file contents here ...

The "csv" module defines the following constants:

csv.QUOTE_ALL

   Instructs "writer" objects to quote all fields.

csv.QUOTE_MINIMAL

   Instructs "writer" objects to only quote those fields which contain
   special characters such as *delimiter*, *quotechar*, "'\r'", "'\n'"
   or any of the characters in *lineterminator*. If *doublequote* is
   "False" and *escapechar* is set, the *quotechar* is escaped instead
   of causing the field to be quoted.

csv.QUOTE_NONNUMERIC

   Instructs "writer" objects to quote all non-numeric fields.
```


## B t04 filter_applied=None

Q: What happens to lru_cache when maxsize is None?
Gold: [('lib-functools', [5])]


### rank 1 B:lib-functools:p005:c000 score=0.6161 hit=True
source=python-3.13-docs-text/library/functools.txt page=5 page_id=lib-functools#p005 doc_type=library section="functools" --- Higher-order functions and operations on callable objects (cont.)

```text
["functools" --- Higher-order functions and operations on callable objects (cont.)]
   If *user_function* is specified, it must be a callable. This allows
   the *lru_cache* decorator to be applied directly to a user
   function, leaving the *maxsize* at its default value of 128:

      @lru_cache
      def count_vowels(sentence):
          return sum(sentence.count(vowel) for vowel in 'AEIOUaeiou')

   If *maxsize* is set to "None", the LRU feature is disabled and the
   cache can grow without bound.

   If *typed* is set to true, function arguments of different types
   will be cached separately.  If *typed* is false, the implementation
   will usually regard them as equivalent calls and only cache a
   single result. (Some types such as *str* and *int* may be cached
   separately even when *typed* is false.)
```


### rank 2 B:lib-functools:p006:c000 score=0.5563 hit=False
source=python-3.13-docs-text/library/functools.txt page=6 page_id=lib-functools#p006 doc_type=library section="functools" --- Higher-order functions and operations on callable objects (cont.)

```text
["functools" --- Higher-order functions and operations on callable objects (cont.)]
   The decorator also provides a "cache_clear()" function for clearing
   or invalidating the cache.

   The original underlying function is accessible through the
   "__wrapped__" attribute.  This is useful for introspection, for
   bypassing the cache, or for rewrapping the function with a
   different cache.

   The cache keeps references to the arguments and return values until
   they age out of the cache or until the cache is cleared.

   If a method is cached, the "self" instance argument is included in
   the cache.  See How do I cache method calls?

   An LRU (least recently used) cache works best when the most recent
   calls are the best predictors of upcoming calls (for example, the
   most popular articles on a news server tend to change each day).
   The cache's size limit assures that the cache does not grow without
   bound on long-running processes such as web servers.
```


### rank 3 B:lib-functools:p006:c001 score=0.5318 hit=False
source=python-3.13-docs-text/library/functools.txt page=6 page_id=lib-functools#p006 doc_type=library section="functools" --- Higher-order functions and operations on callable objects (cont.)

```text
["functools" --- Higher-order functions and operations on callable objects (cont.)]
   In general, the LRU cache should only be used when you want to
   reuse previously computed values.  Accordingly, it doesn't make
   sense to cache functions with side-effects, functions that need to
   create distinct mutable objects on each call (such as generators
   and async functions), or impure functions such as time() or
   random().

   Example of an LRU cache for static web content:

      @lru_cache(maxsize=32)
      def get_pep(num):
          'Retrieve text of a Python Enhancement Proposal'
          resource = f'https://peps.python.org/pep-{num:04d}'
          try:
              with urllib.request.urlopen(resource) as s:
                  return s.read()
          except urllib.error.HTTPError:
              return 'Not Found'
```


## B t05 filter_applied=None

Q: In the library reference: why may a dictionary not equal the original after converting it to JSON and back?
Gold: [('lib-json', [5])]


### rank 1 B:tut-datastructures:p008:c001 score=0.5286 hit=False
source=python-3.13-docs-text/tutorial/datastructures.txt page=8 page_id=tut-datastructures#p008 doc_type=tutorial section=5.5. Dictionaries

```text
[5.5. Dictionaries]
It is best to think of a dictionary as a set of *key: value* pairs,
with the requirement that the keys are unique (within one dictionary).
A pair of braces creates an empty dictionary: "{}". Placing a comma-
separated list of key:value pairs within the braces adds initial
key:value pairs to the dictionary; this is also the way dictionaries
are written on output.

The main operations on a dictionary are storing a value with some key
and extracting the value given the key.  It is also possible to delete
a key:value pair with "del". If you store using a key that is already
in use, the old value associated with that key is forgotten.

Extracting a value for a non-existent key by subscripting ("d[key]")
raises a "KeyError". To avoid getting this error when trying to access
a possibly non-existent key, use the "get()" method instead, which
returns "None" (or a specified default value) if the key is not in the
dictionary.
```


### rank 2 B:lib-json:p005:c000 score=0.4801 hit=True
source=python-3.13-docs-text/library/json.txt page=5 page_id=lib-json#p005 doc_type=library section="json" --- JSON encoder and decoder > Basic Usage (cont.)

```text
["json" --- JSON encoder and decoder > Basic Usage (cont.)]
      * **sort_keys** (*bool*) -- If "True", dictionaries will be
        outputted sorted by key. Default "False".

   Note:

     Keys in key/value pairs of JSON are always of the type "str".
     When a dictionary is converted into JSON, all the keys of the
     dictionary are converted to strings. As a result of this, if a
     dictionary is converted into JSON and then back into a
     dictionary, the dictionary may not equal the original one. That
     is, "loads(dumps(x)) != x" if x has non-string keys. *sort_keys*
     sorts the keys before they are converted to strings, so numeric
     keys are sorted by value, not by their string representation.

   Changed in version 3.2: Allow strings for *indent* in addition to
   integers.

   Changed in version 3.4: Use "(',', ': ')" as default if *indent* is
   not "None".

   Changed in version 3.6: All optional parameters are now keyword-
   only.
```


### rank 3 B:lib-json:p001:c000 score=0.474 hit=False
source=python-3.13-docs-text/library/json.txt page=1 page_id=lib-json#p001 doc_type=library section="json" --- JSON encoder and decoder

```text
["json" --- JSON encoder and decoder]
**Source code:** Lib/json/__init__.py

======================================================================

JSON (JavaScript Object Notation), specified by **RFC 7159** (which
obsoletes **RFC 4627**) and by ECMA-404, is a lightweight data
interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [1] ).

Note:

  The term "object" in the context of JSON processing in Python can be
  ambiguous. All values in Python are objects. In JSON, an object
  refers to any data wrapped in curly braces, similar to a Python
  dictionary.

Warning:

  Be cautious when parsing JSON data from untrusted sources. A
  malicious JSON string may cause the decoder to consume considerable
  CPU and memory resources. Limiting the size of data to be parsed is
  recommended.

This module exposes an API familiar to users of the standard library
"marshal" and "pickle" modules.

Encoding basic Python object hierarchies:
```


## B t06 filter_applied=None

Q: Following the tutorial, how do I activate a virtual environment on Windows?
Gold: [('tut-venv', [1])]


### rank 1 B:lib-venv:p005:c000 score=0.5826 hit=False
source=python-3.13-docs-text/library/venv.txt page=5 page_id=lib-venv#p005 doc_type=library section="venv" --- Creation of virtual environments > How venvs work (cont.)

```text
["venv" --- Creation of virtual environments > How venvs work (cont.)]
Added in version 3.4: **fish** and **csh** activation scripts.

Added in version 3.8: PowerShell activation scripts installed under
POSIX for PowerShell Core support.

You don't specifically *need* to activate a virtual environment, as
you can just specify the full path to that environment's Python
interpreter when invoking Python. Furthermore, all scripts installed
in the environment should be runnable without activating it.
```


### rank 2 B:lib-venv:p008:c001 score=0.521 hit=False
source=python-3.13-docs-text/library/venv.txt page=8 page_id=lib-venv#p008 doc_type=library section="venv" --- Creation of virtual environments > API (cont.)

```text
["venv" --- Creation of virtual environments > API (cont.)]
      * "env_name" - The name of the virtual environment. Used for
        "__VENV_NAME__" in activation scripts (see
        "install_scripts()").

      * "prompt" - The prompt to be used by the activation scripts.
        Used for "__VENV_PROMPT__" in activation scripts (see
        "install_scripts()").

      * "executable" - The underlying Python executable used by the
        virtual environment. This takes into account the case where a
        virtual environment is created from another virtual
        environment.

      * "inc_path" - The include path for the virtual environment.

      * "lib_path" - The purelib path for the virtual environment.
```


### rank 3 B:tut-venv:p001:c003 score=0.5172 hit=True
source=python-3.13-docs-text/tutorial/venv.txt page=1 page_id=tut-venv#p001 doc_type=tutorial section=12. Virtual Environments and Packages > 12.2. Creating Virtual Environments

```text
[12. Virtual Environments and Packages > 12.2. Creating Virtual Environments]
A common directory location for a virtual environment is ".venv". This
name keeps the directory typically hidden in your shell and thus out
of the way while giving it a name that explains why the directory
exists. It also prevents clashing with ".env" environment variable
definition files that some tooling supports.

Once you've created a virtual environment, you may activate it.

On Windows, run:

   tutorial-env\Scripts\activate

On Unix or MacOS, run:

   source tutorial-env/bin/activate

(This script is written for the bash shell.  If you use the **csh** or
**fish** shells, there are alternate "activate.csh" and
"activate.fish" scripts you should use instead.)

Activating the virtual environment will change your shell's prompt to
show what virtual environment you're using, and modify the environment
so that running "python" will get you that particular version and
installation of Python. For example:
```


## C t01 filter_applied=None

Q: If both the try block and the finally block contain a return statement, which value is returned?
Gold: [('tut-errors', [6])]


### rank 1 C:tut-errors:p006:c002 score=0.5563 hit=True
source=python-3.13-docs-text/tutorial/errors.txt page=6 page_id=tut-errors#p006 doc_type=tutorial section=8.7. Defining Clean-up Actions

```text
[8.7. Defining Clean-up Actions]
* An exception could occur during execution of an "except" or "else"
  clause. Again, the exception is re-raised after the "finally" clause
  has been executed.

* If the "finally" clause executes a "break", "continue" or "return"
  statement, exceptions are not re-raised.

* If the "try" statement reaches a "break", "continue" or "return"
  statement, the "finally" clause will execute just prior to the
  "break", "continue" or "return" statement's execution.

* If a "finally" clause includes a "return" statement, the returned
  value will be the one from the "finally" clause's "return"
  statement, not the value from the "try" clause's "return" statement.

For example:

   >>> def bool_return():
   ...     try:
   ...         return True
   ...     finally:
   ...         return False
   ...
   >>> bool_return()
   False

A more complicated example:
```


### rank 2 C:tut-errors:p006:c001 score=0.4685 hit=False
source=python-3.13-docs-text/tutorial/errors.txt page=6 page_id=tut-errors#p006 doc_type=tutorial section=8.7. Defining Clean-up Actions

```text
[8.7. Defining Clean-up Actions]
The "try" statement has another optional clause which is intended to
define clean-up actions that must be executed under all circumstances.
For example:

   >>> try:
   ...     raise KeyboardInterrupt
   ... finally:
   ...     print('Goodbye, world!')
   ...
   Goodbye, world!
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
       raise KeyboardInterrupt
   KeyboardInterrupt

If a "finally" clause is present, the "finally" clause will execute as
the last task before the "try" statement completes. The "finally"
clause runs whether or not the "try" statement produces an exception.
The following points discuss more complex cases when an exception
occurs:

* If an exception occurs during execution of the "try" clause, the
  exception may be handled by an "except" clause. If the exception is
  not handled by an "except" clause, the exception is re-raised after
  the "finally" clause has been executed.
```


### rank 3 C:tut-controlflow:p003:c003 score=0.4395 hit=False
source=python-3.13-docs-text/tutorial/controlflow.txt page=3 page_id=tut-controlflow#p003 doc_type=tutorial section=4.5. "else" Clauses on Loops

```text
[4.5. "else" Clauses on Loops]
When used with a loop, the "else" clause has more in common with the
"else" clause of a "try" statement than it does with that of "if"
statements: a "try" statement's "else" clause runs when no exception
occurs, and a loop's "else" clause runs when no "break" occurs. For
more on the "try" statement and exceptions, see Handling Exceptions.
```


## C t02 filter_applied=None

Q: Which locations is sys.path initialized from?
Gold: [('tut-modules', [3])]


### rank 1 C:tut-modules:p005:c001 score=0.6185 hit=False
source=python-3.13-docs-text/tutorial/modules.txt page=5 page_id=tut-modules#p005 doc_type=tutorial section=6.2. Standard Modules

```text
[6.2. Standard Modules]
The variable "sys.path" is a list of strings that determines the
interpreter's search path for modules. It is initialized to a default
path taken from the environment variable "PYTHONPATH", or from a
built-in default if "PYTHONPATH" is not set.  You can modify it using
standard list operations:

   >>> import sys
   >>> sys.path.append('/ufs/guido/lib/python')
```


### rank 2 C:tut-modules:p003:c002 score=0.5161 hit=False
source=python-3.13-docs-text/tutorial/modules.txt page=3 page_id=tut-modules#p003 doc_type=tutorial section=6.1.2. The Module Search Path

```text
[6.1.2. The Module Search Path]
  On file systems which support symlinks, the directory containing the
  input script is calculated after the symlink is followed. In other
  words the directory containing the symlink is **not** added to the
  module search path.

After initialization, Python programs can modify "sys.path".  The
directory containing the script being run is placed at the beginning
of the search path, ahead of the standard library path. This means
that scripts in that directory will be loaded instead of modules of
the same name in the library directory. This is an error unless the
replacement is intended.  See section Standard Modules for more
information.
```


### rank 3 C:tut-modules:p003:c001 score=0.5066 hit=True
source=python-3.13-docs-text/tutorial/modules.txt page=3 page_id=tut-modules#p003 doc_type=tutorial section=6.1.2. The Module Search Path

```text
[6.1.2. The Module Search Path]
When a module named "spam" is imported, the interpreter first searches
for a built-in module with that name. These module names are listed in
"sys.builtin_module_names". If not found, it then searches for a file
named "spam.py" in a list of directories given by the variable
"sys.path".  "sys.path" is initialized from these locations:

* The directory containing the input script (or the current directory
  when no file is specified).

* "PYTHONPATH" (a list of directory names, with the same syntax as the
  shell variable "PATH").

* The installation-dependent default (by convention including a "site-
  packages" directory, handled by the "site" module).

More details are at The initialization of the sys.path module search
path.

Note:
```


## C t03 filter_applied=None

Q: How should a file be opened before passing it to csv.reader?
Gold: [('lib-csv', [2])]


### rank 1 C:lib-csv:p002:c000 score=0.5886 hit=True
source=python-3.13-docs-text/library/csv.txt page=2 page_id=lib-csv#p002 doc_type=library section=Module Contents

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


### rank 2 C:lib-csv:p013:c000 score=0.5876 hit=False
source=python-3.13-docs-text/library/csv.txt page=13 page_id=lib-csv#p013 doc_type=library section=Examples

```text
[Examples]
The simplest example of reading a CSV file:

   import csv
   with open('some.csv', newline='') as f:
       reader = csv.reader(f)
       for row in reader:
           print(row)

Reading a file with an alternate format:

   import csv
   with open('passwd', newline='') as f:
       reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
       for row in reader:
           print(row)

The corresponding simplest possible writing example is:

   import csv
   with open('some.csv', 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerows(someiterable)

Since "open()" is used to open a CSV file for reading, the file will
by default be decoded into unicode using the system default encoding
(see "locale.getencoding()").  To decode a file using a different
encoding, use the "encoding" argument of open:

   import csv
   with open('some.csv', newline='', encoding='utf-8') as f:
       reader = csv.reader(f)
       for row in reader:
           print(row)
```


### rank 3 C:lib-csv:p008:c001 score=0.5531 hit=False
source=python-3.13-docs-text/library/csv.txt page=8 page_id=lib-csv#p008 doc_type=library section="csv" --- CSV File Reading and Writing > Module Contents (cont.)

```text
["csv" --- CSV File Reading and Writing > Module Contents (cont.)]
   with open('example.csv', newline='') as csvfile:
       dialect = csv.Sniffer().sniff(csvfile.read(1024))
       csvfile.seek(0)
       reader = csv.reader(csvfile, dialect)
       # ... process CSV file contents here ...

The "csv" module defines the following constants:

csv.QUOTE_ALL

   Instructs "writer" objects to quote all fields.

csv.QUOTE_MINIMAL

   Instructs "writer" objects to only quote those fields which contain
   special characters such as *delimiter*, *quotechar*, "'\r'", "'\n'"
   or any of the characters in *lineterminator*. If *doublequote* is
   "False" and *escapechar* is set, the *quotechar* is escaped instead
   of causing the field to be quoted.

csv.QUOTE_NONNUMERIC

   Instructs "writer" objects to quote all non-numeric fields.
```


## C t04 filter_applied=None

Q: What happens to lru_cache when maxsize is None?
Gold: [('lib-functools', [5])]


### rank 1 C:lib-functools:p005:c000 score=0.6161 hit=True
source=python-3.13-docs-text/library/functools.txt page=5 page_id=lib-functools#p005 doc_type=library section="functools" --- Higher-order functions and operations on callable objects (cont.)

```text
["functools" --- Higher-order functions and operations on callable objects (cont.)]
   If *user_function* is specified, it must be a callable. This allows
   the *lru_cache* decorator to be applied directly to a user
   function, leaving the *maxsize* at its default value of 128:

      @lru_cache
      def count_vowels(sentence):
          return sum(sentence.count(vowel) for vowel in 'AEIOUaeiou')

   If *maxsize* is set to "None", the LRU feature is disabled and the
   cache can grow without bound.

   If *typed* is set to true, function arguments of different types
   will be cached separately.  If *typed* is false, the implementation
   will usually regard them as equivalent calls and only cache a
   single result. (Some types such as *str* and *int* may be cached
   separately even when *typed* is false.)
```


### rank 2 C:lib-functools:p006:c000 score=0.5563 hit=False
source=python-3.13-docs-text/library/functools.txt page=6 page_id=lib-functools#p006 doc_type=library section="functools" --- Higher-order functions and operations on callable objects (cont.)

```text
["functools" --- Higher-order functions and operations on callable objects (cont.)]
   The decorator also provides a "cache_clear()" function for clearing
   or invalidating the cache.

   The original underlying function is accessible through the
   "__wrapped__" attribute.  This is useful for introspection, for
   bypassing the cache, or for rewrapping the function with a
   different cache.

   The cache keeps references to the arguments and return values until
   they age out of the cache or until the cache is cleared.

   If a method is cached, the "self" instance argument is included in
   the cache.  See How do I cache method calls?

   An LRU (least recently used) cache works best when the most recent
   calls are the best predictors of upcoming calls (for example, the
   most popular articles on a news server tend to change each day).
   The cache's size limit assures that the cache does not grow without
   bound on long-running processes such as web servers.
```


### rank 3 C:lib-functools:p006:c001 score=0.5318 hit=False
source=python-3.13-docs-text/library/functools.txt page=6 page_id=lib-functools#p006 doc_type=library section="functools" --- Higher-order functions and operations on callable objects (cont.)

```text
["functools" --- Higher-order functions and operations on callable objects (cont.)]
   In general, the LRU cache should only be used when you want to
   reuse previously computed values.  Accordingly, it doesn't make
   sense to cache functions with side-effects, functions that need to
   create distinct mutable objects on each call (such as generators
   and async functions), or impure functions such as time() or
   random().

   Example of an LRU cache for static web content:

      @lru_cache(maxsize=32)
      def get_pep(num):
          'Retrieve text of a Python Enhancement Proposal'
          resource = f'https://peps.python.org/pep-{num:04d}'
          try:
              with urllib.request.urlopen(resource) as s:
                  return s.read()
          except urllib.error.HTTPError:
              return 'Not Found'
```


## C t05 filter_applied={'doc_type': 'library'}

Q: In the library reference: why may a dictionary not equal the original after converting it to JSON and back?
Gold: [('lib-json', [5])]


### rank 1 C:lib-json:p005:c000 score=0.4801 hit=True
source=python-3.13-docs-text/library/json.txt page=5 page_id=lib-json#p005 doc_type=library section="json" --- JSON encoder and decoder > Basic Usage (cont.)

```text
["json" --- JSON encoder and decoder > Basic Usage (cont.)]
      * **sort_keys** (*bool*) -- If "True", dictionaries will be
        outputted sorted by key. Default "False".

   Note:

     Keys in key/value pairs of JSON are always of the type "str".
     When a dictionary is converted into JSON, all the keys of the
     dictionary are converted to strings. As a result of this, if a
     dictionary is converted into JSON and then back into a
     dictionary, the dictionary may not equal the original one. That
     is, "loads(dumps(x)) != x" if x has non-string keys. *sort_keys*
     sorts the keys before they are converted to strings, so numeric
     keys are sorted by value, not by their string representation.

   Changed in version 3.2: Allow strings for *indent* in addition to
   integers.

   Changed in version 3.4: Use "(',', ': ')" as default if *indent* is
   not "None".

   Changed in version 3.6: All optional parameters are now keyword-
   only.
```


### rank 2 C:lib-json:p001:c000 score=0.474 hit=False
source=python-3.13-docs-text/library/json.txt page=1 page_id=lib-json#p001 doc_type=library section="json" --- JSON encoder and decoder

```text
["json" --- JSON encoder and decoder]
**Source code:** Lib/json/__init__.py

======================================================================

JSON (JavaScript Object Notation), specified by **RFC 7159** (which
obsoletes **RFC 4627**) and by ECMA-404, is a lightweight data
interchange format inspired by JavaScript object literal syntax
(although it is not a strict subset of JavaScript [1] ).

Note:

  The term "object" in the context of JSON processing in Python can be
  ambiguous. All values in Python are objects. In JSON, an object
  refers to any data wrapped in curly braces, similar to a Python
  dictionary.

Warning:

  Be cautious when parsing JSON data from untrusted sources. A
  malicious JSON string may cause the decoder to consume considerable
  CPU and memory resources. Limiting the size of data to be parsed is
  recommended.

This module exposes an API familiar to users of the standard library
"marshal" and "pickle" modules.

Encoding basic Python object hierarchies:
```


### rank 3 C:lib-json:p011:c001 score=0.4422 hit=False
source=python-3.13-docs-text/library/json.txt page=11 page_id=lib-json#p011 doc_type=library section="json" --- JSON encoder and decoder > Encoders and Decoders (cont.)

```text
["json" --- JSON encoder and decoder > Encoders and Decoders (cont.)]
   If *check_circular* is true (the default), then lists, dicts, and
   custom encoded objects will be checked for circular references
   during encoding to prevent an infinite recursion (which would cause
   a "RecursionError"). Otherwise, no such check takes place.

   If *allow_nan* is true (the default), then "NaN", "Infinity", and
   "-Infinity" will be encoded as such.  This behavior is not JSON
   specification compliant, but is consistent with most JavaScript
   based encoders and decoders.  Otherwise, it will be a "ValueError"
   to encode such floats.

   If *sort_keys* is true (default: "False"), then the output of
   dictionaries will be sorted by key; this is useful for regression
   tests to ensure that JSON serializations can be compared on a day-
   to-day basis.
```


## C t06 filter_applied={'doc_type': 'tutorial'}

Q: Following the tutorial, how do I activate a virtual environment on Windows?
Gold: [('tut-venv', [1])]


### rank 1 C:tut-venv:p001:c003 score=0.5172 hit=True
source=python-3.13-docs-text/tutorial/venv.txt page=1 page_id=tut-venv#p001 doc_type=tutorial section=12. Virtual Environments and Packages > 12.2. Creating Virtual Environments

```text
[12. Virtual Environments and Packages > 12.2. Creating Virtual Environments]
A common directory location for a virtual environment is ".venv". This
name keeps the directory typically hidden in your shell and thus out
of the way while giving it a name that explains why the directory
exists. It also prevents clashing with ".env" environment variable
definition files that some tooling supports.

Once you've created a virtual environment, you may activate it.

On Windows, run:

   tutorial-env\Scripts\activate

On Unix or MacOS, run:

   source tutorial-env/bin/activate

(This script is written for the bash shell.  If you use the **csh** or
**fish** shells, there are alternate "activate.csh" and
"activate.fish" scripts you should use instead.)

Activating the virtual environment will change your shell's prompt to
show what virtual environment you're using, and modify the environment
so that running "python" will get you that particular version and
installation of Python. For example:
```


### rank 2 C:tut-venv:p001:c002 score=0.4825 hit=False
source=python-3.13-docs-text/tutorial/venv.txt page=1 page_id=tut-venv#p001 doc_type=tutorial section=12. Virtual Environments and Packages > 12.2. Creating Virtual Environments

```text
[12. Virtual Environments and Packages > 12.2. Creating Virtual Environments]
The module used to create and manage virtual environments is called
"venv".  "venv" will install the Python version from which the command
was run (as reported by the "--version" option). For instance,
executing the command with "python3.12" will install version 3.12.

To create a virtual environment, decide upon a directory where you
want to place it, and run the "venv" module as a script with the
directory path:

   python -m venv tutorial-env

This will create the "tutorial-env" directory if it doesn't exist, and
also create directories inside it containing a copy of the Python
interpreter and various supporting files.
```


### rank 3 C:tut-venv:p001:c004 score=0.4191 hit=False
source=python-3.13-docs-text/tutorial/venv.txt page=1 page_id=tut-venv#p001 doc_type=tutorial section=12. Virtual Environments and Packages > 12.2. Creating Virtual Environments

```text
[12. Virtual Environments and Packages > 12.2. Creating Virtual Environments]
   $ source ~/envs/tutorial-env/bin/activate
   (tutorial-env) $ python
   Python 3.5.1 (default, May  6 2016, 10:59:36)
     ...
   >>> import sys
   >>> sys.path
   ['', '/usr/local/lib/python35.zip', ...,
   '~/envs/tutorial-env/lib/python3.5/site-packages']
   >>>

Note that the activated virtual environment does not alter the
"PYTHONPATH" variable in any way. This may lead to unexpected results
if the path includes references to code which is incompatible with the
Python version the virtual environment is using. The best practice is
to "unset PYTHONPATH" in bash or the equivalent for the shell you are
using.

To deactivate a virtual environment, type:

   deactivate

into the terminal.
```
