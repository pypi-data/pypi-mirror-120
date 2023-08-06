# nametract

[![PyPI version](https://badge.fury.io/py/nametract.svg)](https://badge.fury.io/py/nametract)

Simple python package to extract everything that looks like a name from the text. Extremely unreliable. Might work for
you if you don't care about possible errors. Currently in development.

```python
from nametract import extract

extract("My name is Peter, and I love Nancy Brown")  # ["Peter", "I", "Nancy Brown"]
extract("My name is Peter, and I love Nancy Brown", minimal_name_size=2)  # ["Peter", "Nancy Brown"]
extract("My name is Peter, and I love Nancy Brown", ignore_sentence_start=False)  # ["My", "Peter", "I", "Nancy Brown"]
extract("С коня сошел Иван Зайцев-Кабачков")  # ["Иван Зайцев-Кабачков"]
```
