# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'jsonsimpleconfig'}

packages = \
['jsccommon',
 'jscdata',
 'jscextractor',
 'jschelper',
 'jscparser',
 'jsonsimpleconfig',
 'jsonsimpleconfig.jsccommon',
 'jsonsimpleconfig.jscdata',
 'jsonsimpleconfig.jscextractor',
 'jsonsimpleconfig.jschelper',
 'jsonsimpleconfig.jscparser']

package_data = \
{'': ['*'], 'jsonsimpleconfig': ['jscresources/*']}

modules = \
['requirements', 'poetry']
entry_points = \
{'console_scripts': ['jsc2json = jsonsimpleconfig.jsc2json:main',
                     'jscPrint = jsonsimpleconfig.jsc_print:main',
                     'jscValue = jsonsimpleconfig.jsc_value:main',
                     'jsc_print = jsonsimpleconfig.jsc_print:main',
                     'jsc_value = jsonsimpleconfig.jsc_value:main',
                     'json2csv = jsonsimpleconfig.json2csv:main',
                     'json2jsc = jsonsimpleconfig.json2jsc:main']}

setup_kwargs = {
    'name': 'jsonsimpleconfig',
    'version': '0.6',
    'description': 'The simple idea to prepare configuration for your application.',
    'long_description': None,
    'author': 'Marcin Zelek',
    'author_email': 'marcin.zelek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xmzxmz/jsonsimpleconfig',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
