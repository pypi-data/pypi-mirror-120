# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scilib',
 'scilib.antv',
 'scilib.cnki',
 'scilib.db',
 'scilib.gender',
 'scilib.gender.agefromname_pypi',
 'scilib.gender.api',
 'scilib.gender.api_gender',
 'scilib.gender.api_genderize',
 'scilib.gender.api_namsor',
 'scilib.gender.benchmark',
 'scilib.gender.chinese_naive_bayes',
 'scilib.gender.gender_computer',
 'scilib.gender.gender_detector',
 'scilib.gender.gender_guesser_pypi',
 'scilib.gender.gender_predictor',
 'scilib.gender.gender_r',
 'scilib.gender.genderizer_pypi',
 'scilib.gender.go_gender',
 'scilib.gender.imdb_wiki_dataset',
 'scilib.gender.tools',
 'scilib.iolib',
 'scilib.scripts',
 'scilib.stata',
 'scilib.tests',
 'scilib.tests.test_wos',
 'scilib.wos']

package_data = \
{'': ['*'],
 'scilib.tests.test_wos': ['fixtures/*'],
 'scilib.wos': ['configs/*']}

install_requires = \
['Unidecode>=1.2.0,<2.0.0',
 'agefromname>=0.0.8,<0.0.9',
 'aiohttp>=3.7.4,<4.0.0',
 'gender-guesser==0.4.0',
 'genderizer>=0.1.2,<0.2.0',
 'jupyter>=1.0.0,<2.0.0',
 'jupyterlab>=3.0.16,<4.0.0',
 'libs>=0.0.10,<0.0.11',
 'matplotlib>=3.2.1,<4.0.0',
 'naiveBayesClassifier>=0.1.3,<0.2.0',
 'nameparser>=1.0.6,<2.0.0',
 'nltk>=3.5,<4.0',
 'numpy>=1.18.2,<2.0.0',
 'openpyxl>=3.0.3,<4.0.0',
 'orjson>=3.2.1,<4.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pypinyin>=0.38.1,<0.39.0',
 'pyquery>=1.4.3,<2.0.0',
 'redis>=3.5.3,<4.0.0',
 'requests>=2.23.0,<3.0.0',
 'scipy>=1.4.1,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'xlrd>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['scilib-cnki-import = scilib.scripts.cnki_import:run',
                     'scilib-db-trans = scilib.scripts.db_trans:run',
                     'scilib-gender-benchmark = '
                     'scilib.gender.benchmark.benchmark:run',
                     'scilib-wos-import = scilib.scripts.wos_import:run']}

setup_kwargs = {
    'name': 'scilib',
    'version': '0.0.14',
    'description': 'scilib',
    'long_description': '\n# scilib\n\n[![Github](https://github.com/phyng/scilib/workflows/test/badge.svg)](https://github.com/phyng/scilib/actions) [![Pypi](https://img.shields.io/pypi/v/scilib.svg?style=flat&label=PyPI)](https://pypi.org/project/scilib/)\n\n## documentation\n\nhttps://phyng.com/scilib/\n\n## install\n\n```bash\n# use pip\npip install scilib\n\n# or use poetry\npoetry add scilib\n```\n\n## usage\n\n### import wos data to ElasticSearch\n\n```bash\nenv ES_API=http://localhost:9205 scilib-wos-import --from /path/to/wos_data/ --to es --index wos\n```\n\n## test\n\n```bash\nnpm test\nnpm test_coverage\n```\n',
    'author': 'phyng',
    'author_email': 'phyngk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/phyng/scilib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
