# nametract

Simple python package to extract everything that looks like a name from the text. Extremely unreliable. Might work for
you if you don't care about possible errors. Currently in development.

```python
from nametract import extract

extract("My name is Peter, and I love Nancy Brown")  # "Peter", "I", "Nancy Brown"
```
