# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dwnld', 'libdwnld']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.7.2,<3.0.0',
 'plumbum>=1.7.0,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'scp>=0.13.6,<0.14.0']

setup_kwargs = {
    'name': 'dwnld',
    'version': '0.1.0',
    'description': 'A multiprotocol downloader',
    'long_description': '# dwnld\n\n![dwnld.png](https://raw.githubusercontent.com/4thel00z/logos/master/dwnld.png)\n\n## Motivation\n\nA library to download stuff given urls with different protocols, like `ftp://...` or `ssh://...`.\n\n## Usage\n\nThere is only one interesting module level function in this repo, it can download (or move) stuff from A to B:\n\n```python\nfrom dwnld import download\n\ndownload("file://stuff.txt", "somewhere_else.txt")\ndownload("ssh://some-remote-server:/home/reptile/stuff.txt", "here.txt")\ndownload("https://cool.com/nice.pdf", "here.pdf")\ndownload("http://cool.com/nice.pdf", "here.pdf")\n```\n\n## Todos\n\n- Support ftp/sftp\n- Support torrent\n\n## License\n\nThis project is licensed under the GPL-3 license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4thel00z/dwnld',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
