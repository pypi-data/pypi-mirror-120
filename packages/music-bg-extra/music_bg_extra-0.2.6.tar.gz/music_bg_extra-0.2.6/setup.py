# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['music_bg_extra', 'music_bg_extra.processors', 'music_bg_extra.variables']

package_data = \
{'': ['*']}

install_requires = \
['Pillow-SIMD>=7.0.0,<8.0.0', 'music-bg>=0.2.0,<0.3.0', 'numpy>=1.21.2,<2.0.0']

entry_points = \
{'mbg_processors': ['box_blur = music_bg_extra.processors.blur:box_blur',
                    'circle = music_bg_extra.processors.circle:circle',
                    'gaussian_blur = '
                    'music_bg_extra.processors.blur:gaussian_blur',
                    'pop_filter = music_bg_extra.processors.pop:pop_filter',
                    'print = music_bg_extra.processors.print:img_print',
                    'radial_gradient = '
                    'music_bg_extra.processors.gradients:radial_gradient'],
 'mbg_variables': ['least_frequent_color = '
                   'music_bg_extra.variables.colors:most_frequent_color_inverted_var',
                   'most_frequent_color = '
                   'music_bg_extra.variables.colors:most_frequent_color_var',
                   'most_frequent_color_inverted = '
                   'music_bg_extra.variables.colors:most_frequent_color_inverted_var',
                   'uuid4 = music_bg_extra.variables.uuid_gen:uuid4']}

setup_kwargs = {
    'name': 'music-bg-extra',
    'version': '0.2.6',
    'description': 'Extra utils for music_bg',
    'long_description': '# Extra processors and variables for music_bg.\n\nThis is a plugin for [music_bg](https://github.com/music-bg/music_bg) package.\n\n## Plugin contents\n\nProcessors:\n* Box blur;\n* Gaussian blur;\n* Circle;\n* pop_filter\n* print\n* radial_gradient\n\nVariables:\n* uuid4\n* most_frequent_color\n* least_frequent_color or most_frequent_color_inverted\n\n\nSource image for all examples is:\n![box_blur](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/src.png)\nThis is cover for album "SCUZZY" by [Nikki Nair](https://open.spotify.com/artist/27JCep1zDO3K8GY50trDo6?si=sQZBGPUGSByvyzZY45AduA&dl_branch=1).\n\n# Processors\n## Blurs\n\n![box_blur](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/box_blur.png)\n\nTo blur an image add this to your layer config:\n```json\n{\n    "name": "box_blur",\n    "args": {\n        "strength": "6"\n    }\n}\n```\n\n![box_blur](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/gaussian_blur.png)\n\nYou can use gaussian blur.\nAs an optional parameter you\ncan adjust radius.\n```json\n{\n    "name": "gaussian_blur",\n    "args": {\n        "radius": "5.4"\n    }\n}\n```\n\n## Circle processor\n\n![circle](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/circle.png)\n\nThis processor will crop a circle\nout of an image.\nTo use it add this to your conig file:\n```json\n{\n    "name": "circle"\n}\n```\n\nIt doesn\'t take any args.\n\n## Pop filter\n\n![pop_filter](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/pop_filter.png)\n\nThis processor splits image onto 3 color channels and places near each other.\n\n```json\n{\n    "name": "pop_filter",\n    "args": {\n        "offset_x": 100,\n        "offset_y": 100,\n        "increase_factor": 1.4,\n        "decrease_factor": 0.8\n    }\n}\n```\nincrease and decrease factors change\nincreasing and decreasing incdividual colors for each color chanel.\n\n# Print\n\n![print](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/print_processor.png)\n\nThis processor renders text on an image.\n\n```json\n{\n  "name": "print",\n  "args": {\n    "text": "This text created by processor",\n    "color": "#FFFFFF",\n    "font": "FiraCode-Retina",\n    "font_size": 30,\n    "start_x": null,\n    "start_y": null,\n    }\n}\n```\n\nyou can adjust font and size.\nAlso you can choose x and y coordinates where to\nstart draw.\n\n\n# Radial gradient\n![radial_gradient](https://raw.githubusercontent.com/music-bg/music_bg_extra/master/images/radial_gradient.png)\n\nThis processor creates radial gradient with\ntwo colors "inner" and "outer".\nInner - color at the center of an image,\nouter - color at the border.\n\n# Variables\n\n## uuid4\nYou can use "{uuid4}" or "{uuid4.hex}" in your config to generate\nUUIDv4.\n\n\n## most_frequent_color\n\nThis variable is used to retrieve\nmost frequent color of an image in\nhex format.\n\n## least_frequent_color\n\nThis variable is used to retrieve\ninverted color to the most frequent one.\n\nIt\'s calculated by inverting the\noriginal color.\n\ninverted = (255 - red, 255 - green, 255 - blue)\n\nAlso this variable has a synonym "`most_frequent_color_inverted`".\n',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/music-bg/music_bg_extra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
