# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_workspace',
 'poetry_workspace.commands',
 'poetry_workspace.commands.workspace',
 'poetry_workspace.vcs']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['poetry-workspace-plugin = '
                               'poetry_workspace.plugin:WorkspacePlugin']}

setup_kwargs = {
    'name': 'poetry-workspace-plugin',
    'version': '0.3.0',
    'description': 'Multi project workspace plugin for Poetry',
    'long_description': '',
    'author': 'Martin Liu',
    'author_email': 'martin.xs.liu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
