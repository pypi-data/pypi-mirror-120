# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kitsu']

package_data = \
{'': ['*']}

modules = \
['LICENSE']
install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'kitsu.py',
    'version': '0.1.1',
    'description': 'A simple async python wrapper for the kitsu.io API.',
    'long_description': '# Kitsu.py\n[![PyPI](https://badge.fury.io/py/kitsu.py.svg)](https://pypi.org/project/kitsu.py)\n\nA simple async python wrapper for the [Kitsu.io](https://kitsu.io) API.\n\n## Key Features\n* Simple and modern Pythonic API using `async/await`\n* Fully type checked\n\n## Requirements\n\nPython 3.8+\n* [aiohttp](https://pypi.org/project/aiohttp/)\n* [python-dateutil](https://pypi.org/project/aiohttp/)\n\n## Installing\nTo install the library, run the following commands:\n```shell\n# Linux/MacOS\npython3 -m pip install -U kitsu.py\n\n# Windows\npy -3 -m pip install -U kitsu.py\n```\n\n## Getting started\n\nSearch for an anime:\n```python\nimport kitsu\nimport asyncio\n\nclient = kitsu.Client()\n\nasync def main():\n    data = await client.search_anime("jujutsu kaisen", limit=1)\n    \n    print("Canonical Title: " + data.canonical_title)\n    print("Average Rating: " + str(data.average_rating))\n    \n    # Close the internal aiohttp ClientSession\n    await client.close()\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\n```\nThis prints:\n```\nCanonical Title: Jujutsu Kaisen\nAverage Rating: 85.98\n```\nYou can find more examples in the [examples](https://github.com/MrArkon/kitsu.py/tree/master/examples/) directory.\n\n## License\n\nThis project is distributed under the [MIT](https://github.com/MrArkon/kitsu.py/blob/master/LICENSE.txt) license.\n',
    'author': 'MrArkon',
    'author_email': 'mrarkon@outlook.com',
    'maintainer': 'MrArkon',
    'maintainer_email': 'mrarkon@outlook.com',
    'url': 'https://github.com/MrArkon/kitsu.py/',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
