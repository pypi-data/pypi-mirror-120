# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nametract']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nametract',
    'version': '1.1.0',
    'description': 'Simple and stupid name extraction',
    'long_description': '# nametract\n\n[![PyPI version](https://badge.fury.io/py/nametract.svg)](https://badge.fury.io/py/nametract)\n\nSimple python package to extract everything that looks like a name from the text. Extremely unreliable. Might work for\nyou if you don\'t care about possible errors. Currently in development.\n\n```python\nfrom nametract import extract\n\nextract("My name is Peter, and I love Nancy Brown")  # ["Peter", "I", "Nancy Brown"]\nextract("My name is Peter, and I love Nancy Brown", minimal_name_size=2)  # ["Peter", "Nancy Brown"]\nextract("My name is Peter, and I love Nancy Brown", ignore_sentence_start=False)  # ["My", "Peter", "I", "Nancy Brown"]\nextract("С коня сошел Иван Зайцев-Кабачков")  # ["Иван Зайцев-Кабачков"]\n```\n',
    'author': 'keddad',
    'author_email': 'keddad@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/keddad/nametract',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
