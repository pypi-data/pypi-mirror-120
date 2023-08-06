""" 
easy_import.py
    by NerdyTurke Sept 2021

Makes python modules and packages anywhere visible for easy import


# ==========================
# easy_import.py example Use
# ==========================
# I have no idea where on my computer the module 'data_tools.py 'is,
# nor where the package 'audio' is.
# Note: assumes 'audio' has not been pip installed.
 
# EasyImport will search the entire storage to find these items and make them visible
# for import as though they were in current working directory.

# Locations are cached to json files in the CWD for faster access next time.
# There is one cache for modules and one for packages.

# The cached location can be ignored, e.g. to make a new search in case the
# location has changed by setting optional param use_cached=False

# The search can be narrowed down to a particular directory tree by setting
# optional param search_dir = "directory_path" where "directory_path" is whatever
# path is required.

from easy_import import EasyImport


with EasyImport("data_tools.py"):
    # import smooth function from data_tools.py
    from data_tools import smooth


with EasyImport("audio", is_package=True):
    # import SFX class from audio.sfx
    from audio.sfx import SFX 
.
.

smoothed_data = smooth(data)

.
.
.
my_sfx = SFX()
.
.
.

"""

__version__ = "0.2"
__author__ = "NerdyTurkey"


import os
from pathlib import Path
import json
import sys

PACKAGE_CACHE_FNAME = "__package_cached_paths.json"
MODULE_CACHE_FNAME = "__module_cached_paths.json"


def find_file(name, search_dir=None):
    """ 
    Searches for file 'name' in search_dir and returns paths of all its found
    locations, or an empty list if not found.
    
    If search_dir is None (default), the entire storage is searched, e.g. C:\
    
    """
    if search_dir is None:
        # search entire storage, e.g. "C:\"
        search_dir = Path(os.getcwd()).anchor
    result = []
    for root, dirs, files in os.walk(search_dir):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def find_directory(name, search_dir):
    """ 
    Searches for directory 'name' in search_dir and returns paths of all its found
    locations, or an empty list if not found.
    
    If search_dir is None (default), the entire storage is searched, e.g. C:\
    
    """
    if search_dir is None:
        # search entire storage, e.g. "C:\"
        search_dir = Path(os.getcwd()).anchor
    result = []
    for root, dirs, files in os.walk(search_dir):
        if name in dirs:
            result.append(os.path.join(root, name))
    return result


class EasyImport:
    """
    Class-based context manager.
    
    Searches for 'name' and if found, inserts the path of its parent directory
    into the system path to allow item to be imported as though it was in the
    current working directory.
    
    If is_package is False (default), name is assumed to be module (file),
    else name is assumed to be a package (directory with __init__.py).
    
    If search_dir is None (default), the entire storage is searched, else just
    the search_dir tree (top-down).
    
    Searching the entire storage is slow, so once the path is found it is 
    cached for next time. The cache is a dictionary that is json dumped and loaded
    into the CWD. A different cache is used for modules and packages to allow for
    the same name being used for a package and a module.
    
    If use_cached is True, the cached value is used, else a new search is made.
    
    If name is not found, raises ModuleNotFoundError.
    
    If name is found in multiple locations, gives user chance to select desired
    path or quit. Quit raises SystemExit.
    
    """

    def __init__(
        self,
        name,
        is_package=False,
        search_dir=None,
        use_cached=True,
        clear_cache=False,
        verbose=True,
    ):
        if not isinstance(name, str):
            raise TypeError("name must be a string.")

        if search_dir is not None and not isinstance(search_dir, str):
            raise TypeError("search_dir must be a string.")

        self.name = name
        self.is_package = is_package
        self.search_dir = search_dir
        self.use_cached = use_cached
        self.clear_cache = clear_cache
        self.verbose = verbose

    def _init(self):
        self.path_inserted = False
        self.cached_paths_exists = True
        self.make_search = True
        self.cache_fname = (
            PACKAGE_CACHE_FNAME if self.is_package else MODULE_CACHE_FNAME
        )
    
    def _info(self, info):
        if self.verbose:
            print(f"\nINFO: {info}")
    
    def _warning(self, warning):
        """ may upgrade levels of verbose, hence this is not a staticmethod """
        print(f"\nWARNING: {warning}") 
        
    def _clear_cache(self):
        with open(self.cache_fname, "w") as f:
            json.dump({}, f)

    def _get_cached_paths(self):
        try:
            with open(self.cache_fname, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _use_cached(self):
        if self.cached_paths_exists:
            self.path = self.cached_paths.get(self.name, None)

            if self.path is not None:
                self.make_search = False
                self._info("Using cached path.")

        else:
            self._info("No paths cached yet.")

    def _get_search_result(self):
        self._info(f"Searching for {self.name}...")

        if self.is_package:
            result = find_directory(self.name, search_dir=self.search_dir)

        else:
            result = find_file(self.name, search_dir=self.search_dir)

        self._info("...finished.")

        return result

    def _process(self, result):
        if not result:
            self.path = None

        elif len(result) > 1:
            self._choose_path(result)

        else:
            self.path = str(Path(result[0]).resolve().parents[0])

        if self.path is None:
            raise ModuleNotFoundError(f"Failed. {self.name} not found")

    def _choose_path(self, result):
        self._warning(f"{self.name} found at multiple locations. Choose path:")
        self._info("0. Quit")

        for i, path in enumerate(result):
            self._info(f"{i+1}. {path}")

        while True:

            try:
                choice = int(input(f"Enter desired path (0 - {len(result)}) :"))

            except ValueError:
                self._warning("Invalid input !")
                continue

            if 0 <= choice <= len(result):
                break

            self._warning("Invalid choice !")

        if choice == 0:
            raise SystemExit("User quit. No path selected.")

        self.path = str(Path(result[choice - 1]).resolve().parents[0])

    def _update_cache(self):
        self._info("Saving path to cache...")
        self.cached_paths[self.name] = self.path

        with open(self.cache_fname, "w") as f:
            json.dump(self.cached_paths, f)

        self._info("...finished.")

    def _update_sys_path(self):
        sys.path.insert(0, self.path)
        self.path_inserted = True

    def __enter__(self):
        """ for context manager - called when entering with block """
        
        self._init()

        if self.clear_cache:
            self._clear_cache()

        self.cached_paths = self._get_cached_paths()

        if not self.cached_paths:
            self.cached_paths_exists = False

        if self.use_cached:
            self._use_cached()

        if self.make_search:
            result = self._get_search_result()
            self._process(result)

        if self.make_search:
            self._update_cache()

        self._update_sys_path()

        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ for context manager - called when exitting with block """
        if self.path_inserted:
            sys.path.pop(0)  # remove path to leave sys.path as it was before
            
