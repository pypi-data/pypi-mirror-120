# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mdal', 'mdal.statics', 'mdal.time_series']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'pmdarima>=1.8.2,<2.0.0',
 'scikit-posthocs>=0.6.7,<0.7.0',
 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'mdal',
    'version': '0.1.5',
    'description': 'mdal(My Data Analytics Library)',
    'long_description': None,
    'author': 'Yuya Nagai',
    'author_email': 'ynny.opem@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ynny-github/mdal',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
