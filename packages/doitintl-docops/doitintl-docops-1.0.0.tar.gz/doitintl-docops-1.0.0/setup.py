# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['doitintl',
 'doitintl.docops',
 'doitintl.docops.gitbook',
 'doitintl.docops.gitbook.cli',
 'doitintl.docops.gloss',
 'doitintl.docops.gloss.analyzers',
 'doitintl.docops.gloss.cli']

package_data = \
{'': ['*']}

install_requires = \
['api-client>=1.3.1,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'charset-normalizer>=2.0.4,<3.0.0',
 'docopt>=0.6.2,<0.7.0',
 'inflect>=5.3.0,<6.0.0',
 'inflection>=0.5.1,<0.6.0',
 'nltk>=3.6.2,<4.0.0',
 'pastel>=0.2.1,<0.3.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['docops-gitbook = doitintl.docops.gitbook.cli:run',
                     'docops-gloss-terms = '
                     'doitintl.docops.gloss.cli.terms:run']}

setup_kwargs = {
    'name': 'doitintl-docops',
    'version': '1.0.0',
    'description': 'Python library and CLI tools for doing DocOps at DoiT',
    'long_description': '# DoiT DocOps Python Package\n\n_Python library and CLI tools for doing DocOps at DoiT_\n\n**Table of contents:**\n\n- [Install](#install)\n- [Documentation](#documentation)\n  - [Users](#users)\n  - [Developers](#developers)\n\n## Install\n\nYou can install the [doit-docops][pypi-project] package using [Pip][pip]:\n\n```console\n$ pip install doit-docops\nCollecting doit-docops\n  Downloading doit_docops-0.0.0-py3-none-any.whl (175 kB)\n[...]\nSuccessfully installed doit-docops-0.0.0\n```\n\nThe [project releases][releases] page has a complete list of all releases and\nthe corresponding release notes. If you prefer to install the package manually,\neach release page has links to multiple release assets.\n\n## Documentation\n\n> 📝 **Note**\n>\n> Documentation is sparse at the moment because this project is still in the\n> early stages of development.\n\n### Users\n\n- [Glossary utilities][user-gloss]\n- [GitBook client][user-gitbook]\n\n### Developers\n\n- [Python development][dev-python]\n\n<!-- Link references go below this line, sorted ascending --->\n\n[dev-python]: https://github.com/doitintl/docops-python/blob/main/docs/dev/python.md\n[pip]: https://pip.pypa.io/en/stable/\n[pypi-project]: https://pypi.org/project/ddoit-docops\n[releases]: https://github.com/doitintl/docops-python/releases\n[user-gitbook]: https://github.com/doitintl/docops-python/blob/main/docs/user/gitbook.md\n[user-gloss]: https://github.com/doitintl/docops-python/blob/main/docs/user/gloss.md\n',
    'author': 'DoiT International',
    'author_email': 'engineering@doit-intl.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/doitintl/docops',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
