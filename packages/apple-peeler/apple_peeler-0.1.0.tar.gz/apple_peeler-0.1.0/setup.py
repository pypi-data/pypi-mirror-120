# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apple_peeler']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0', 'click>=8.0.1,<9.0.0', 'lxml>=4.6.3,<5.0.0']

entry_points = \
{'console_scripts': ['apple-peeler = apple_peeler.extract:main']}

setup_kwargs = {
    'name': 'apple-peeler',
    'version': '0.1.0',
    'description': 'Extract XML from the OS X dictionaries.',
    'long_description': 'This is inspired by\nhttps://fmentzer.github.io/posts/2020/dictionary/\nAnd the discussion on Hacker News\nhttps://news.ycombinator.com/item?id=28505406\nhttps://josephg.com/blog/reverse-engineering-apple-dictionaries/\nhttps://josephg.com/blog/apple-dictionaries-part-2/\n',
    'author': 'Joshua Olson',
    'author_email': 'joshua+github@solarmist.net',
    'maintainer': 'Joshua Olson',
    'maintainer_email': 'joshua+github@solarmist.net',
    'url': 'https://github.com/solarmist/apple-peeler',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
