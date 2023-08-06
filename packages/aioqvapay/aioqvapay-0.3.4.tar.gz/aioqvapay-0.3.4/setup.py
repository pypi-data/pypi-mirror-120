# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioqvapay',
 'aioqvapay.v1',
 'aioqvapay.v1.models',
 'aioqvapay.v2',
 'aioqvapay.v2.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx[brotli]>=0.19.0,<0.20.0', 'pydantic[dotenv]>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'aioqvapay',
    'version': '0.3.4',
    'description': 'Asynchronous and also synchronous non-official QvaPay client for asyncio and Python language.',
    'long_description': '# QvaPay client for Python (Deprecated!!!)\n\n![QvaPay client for Python Banner](https://raw.githubusercontent.com/leynier/aioqvapay/main/banner.png)\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT) [![Test](https://github.com/leynier/aioqvapay/workflows/CI/badge.svg)](https://github.com/leynier/aioqvapay/actions?query=workflow%3ACI) [![codecov](https://codecov.io/gh/leynier/aioqvapay/branch/main/graph/badge.svg?token=Z1MEEL3EAB)](https://codecov.io/gh/leynier/aioqvapay) [![DeepSource](https://deepsource.io/gh/leynier/aioqvapay.svg/?label=active+issues)](https://deepsource.io/gh/leynier/aioqvapay/?ref=repository-badge) [![DeepSource](https://deepsource.io/gh/leynier/aioqvapay.svg/?label=resolved+issues&show_trend=true&token=4v2I_h38kqwuuBKg1qGyupG1)](https://deepsource.io/gh/leynier/aioqvapay/?ref=repository-badge) [![Version](https://img.shields.io/pypi/v/aioqvapay?color=%2334D058&label=Version)](https://pypi.org/project/aioqvapay) [![Last commit](https://img.shields.io/github/last-commit/leynier/aioqvapay.svg?style=flat)](https://github.com/leynier/aioqvapay/commits) [![GitHub commit activity](https://img.shields.io/github/commit-activity/m/leynier/aioqvapay)](https://github.com/leynier/aioqvapay/commits) [![Github Stars](https://img.shields.io/github/stars/leynier/aioqvapay?style=flat&logo=github)](https://github.com/leynier/aioqvapay/stargazers) [![Github Forks](https://img.shields.io/github/forks/leynier/aioqvapay?style=flat&logo=github)](https://github.com/leynier/aioqvapay/network/members) [![Github Watchers](https://img.shields.io/github/watchers/leynier/aioqvapay?style=flat&logo=github)](https://github.com/leynier/aioqvapay) [![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fleynier.github.io/aioqvapay)](https://leynier.github.io/aioqvapay) [![GitHub contributors](https://img.shields.io/github/contributors/leynier/aioqvapay?label=code%20contributors)](https://github.com/leynier/aioqvapay/graphs/contributors) <!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)<!-- ALL-CONTRIBUTORS-BADGE:END -->\n\n## IMPORTANT: Deprecated, we recommend using https://pypi.org/project/qvapay\n\n[Asynchronous](https://docs.python.org/3/library/asyncio-task.html) and also synchronous **non-official** [QvaPay](https://qvapay.com) client for [asyncio](https://docs.python.org/3/library/asyncio.html) and [Python language](https://www.python.org). This library is still under development, the interface could be changed.\n\n## Features\n\n* Response models with type hints annotated fully (Also internal code have type hints annotated fully) thank you to  Python\'s type hints (or annotations) and [pydantic](https://pydantic-docs.helpmanual.io)\n* Asynchronous and synchronous behavior thank you to [httpx](https://www.python-httpx.org)\n* Coverage 100%\n* Project collaborative and open source\n\n## Alternatives\n\n* <https://pypi.org/project/qvapay>\n\nFor more information about **QvaPay API**, read the [QvaPay docs](https://qvapay.com/docs).\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="http://leynier.github.io"><img src="https://avatars.githubusercontent.com/u/36774373?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Leynier Gutiérrez González</b></sub></a><br /><a href="https://github.com/leynier/aioqvapay/commits?author=leynier" title="Code">💻</a> <a href="#maintenance-leynier" title="Maintenance">🚧</a> <a href="https://github.com/leynier/aioqvapay/commits?author=leynier" title="Tests">⚠️</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\nThis project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!\n',
    'author': 'Leynier Gutiérrez González',
    'author_email': 'leynier41@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://leynier.github.io/aioqvapay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.14,<4.0.0',
}


setup(**setup_kwargs)
