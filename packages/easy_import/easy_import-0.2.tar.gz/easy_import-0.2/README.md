# easy_import
Python imports made easy! Import any module or package from anywhere - as though it was in your current working directory.

## Installation
Requires python 3.

```bash
pip install easy_import
```

## Usage
```python
"""
data_tools.py is a (fictious) module located....somwehere on your computer. 
But not in the current working directory.

Directly trying to import it will raise an ImportError since its not visible.

easy_import to the rescue!

It will search the entire storage (or a given directory) for the module and make it visible
for importing as though it was in the current working directory.
"""

from easy_import import EasyImport
with EasyImport("data_tools.py"):
    import data_tools

# etc

"""
Now we can use a function or class in data_tools.py
e.g. :
"""
smoothed_data = data_tools.smooth(data)

"""
Since searching the entire storage is s l o w, the locations of searched items
are cached to json files so the next time you run it, it will be super fast!

Check out example.py in the repository for a runnable example and more details.
"""

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
