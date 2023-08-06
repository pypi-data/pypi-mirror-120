# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gcrc']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'pydantic[dotenv]>=1.8.2,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'typer[colorama]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['gcrc = gcrc.main:app']}

setup_kwargs = {
    'name': 'gcrc',
    'version': '1.0.4',
    'description': 'Google Container Registry Cleanup utility',
    'long_description': '# Google Container Registry Cleanup utility\n\nIf you use a CI system to push images to Google Container Registry you will eventually run into a situation where you\'re paying more than you would like for the storage there.\n\nThis tool helps you keep those costs reasonable, while allowing you to benefit from caches, keeping backups for rollbacks, etc.\n\n## Prerequisites and setup\n\n- [Python 3.9+](https://www.python.org/downloads/)\n- [Gcloud SDK](https://cloud.google.com/sdk/docs/install) with an authentication token that has admin access to the registry properly configured\n\n```bash\npip install -U gcrc\n```\n\n## Usage\n\nReplace `gcr.io/project-name` with the specific GCR address to your repository, e.g. if your Google Cloud project is called `foo-bar` and it\'s in the EU zone this would likely be `eu.gcr.io/foo-bar`.\n\n### List all images\n\nFigures out the different images we can access in the Container Registry.\n\n```bash\ngcrc list-images gcr.io/project-name\n```\n\n### Show information on images\n\nAnalyzes current images and any need for cleanup based on current configuration without actually deleting anything. Use to check that configuration seems correct.\n\n```bash\ngcrc image-info gcr.io/project-name\n```\n\n### Clean up images\n\nLook up images with unneeded tags and delete them from Google Container Registry\n\n```bash\ngcrc cleanup gcr.io/project-name\n```\n\n## Configuration\n\nThe following environment variables can be used to adjust the configuration:\n\n```\nKEEP_TAGS_MIN=10\n```\n\nKeeps at least this many tags for every image.\n\n```\nKEEP_TAGS_DAYS=14\n```\n\nKeep everything from within this many days.\n\n```\nKEEP_EXTRA=\'["^latest$", "^(master|main)-"]\'\n```\n\nList of regex matches for important images that we want to keep an extra `KEEP_TAGS_MIN` items of. Formatted as a JSON list of strings.\n\nThe default is to keep `latest` and any tags starting with `master-` or `main-` for people who tag their images like `<branch>-<timestamp or commit hash or uuid>`.\n\nYou can also put these in a `.env` -file, but environment variables take priority over `.env`.\n\n```\n# .env\nKEEP_TAGS_MIN=10\nKEEP_TAGS_DAYS=14\nKEEP_EXTRA=\'["^important-", "^latest$"]\'\n```\n\n# Financial support\n\nThis project has been made possible thanks to [Cocreators](https://cocreators.ee) and [Lietu](https://lietu.net). You can help us continue our open source work by supporting us on [Buy me a coffee](https://www.buymeacoffee.com/cocreators).\n\n[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cocreators)\n',
    'author': 'Janne Enberg',
    'author_email': 'janne.enberg@lietu.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lietu/gcrc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
