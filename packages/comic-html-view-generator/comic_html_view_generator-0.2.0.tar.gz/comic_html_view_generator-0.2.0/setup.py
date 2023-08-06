# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comic_html_view_generator']

package_data = \
{'': ['*'],
 'comic_html_view_generator': ['test_output_volume/simulated_comic_volume_001/issue001/*',
                               'test_output_volume/simulated_comic_volume_001/issue002/*']}

entry_points = \
{'console_scripts': ['comic_html_view_generator = '
                     'comic_html_view_generator.chvg:main']}

setup_kwargs = {
    'name': 'comic-html-view-generator',
    'version': '0.2.0',
    'description': 'HTML generator to view comic books',
    'long_description': 'comic_html_view_generator\n=========================\n\ncomic_html_view_generator is a command-line tool and library for creating\nstatic HTML files for viewing comic books. Given a directory with images or\n.cbz files in it, it\'ll create HTML files which embed those images in order,\nand an overall "browse all the comics here" HTML page which will list all the\ncomics books which have had a readable HTML file generated from them.\n\nInstallation\n------------\n\nInstall this library via Pip: ::\n\n    pip install comic-html-view-generator\n\nUse with: ::\n\n    python -m comic_html_view_generator --source <SOURCE_PATH> --destination <DESTINATION_PATH>\n\nAssumptions\n-----------\n\nThis tool makes many assumptions about your directory structure. It assumes\nthat in the directory tree provided, that all the images comprising a single\n"comic book" will be collected into a single folder with all the images in it,\nwith no sub-folders. It\'s assumed that each image in an "image folder" is a\nsingle "page" of that comic book. Additionally, it further assumes that the\nalpha-numeric order (`00` comes before `01` comes before `0a`) of the names of\nthe images in each folder represent the "order" of each page in the comic book.\n\nUsage\n-----\nUsage of the script is as follows: ::\n\n    $ python -m comic_html_view_generator\n    usage: comic_html_view_generator.py [-h] [-v] --source SOURCE --destination DESTINATION\n                                        [--embed-images] [--maintain-existing-images]\n\n    Create HTML files for browsing directories of images as though those directories\n    represent comic books. Will also automatically expand .cbz files.\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      -v, --verbose         If set, logs additional information to stderr during execution\n      --source SOURCE       The source directory of images/cbz files, which will be used as\n                            the basis for the all-new directory with images and HTML files\n                            for viewing those images.\n      --destination DESTINATION\n                            The destination directory to be filled with images and HTML\n                            files for viewing those images.\n      --embed-images        If specified, causes all images to be embedded into the\n                            generated HTML files as base64 encoded data URIs. Grows page\n                            size, but improves portability.\n      --maintain-existing-images\n                            If provided, then images (in folders and CBZ files) will only be\n                            copied into the \'destination\' directory if there isn\'t already a\n                            file with the same name in the destination directory. If an\n                            image file would be copied from source to destination, but it\n                            exists in destination already, then it is not copied if this\n                            argument is provided.\n\n',
    'author': 'Leland Batey',
    'author_email': 'lelandbatey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
