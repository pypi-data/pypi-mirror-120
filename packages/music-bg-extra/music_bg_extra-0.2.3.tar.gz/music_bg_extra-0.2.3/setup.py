# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['music_bg_extra', 'music_bg_extra.processors', 'music_bg_extra.variables']

package_data = \
{'': ['*']}

install_requires = \
['Pillow-SIMD>=7.0.0,<8.0.0', 'music-bg>=0.1.9,<0.2.0']

entry_points = \
{'mbg_processors': ['box_blur = music_bg_extra.processors.blur:box_blur',
                    'circle = music_bg_extra.processors.circle:circle',
                    'gaussian_blur = '
                    'music_bg_extra.processors.blur:gaussian_blur',
                    'pop_filter = music_bg_extra.processors.pop:pop_filter'],
 'mbg_variables': ['uuid4 = music_bg_extra.variables.uuid_gen:uuid4']}

setup_kwargs = {
    'name': 'music-bg-extra',
    'version': '0.2.3',
    'description': 'Extra utils for music_bg',
    'long_description': '# Extra processors and variables for music_bg.\n\nThis is a plugin for [music_bg](https://github.com/music-bg/music_bg) package.\n\n## Plugin contents\n\nProcessors:\n* Box blur;\n* Gaussian blur;\n* Circle;\n* pop_filter\n\nVariables:\n* uuid4\n\nSource image for all examples is:\n![box_blur](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/src.png)\nThis is cover for album "SCUZZY" by [Nikki Nair](https://open.spotify.com/artist/27JCep1zDO3K8GY50trDo6?si=sQZBGPUGSByvyzZY45AduA&dl_branch=1).\n\n# Processors\n## Blurs\n\n![box_blur](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/box_blur.png)\n\nTo blur an image add this to your layer config:\n```json\n{\n    "name": "box_blur",\n    "args": {\n        "strength": "6"\n    }\n}\n```\n\n![box_blur](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/gaussian_blur.png)\n\nYou can use gaussian blur.\nAs an optional parameter you\ncan adjust radius.\n```json\n{\n    "name": "gaussian_blur",\n    "args": {\n        "radius": "5.4"\n    }\n}\n```\n\n## Circle processor\n\n![circle](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/circle.png)\n\nThis processor will crop a circle\nout of an image.\nTo use it add this to your conig file:\n```json\n{\n    "name": "circle"\n}\n```\n\nIt doesn\'t take any args.\n\n## Pop filter\n\n![pop_filter](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/pop_filter.png)\n\nThis processor splits image onto 3 color channels and places near each other.\n\n```json\n{\n    "name": "pop_filter",\n    "args": {\n        "offset_x": 100,\n        "offset_y": 100,\n        "increase_factor": 1.4,\n        "decrease_factor": 0.8\n    }\n}\n```\nincrease and decrease factors change\nincreasing and decreasing incdividual colors for each color chanel.\n\n# Variables\n\nYou can use "{uuid4}" or "{uuid4.hex}" in your config to generate\nUUIDv4.\n',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/music-bg/music_bg_extra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
