# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bavard_ml_common',
 'bavard_ml_common.ml',
 'bavard_ml_common.mlops',
 'bavard_ml_common.types',
 'bavard_ml_common.types.conversations']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0',
 'google-cloud-error-reporting>=1.1.1,<2.0.0',
 'google-cloud-pubsub>=2.2.0,<3.0.0',
 'google-cloud-storage>=1.35.1,<2.0.0',
 'loguru>=0.5.1,<0.6.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.21.0,<3.0.0']

extras_require = \
{'ml': ['numpy>=1.15.4,<2.0.0', 'scikit-learn>=0.24.2,<0.25.0']}

setup_kwargs = {
    'name': 'bavard-ml-common',
    'version': '0.1.17',
    'description': 'Machine learning and Python web service utilities',
    'long_description': None,
    'author': 'Bavard AI, Inc.',
    'author_email': 'dev@bavard.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
