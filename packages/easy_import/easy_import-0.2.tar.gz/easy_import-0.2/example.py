# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 16:21:25 2021

@author: NerdyTurkey
"""


"""

example.py, a demo  of easy_import.py
--------------------------------------

First restart your IDE / clear your import history

The repository is structured as follows: 

    
├───easy import
    ├───another_directory
    │   ├───sub_directory
    │   │     ├──my_package
    │   │     │   ├───__init__.py
    │   │     │   └───treble_module.py    
    │   │     └───a_script.py    
    │   ├───double_module.py
    │   └───a_script.py
    ├───easy_import.py
    └───example.py
"""


# First, let's try and directly import the double() function from 'double_module.py'

try:
    from double_module import double
except ImportError:
    print("Direct import of 'double_module.py' failed !")


# Second, let's try and directly import 'treble_module.py' from the package
# 'my_package'

try:
    from my_package import treble_module
except ImportError:
    print("Direct import of 'treble_module.py' from 'my_package' failed !")


# These both failed because 'double_module.py' and 'my_package' are not in the
# current working directory.


# Now let's use easy_import!

from easy_import import EasyImport

with EasyImport("double_module.py"):
    from double_module import double
print(double(2))

with EasyImport("my_package", is_package=True):
    from my_package import treble_module
print(treble_module.treble(2))


"""
EasyImport has searched the entire storage for these items.

Since this can be slow, the locations are cached in json files in the CWD 
(one for modules and one for packages).This means that the next time we run this,
the cached locations can be used, which is very fast.

We could have given EasyImport a helping hand by specifying the directory tree
containing the module or package, by using the optional argument
search_dir=<path of tree to search>. 

Here is the full list of optional arguments and their default values:
    
    is_package=False: if False search for module (.py script), else search for
    package
    
    search_dir=None: use this to pass the path of the directory tree you want
    to search. If omitted, the entire storage is searched.
    
    use_cached=True: if True, the cached location is used if it exists, else a
    new search is made and the cached value updated.
    
    clear_cache=False, if True, the entire module or package cache is cleared,
    depending on whether is_package=False or is_package=True
    
    verbose=True: if True, display progress info, else suppress them

"""

# ============================================================================

"""
BUT...what happens if there is more than one module or package with the same name?

If this is the case, then EasyImport will display all the options and allow you to
choose which one you want to use.


In the example below, we want the 'a_script.py' in 'sub_directory'  not the 
one in 'another_dirctory'.

EasyImport will give us the choice first time we search for it. Then, as before,
the cached location will be used subsequently, unless we set use_cached=False or
clear_cache=True.
"""

with EasyImport("a_script.py"):
    from a_script import quadruple
print(quadruple(2))
