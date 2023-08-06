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
    'version': '0.1.1',
    'description': 'Extract XML from the OS X dictionaries.',
    'long_description': '# Before You Start\n\nApple-peeler was written using python 3.9 (but it should be trivial to support earlier versions of python 3.5+).\n\n# Installation\n\n    pip install apple-peeler\n\n# Dependencies\n\n[BeautifulSoup 4](https://beautiful-soup-4.readthedocs.io/en/latest/), [lxml](https://lxml.de), and [click](https://click.palletsprojects.com/en/8.0.x/)\n\n# Usage\n\nApple likes to move around the dictionaries location from macOS version to macOS version. So if the dictionaries are no longer at the path below you can tell `apple-peeler` where to look by exporting `DICT_BASE` in your environment or using the `--base` option below.\n\n    export DICT_BASE="/System/Library/AssetsV2/com_apple_MobileAsset_DictionaryServices_dictionaryOSX/"\n\nAfter that, useage is straightforward.\n\n    Usage: apple-peeler [OPTIONS]\n\n    Extract XML from Apple Dictionary files.\n\n    Options:\n    --base DIRECTORY                The root directory of the OS X dictionaries.\n                                    (Default: /System/Library/AssetsV2/com_apple\n                                    _MobileAsset_DictionaryServices_dictionaryOS\n                                    X/) [Env var DICT_BASE]\n    --out DIRECTORY                 The path to place extracted XML files.\n    -d, --dictionary [\n        all|Arabic - English|Danish|Duden Dictionary Data Set I|Dutch|\n        Dutch - English|French|French - English|French - German|German - English|\n        Hebrew|Hindi|Hindi - English|Indonesian - English|Italian|\n        Italian - English|Korean|Korean - English|New Oxford American Dictionary|\n        Norwegian|Oxford American Writer\'s Thesaurus|\n        Oxford Dictionary of English|Oxford Thesaurus of English|\n        Polish - English|Portuguese|Portuguese - English|Russian|\n        Russian - English|Sanseido Super Daijirin|\n        Sanseido The WISDOM English-Japanese Japanese-English Dictionary|\n        Simplified Chinese - English|Simplified Chinese - Japanese|Spanish|\n        Spanish - English|Swedish|Thai|Thai - English|\n        The Standard Dictionary of Contemporary Chinese|Traditional Chinese|\n        Traditional Chinese - English|Turkish|Vietnamese - English]\n                                    The dictionary to extract or \'all\'.\n                                    (Default: all) [Accepts multiple]\n    --format-xml / --no-format-xml  Format the XML files using BeautifulSoup.\n                                    (Default: False)\n    --debug                         Output debug information to STDERR.\n                                    (Default: False)\n    --help                          Show this message and exit.\n\n## Introduction\n\nI need a ton of dictionary data for prototyping my learning a language tool, [Parsnip](https://solarmist.net/), and licensing 40 dictionaries seems too expensive for a bootstrapper working on an MVP (I look forward to the day this is no longer true).\n\nParsnip uses Natural Language Processing and Dictionaries to decouple the word <-> sentence tug-of-war that\'s existed as long as flashcards have been used for language learning. I.e., should I make a word (concept) or a sentence (example) flashcard?\n\nI care about what words I know for tracking purposes, but I want those words in context when I\'m practicing. So the learning system breaks down sentences into lemmas (or dictionary form of a word) and a database of example sentences that the words appear in. This resolves the conceptual tug-of-war for flashcards.\n\nBut by removing reference data from the flashcards themselves, I need to integrate reference material directly into Parsnip\'s UI. [JMDict](https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project) is a great open source project for this, but that only covers a single language. So, I\'ve been keeping my eyes open for people working on extracting the data from Apple\'s bundled dictionaries.\n\nThis has been a community effort that\'s spanned several years. My contribution is to collect the results, clear up some details about the file format, and package it into a general command-line tool.\n\n## References\n\nThis is inspired by\n[Reverse-Engineering Apple Dictionary](https://fmentzer.github.io/posts/2020/dictionary/).\nAnd the discussion on Hacker News\n[Hacker News: Reverse-Engineering Apple Dictionary (2020)](https://news.ycombinator.com/item?id=28505406). Special thanks to tim-- and enragedcacti who introduced me to `binwalk`. And dunham who mentioned the random bytes looking like `int`s of payload sizes.\n\nAdditionally, I\'ve found these posts informative:\n\n- https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/DictionaryServicesProgGuide/prepare/prepare.html#//apple_ref/doc/uid/TP40006152-CH3-SW7\n- https://jadedtuna.github.io/apple-dictionary/\n- https://josephg.com/blog/reverse-engineering-apple-dictionaries/\n- https://josephg.com/blog/apple-dictionaries-part-2/\n- https://gist.github.com/josephg/5e134adf70760ee7e49d\n',
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
