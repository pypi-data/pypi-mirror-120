# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rsserpent',
 'rsserpent.models',
 'rsserpent.plugins',
 'rsserpent.plugins.builtin',
 'rsserpent.utils']

package_data = \
{'': ['*'], 'rsserpent': ['templates/*']}

install_requires = \
['arrow>=1.1.1,<2.0.0',
 'importlib-metadata>=4.5.0,<5.0.0',
 'pydantic[email]>=1.8.2,<2.0.0',
 'starlette[full]>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'rsserpent',
    'version': '0.1.4a1',
    'description': '🐍 This snake helps you reconnect the Web, with RSS feeds!',
    'long_description': '<p align="center">\n<img alt="RSSerpent" src="https://i.loli.net/2021/07/31/14nQw2XRFCPuLDN.png" width="250" />\n</p>\n\n[![python: 3.6.2+](https://img.shields.io/badge/python->=3.6.2-blue.svg)](https://www.python.org/downloads/)\n[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![mypy: checked](https://img.shields.io/badge/mypy-checked-blue.svg)](https://github.com/python/mypy)\n\n[![pypi: version](https://img.shields.io/pypi/v/rsserpent)](https://pypi.org/project/rsserpent/)\n[![pypi downloads: per month](https://img.shields.io/pypi/dm/rsserpent)](https://pypi.org/project/rsserpent/)\n[![docker: version](https://img.shields.io/docker/v/queensferry/rsserpent/latest?label=docker&sort=semver)](https://hub.docker.com/r/queensferry/rsserpent)\n[![docker: image size](https://img.shields.io/docker/image-size/queensferry/rsserpent/latest)](https://hub.docker.com/r/queensferry/rsserpent)\n\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/RSSerpent/RSSerpent/master.svg)](https://results.pre-commit.ci/latest/github/RSSerpent/RSSerpent/master)\n[![github test status](https://img.shields.io/github/workflow/status/RSSerpent/RSSerpent/Test?label=test&logo=github&message=passed)](https://github.com/RSSerpent/RSSerpent/actions/workflows/test.yaml)\n[![codecov status](https://codecov.io/gh/RSSerpent/RSSerpent/branch/master/graph/badge.svg?token=FQZ5OWOQRO)](https://codecov.io/gh/RSSerpent/RSSerpent)\n[![github docker status](https://img.shields.io/github/workflow/status/RSSerpent/RSSerpent/Build%20Docker%20Image?label=docker&logo=docker)](https://github.com/RSSerpent/RSSerpent/actions/workflows/docker.yaml)\n\n[![chat on telegram](https://img.shields.io/badge/chat%20on-telegram-blue.svg)](https://t.me/rsserpent)\n\nThis snake helps you reconnect the Web, with RSS feeds!\n\nRSSerpent is an open-source software that create [RSS](https://en.wikipedia.org/wiki/RSS) feeds for websites that do not provide any.\n\n[English](https://github.com/RSSerpent/RSSerpent/blob/master/README.md) | [中文](https://github.com/RSSerpent/RSSerpent/blob/master/README.zh.md)\n\n# Quick Start\n\n- Official Instance: <https://www.rsserpent.com/>\n- Documentation: <https://docs.rsserpent.com/>\n\n# Thanks\nThe RSSerpent Project is heavily inspired by [RSSHub](https://github.com/DIYgod/RSSHub) 🎉 We pay the highest possible tribute to RSSHub & its maintainers.\n\n## Sponsors\n\n<a href="https://linktr.ee/rss3" target="_blank"><img alt="rss3" src="https://rss3.io/assets/images/Logo.svg" width="200" /></a>\n\n# People\n\nThe RSSerpent Project is created by [@queensferry](https://github.com/queensferryme/), supported by various [project members](https://github.com/orgs/RSSerpent/people) & [contributors](https://github.com/RSSerpent/RSSerpent/graphs/contributors).\n\n[![contributors](https://opencollective.com/RSSerpent/contributors.svg?avatarHeight=50)](https://github.com/RSSerpent/RSSerpent/graphs/contributors)\n',
    'author': 'Queensferry',
    'author_email': 'queensferry.me@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RSSerpent/RSSerpent',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
