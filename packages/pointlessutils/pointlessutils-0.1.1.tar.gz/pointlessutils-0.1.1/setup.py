# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pointlessutils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pointlessutils',
    'version': '0.1.1',
    'description': 'Pointless utilities for python.',
    'long_description': '# Pointless Utils\n\nA collection of utilities that are (probably) pointless.\n\n## Decorators\n\nThere are currently 5 pointless decorators available to use:\n\n- `@none` - Causes the function to always return `None`\n- `@true` - Causes the function to always return `True`\n- `@false` - Causes the function to always return `False`\n- `@maybe` - Causes the function to return a random choice of `True` or `False`\n- `@never` - The function will never return and will block indefinitely\n\nThese decorators can be used on either normal or async functions. For example:\n\n```py\n@maybe\ndef ex_1():\n    pass\n\n@maybe\nasync def ex_2():\n    pass\n```\n',
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vcokltfre/pointlessutils',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
