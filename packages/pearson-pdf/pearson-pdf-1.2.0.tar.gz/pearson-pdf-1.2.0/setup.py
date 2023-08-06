# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pearson_pdf']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.2,<9.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['pearson_pdf = pearson_pdf.__main__:main']}

setup_kwargs = {
    'name': 'pearson-pdf',
    'version': '1.2.0',
    'description': 'Tool to download Pearson books as PDFs.',
    'long_description': "# pearson-pdf\n\nTool to download Pearson books as PDFs.\n\n## Installation\n\nInstall `pearson-pdf` using pip.\n\n```bash\npip install pearson-pdf\n```\n\n## Usage\n\nTo download a PDF, you'll need to get the book's ID:\n\n1. Open up DevTools in your browser.\n2. Navigate to Console.\n3. Type in:\n   ```js\n   window.foxitAssetURL;\n   ```\n4. Copy that URL. pearson-pdf will parse the ID from that URL.\n\nNow you can download your PDF:\n\n```bash\n# with an id\npearson_pdf xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\n\n# with a url\npearson_pdf https://example.com/generated/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/foxit-assets\n```\n\nMore information on usage is in the help page:\n\n```bash\npearson_pdf -h\n```\n\n## License\n\nSee [LICENSE](LICENSE) for details.\n",
    'author': 'Joel',
    'author_email': 'joel@joel.tokyo',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jyooru/pearson-pdf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
