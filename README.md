# Python Lame binding

## Usage

```python
from lame_ctypes import *

lame = lame_init()

lame_close(lame, 1)
```

See [sample](./sapmles/decodemp3.py)

## Important limitation

Currently, only decoding bindings are defined.

## How to execute a sample

```console
poetry install
PYTHONPATH=. poetry run python3 samples/decodemp3.py your-mp3-file.mp3 output.wav
```
