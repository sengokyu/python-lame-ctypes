# Python Lame binding

## Usage

```python
from lame_ctypes import *

lame = lame_init()

lame_close(lame, 1)
```

See [sample](https://github.com/sengokyu/python-lame-ctypes/blob/main/samples/)

## Important limitation

Currently, only decoding bindings are defined.
