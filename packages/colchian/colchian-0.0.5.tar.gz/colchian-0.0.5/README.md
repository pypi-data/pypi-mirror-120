# Colchian

In Greek mythology, the Colchian Dragon guarded the Golden Fleece. Jason was sent on a quest to obtain the Golden Fleece, to prove himself worthy as king - but the Colchian Dragon was the final obstacle (after many others) stopping Jason from obtaining the fleece.

The `colchian` package contains the `Colchian` class, which can be used to validate .json documents, or rather the Python `dict` resulting from loading a .json file with `json.load()`.

Colchian was developed with validation of Conffu (https://pypi.org/project/conffu/) configurations in mind, but will work for any reasonably sized .json file (no testing was performed for large documents, nor has the code been optimised for performance).

## Installation

Colchian is available from PyPI:
```commandline
pip install colchian
```

## Usage

A very simple example:
```python
from colchian import Colchian
from json import load, dumps

type_dict = {
    "an integer": int,
    "some strings": [str]
}

with open('my.json') as f:
    data = load(f)
    try:
        valid_data = Colchian.validated(data, type_dict)
        print(f'Valid:\n{dumps(valid_data)}')
    except SyntaxError as e:
        print(f'Something is wrong: {e}')
```
A valid `my.json`:
```json
{
  "an integer": 42,
  "some strings": ["vastly", "hugely", "mind-bogglingly", "big"]
}
```

To use Colchian:
- create a dictionary that defines the structure and types of a valid data dictionary (from a .json document);
- call `Colchian.validated()` with the data and the type dictionary;
- the result will be the same data, with some data casted to the appropriate type, if `strict=False` is passed to the `.validated()` method;
- a SyntaxError exception will be raised if the data is not valid according top the type_dict.

A few more tricks:
- use the Python `typing` module to use special types like `Union`, `Any`, `List` or `Optional`;
- use wildcards (keys starting with `*`) to define elements that may appear with any name (and repeatedly);
- instead of `typing.Union`, you can also use a tuple to indicate multiple options (for example `(int, float)` for a number field);
- assign a function as a type to perform custom validation or transformation on elements.

These two type dictionaries function identically:
```python
type_dict1 = {
    'words': [str],
    'secret': (bool, None)
}

type_dict2 = {
    'words': List[str],
    'secret': Optional[bool]
}
```

When setting functions as a type, make sure they match this signature:
```python
def func(x: Any, *args, strict: bool, keys: List[str]) -> Any:
    pass
```
That is, the function should expect the value to validate as the first positional parameter, followed by any extra parameters you may define in the type dict, with two required keyword parameters, `strict` (which will tell your function if the validation should be strict) and `keys` (which will tell your function where the value sits in the .json document).

To keep things easily organised, you should probably define such functions as methods on child of the Colchian class. For example:
```python
from typing import List
from colchian import Colchian

class MyColchian(Colchian):
    @staticmethod
    def fizzbuzz(xs: List[int], fizz: str, buzz: str, strict: bool, keys: List[str]):
        return [fizz*(i % 3 == 0)+buzz*(i % 5 == 0) or i for i in xs]

data = {
    'xs': range(15)
}

type_dict = {
    'xs': (MyColchian.fizzbuzz, 'fizz', 'buzz')
}

print(MyColchian.validated(data, type_dict))
```

You can pass extra parameters to your functions like this:
```python
type_dict = {
    'xs': (MyColchian.dt_str, '%Y-%m-%d %H:%M')
}
```
The validation will interpret the rest of the tuple as positional parameters after the value, instead of type options.

Note: this means that you can't pass two functions as the only options for a type:
```python
# causes problems:
type_dict = {
    'xs': (MyColchian.method1, MyColchian.method2)
}
```
This will cause values for key `'xs'` to be validated by calling `MyColchian.method1(value, MyColchian.method2, strict, keys)`, instead of trying each function separately as you might expect. If you need this functionality, you can instead do this:
```python
# no problem:
type_dict = {
    'xs': ((MyColchian.method1,), (MyColchian.method2,))
}
```
Similarly, if you want to validate an optional value against a function or method, you should use `(None, function_name)` instead of `(function_name, None)`, as that would result in a call to `function_name(value, None, strict, keys)`.

An additional example is available in [typed_configuration.py](example/typed_configuration.py). Try that code and experiment with breaking [example_configuration.json](example/example_configuration.json) in interesting ways.

### Wildcards

If you define wildcards in a type dictionary, elements that don't match required keys will be matched against them. If there are multiple wildcards, Colchian will try them all. For example:
```python
type_dict = {
    '*:1': {
        'type': 'car',
        'wheels': 4,
        'engine': float,
        'electric': typing.Optional[bool]
    },
    '*:2': {
        'type': 'bicycle',
        'wheels': 2,
        'electric': bool
    }
}
```
Makes this `vehicles.json` a valid file:
```json
{
  "Peugeot 208": {
    "type": "car",
    "wheels": 4,
    "engine": 1.4,
    "electric": false
  },
  "Batavus Socorro": {
    "type": "bicycle",
    "wheels": 2,
    "electric": false
  },
  "T-Ford": {
    "type": "car",
    "wheels": 4,
    "engine": 2.9
  }
}
```
Note that you can't use the key `'*'` twice, which is why the wildcards are distinguished as `'*:1'` and `'*:2'`.
