# PyOOPy :poop:
**P**ython **O**bject-**O**riented **P**rogramming library

## Installation
```pip install PyOOPy```

## Usage

```python
from dataclasses import dataclass
from PyOOPy import PyOOPy


@dataclass
class Base(PyOOPy):
    protected_field: PyOOPy.Protected = None
    private_field: PyOOPy.Private = None
    public_field: PyOOPy.Public = None

    @PyOOPy.protected
    def protected_method(self):
        pass

    @PyOOPy.private
    def private_method(self):
        pass

    @PyOOPy.public
    def public_method(self):
        pass
```

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
