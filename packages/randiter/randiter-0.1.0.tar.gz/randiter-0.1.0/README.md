# randiter

`randiter` randomly iterates a sequence with buffered shuffling.
`randiter` is suitable for shuffling very long sequences and sequences with an unknown length.

## Usage

Shuffle a very long sequence:

```python
from randiter import randiter

for index in randiter(range(1_000_000_000)):
    print(index)  # random number
```

Shuffle lines in a text file with an unknown length:

```python
from randiter import randiter

with open("large.txt", "rt") as f:
    for line in randiter(f):
        print(line)  # random line
```

Shuffle a sequence with a large buffer size (to perform perfect shuffling, specify a buffer size that is equal to or greater than the length of the given sequence):

```python
from randiter import randiter

for index in randiter(range(1_000_000_000), buffer_size=1_000_000):
    print(index)  # random number
```

## FAQ

- Q. Shuffled sequences are not completely shuffled.
  - A. This is because `randiter` performs *buffered* shuffling. This problem can be mitigated by specifying a larger buffer size.
