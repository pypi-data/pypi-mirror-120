# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['palettecleanser', 'palettecleanser.cli']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pywal>=3.3.0,<4.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['pclean = palettecleanser.cli.main:app']}

setup_kwargs = {
    'name': 'palettecleanser',
    'version': '0.2.0',
    'description': '',
    'long_description': '# Palette Cleanser\n\nWe all know that refreshing sensation of setting our desktop applications to a\ndelicious color scheme such as [Dracula](https://draculatheme.com/) or\n[Nord](https://www.nordtheme.com/). But even the tastiest of color schemes can\ngrow bland after awhile, leaving you craving a new flavor for your desktop apps.\n\nPalette Cleanser provides a means for storing your configuration files as\ntemplates and you color palettes as deployable desktop themes so that you can\navoid the hassle of manually editing hex codes when switching your\napplications to a new color scheme.\n\n# Requirements\n\nPython 3.9+\n\n## Dependencies\n\n* Jinja2 3.0.1+\n* numpy 1.21.1+\n* pywal 3.3.0+\n* PyYAML 5.4.1+\n* tabulate 0.8.9+\n* typer 0.3.2+\n\n# Installation\n\nInstall Palette Cleanser with pip:\n\n``` sh\n$ pip install [--user] palettecleanser\n```\n\n# Documentation\n\nCheck out the [wiki](https://github.com/mmuldo/palette-cleanser/wiki) for detailed documentation.\n\n# Quickstart\n\nCreate a template:\n``` sh\n$ pclean template create .config/alacritty/alacritty.yml\n```\n\nCreate a theme:\n``` sh\n$ pclean theme generate --from-image path/to/image --name my-clean-theme\n```\n\nDeploy a theme:\n``` sh\n$ pclean theme deploy my-clean-theme --template .config/alacritty/alacritty.yml\n```\n\n# Licence\n\nThis project is licensed under the terms of the MIT Licence.\n',
    'author': 'Matt Muldowney',
    'author_email': 'matt.muldowney@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mmuldo/palette-cleanser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
