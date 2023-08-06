# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['richerr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'richerr',
    'version': '0.1.1',
    'description': 'Rich errors (sort of)',
    'long_description': '# Welcome\n\n## RichErr\n\nRichErr is a tiny module that gives you basic error class, which can be used in JSON, dict, list, and other mutation\n\n```python example.py\nfrom richerr import RichErr\n\nprint(RichErr.convert(ValueError(\'Hello world!\')).json(indent=2))\n```\n\n```json5\n{\n  "error": {\n    "code": 400,\n    "exception": "BadRequestException",\n    "message": "Hello world!",\n    "caused_by": {\n      "error": {\n        "code": 500,\n        "exception": "ValueErrorException",\n        "message": "Hello world!",\n        "caused_by": null\n      }\n    }\n  }\n}\n```\n\n## Installation\n\n### Poetry\n\n```shell\npoetry add RichErr\n```\n\n### PIP\n\n```shell\npip install RichErr\n```\n\n## Requirements\n\n- [x] Python 3.10+\n- [x] No package dependencies\n\n## Plugins\n\n- [x] Supported Django Validation and ObjectNotFound errors\n- [x] Supported DRF Validation errors\n- [x] Supported Pydantic Validation errors\n\n### Want to add your own error conversion?\n\nAdd direct conversion\n\n```python\nfrom richerr import RichErr, GatewayTimeout\n\n\nclass MyTimeoutError(IOError): ...\n\n\nRichErr.add_conversion(MyTimeoutError, GatewayTimeout)\n```\n\nOr add conversion method\n\n```python\nfrom richerr import RichErr\n\n\nclass MyTimeoutError(IOError): ...\n\n\ndef _convert(err: MyTimeoutError):\n    return RichErr.from_error(err, message=\'Something happened\', code=500, name=\'MyTimeoutError\')\n\n\nRichErr.add_conversion(MyTimeoutError, _convert)\n```\n\n!!!\nSubclasses will be checked before their parent, if multiple classes in same MRO will be registered.\n!!!',
    'author': 'Bogdan Parfenov',
    'author_email': 'adam.brian.bright@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://adambrianbright.github.io/python-richerr/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10.0rc2,<4.0',
}


setup(**setup_kwargs)
