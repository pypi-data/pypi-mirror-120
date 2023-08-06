# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcade_imgui']

package_data = \
{'': ['*']}

install_requires = \
['arcade>=2.6.2,<3.0.0', 'imgui>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'arcade-imgui',
    'version': '0.2.0',
    'description': 'IMGUI integration for arcade',
    'long_description': '# Arcade ImGui\n\n[The Python Arcade Library](https://arcade.academy/) + [pyimgui](https://github.com/swistakm/pyimgui) = :heart:\n\n:package: [Package](https://pypi.org/project/arcade-imgui/)\n\n## Prerequisite\n\nGet [Poetry](https://python-poetry.org/)\n\n## Clone\n\nClone the repository and change directory\n\n       git clone https://github.com/kfields/arcade-imgui.git\n       cd arcade-imgui\n       poetry shell\n\n## Run the Demo\n\n        cd imdemo\n        poetry install\n        python imdemo\n\n## Run the ImFlo Demo\n\n        cd imflo\n        poetry install\n        python imflo\n',
    'author': 'Kurtis Fields',
    'author_email': 'kurtisfields@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kfields/arcade-imgui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
