# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nayose']

package_data = \
{'': ['*'], 'nayose': ['data/*']}

install_requires = \
['feather-format>=0.4.0,<0.5.0', 'pandas>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'nayose',
    'version': '0.1.6',
    'description': '',
    'long_description': '\nnayose is a Python module for data cleansing for Japanese address and is distributed under the MIT license.\n\nInstallation\n============\n\nYou can install the latest this module with the command:\n\n    pip install nayose\n\nQuick start\n============\n\nnayose has two main function of data cleansing for Japanese address.\n\n`complete_address` is a function to complete dirty address. For example, the followings is a case of missing state(都道府県).\n\n    from nayose import complete_address\n\n    complete_address("千代田区大手町1−1−1大手町あいうえビル")\n    > "東京都千代田区大手町1−1−1大手町あいうえビル"\n\n\n`split_address` is a function to split complete address to state(都道府県), city(市区郡) and street(その他).\n\n    from nayose import split_address\n\n    split_address("東京都千代田区大手町1−1−1大手町あいうえビル")\n    > (\'東京都\', \'千代田区\', \'大手町1−1−1大手町あいうえビル\')\n\n\nImportant links\n============\n\nOfficial source code repo: https://github.com/sonesuke/nayose\nDownload releases: https://pypi.org/project/nayose/\nIssue tracker: https://github.com/sonesuke/nayose/issues\n\nCitation\n============\n\nIf you use nayose in a publication, we would appreciate citations: https://github.com/sonesuke/nayose\n\n\nFor contributors\n============\n\nYou can contribute it quickly by using docker image with the command.\n\n    git clone https://github.com/sonesuke/nayose.git\n    docker-compose run nayose bash\n\n\nFor test.\n\n    bash scripts/test\n\n\nIf you add any modules, please re-build docker image after \'poetry update\' .\n\n\n\n',
    'author': 'sonesuke',
    'author_email': 'iamsonesuke@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sonesuke/nayose',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.10,<4.0.0',
}


setup(**setup_kwargs)
