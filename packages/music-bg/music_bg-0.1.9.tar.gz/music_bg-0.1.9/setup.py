# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['music_bg', 'music_bg.dbus', 'music_bg.img_processors']

package_data = \
{'': ['*']}

install_requires = \
['Pillow-SIMD>=7.0.0,<8.0.0',
 'PyGObject>=3.40.1,<4.0.0',
 'dbus-python>=1.2.16,<2.0.0',
 'entrypoints>=0.3,<0.4',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.2,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['music_bg = music_bg.__main__:main'],
 'mbg_processors': ['blank_image = '
                    'music_bg.img_processors.blank_img:blank_image',
                    'fit = music_bg.img_processors.fit:fit',
                    'load_img = music_bg.img_processors.load_img:load_img',
                    'noop = music_bg.img_processors.noop:noop',
                    'resize = music_bg.img_processors.resize:resize']}

setup_kwargs = {
    'name': 'music-bg',
    'version': '0.1.9',
    'description': 'Dynamic wallpapers with power of mpris2.',
    'long_description': '![python version](https://img.shields.io/pypi/pyversions/music_bg?style=flat-square) ![Build status](https://img.shields.io/github/workflow/status/music-bg/music_bg/Release%20package?style=flat-square) [![version](https://img.shields.io/pypi/v/music_bg?style=flat-square)](https://pypi.org/project/music_bg/)\n\n\n<div align="center">\n<img src="https://raw.githubusercontent.com/music-bg/music_bg/master/images/logo.png" width=700>\n</div>\n\n<p align="center">\n    <a href="https://github.com/music-bg/music_bg/wiki">Wiki</a> •\n    <a href="#about">About</a> •\n    <a href="#installation">Installation</a>\n</p>\n\n<div align="center">\n<h1 id="about">About</h1>\n</div>\n\nThis project is a dynamic wallpaper changer.\nIt waits untill you turn on the music,\ndownloads album cover if it\'s possible and\nsets it as your wallpapper.\n\nAnd the main thing, this project is highly customizable.\nYou can install plugins and write your own configurations.\n\n<div align="center">\n<h1 id="installation">Installation</h1>\n</div>\n\n⚠️ This project requires DBUS to be installed. Currently only linux is supported. ⚠️\n\nTo install this project simply run:\n```bash\npip install music_bg\n# Also you can install extra processors\n# by running\npip install music_bg_extra\n```\n\nThat\'s it. Now you can read our [wiki](https://github.com/music-bg/music_bg/wiki)\nto set up your own music background.\n',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/music-bg/music_bg/wiki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
