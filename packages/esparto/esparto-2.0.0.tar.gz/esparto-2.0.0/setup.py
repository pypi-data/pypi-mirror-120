# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esparto']

package_data = \
{'': ['*'], 'esparto': ['resources/css/*', 'resources/jinja/*']}

install_requires = \
['Pillow>=7.0.0,<9',
 'jinja2>=2.10.1,<4.0.0',
 'markdown>=3.1,<4.0',
 'pyyaml>=5.1']

extras_require = \
{':python_version < "3.7"': ['dataclasses'],
 'extras': ['beautifulsoup4>=4.7', 'weasyprint>=51,<53']}

setup_kwargs = {
    'name': 'esparto',
    'version': '2.0.0',
    'description': 'Simple HTML page and PDF document generator for Python.',
    'long_description': 'esparto\n=======\n\n[![image](https://img.shields.io/pypi/v/esparto.svg)](https://pypi.python.org/pypi/esparto)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/esparto.svg)](https://pypi.python.org/pypi/esparto/)\n[![Build Status](https://travis-ci.com/domvwt/esparto.svg?branch=main)](https://travis-ci.com/domvwt/esparto)\n[![codecov](https://codecov.io/gh/domvwt/esparto/branch/main/graph/badge.svg?token=35J8NZCUYC)](https://codecov.io/gh/domvwt/esparto)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=domvwt_esparto&metric=alert_status)](https://sonarcloud.io/dashboard?id=domvwt_esparto)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/esparto)\n\n\n## Introduction\n**esparto** is a Python package for building shareable reports with content\nfrom popular data analysis libraries.\nWith just a few lines of code, **esparto** turns DataFrames, plots, and\nMarkdown into an interactive webpage or PDF document.\n\nDocuments produced by **esparto** are completely portable - no backend server\nis required - and entirely customisable using CSS and Jinja templating.\nAll content dependencies are declared inline or loaded via a CDN, meaning your\nreports can be shared by email, hosted on a standard http server, or made\navailable as static pages as-is.\n\n\n## Basic Usage\n```python\nimport esparto as es\npage = es.Page(title="My Report")\npage["Data Analysis"] = (pandas_dataframe, plotly_figure)\npage.save_html("my-report.html")\n```\n\n\n## Main Features\n* Automatic and adaptive layout\n* Customisable with CSS or Jinja\n* Jupyter Notebook friendly\n* Output as HTML or PDF\n* Built-in adaptors for:\n    * Markdown\n    * Images\n    * [Pandas DataFrames][Pandas]\n    * [Matplotlib][Matplotlib]\n    * [Bokeh][Bokeh]\n    * [Plotly][Plotly]\n\n\n## Installation\n**esparto** is available from PyPI:\n```bash\npip install esparto\n```\n\nIf PDF output is required, `weasyprint` must also be installed:\n```bash\npip install weasyprint\n```\n\n\n## Dependencies\n*   [python](https://python.org/) >= 3.6\n*   [jinja2](https://palletsprojects.com/p/jinja/)\n*   [markdown](https://python-markdown.github.io/)\n*   [Pillow](https://python-pillow.org/)\n*   [PyYAML](https://pyyaml.org/)\n*   [weasyprint](https://weasyprint.org/) _(optional - required for PDF output)_\n\n\n## License\n[MIT](https://opensource.org/licenses/MIT)\n\n\n## Documentation\nFull documentation and examples are available at [domvwt.github.io/esparto/](https://domvwt.github.io/esparto/).\n\n## Contributions, Issues, and Requests\nAll feedback and contributions are welcome - please raise an issue or pull request on [GitHub][GitHub].\n\n\n## Examples\nIris Report - [Webpage](https://domvwt.github.io/esparto/examples/iris-report.html) |\n[PDF](https://domvwt.github.io/esparto/examples/iris-report.pdf)\n\nBokeh and Plotly - [Webpage](https://domvwt.github.io/esparto/examples/interactive-plots.html) |\n[PDF](https://domvwt.github.io/esparto/examples/interactive-plots.pdf)\n\n<br>\n\n<p width=100%>\n<img width=80%  src="https://github.com/domvwt/esparto/blob/fdc0e787c0bc013d16667773e82e21c647b71d91/docs/images/iris-report-compressed.png?raw=true" alt="example page" style="border-radius:0.5%;">\n</p>\n\n<!-- Links -->\n[Bootstrap]: https://getbootstrap.com/docs/4.6/getting-started/introduction/\n[Pandas]: https://pandas.pydata.org/\n[Matplotlib]: https://matplotlib.org/\n[Bokeh]: https://docs.bokeh.org/en/latest/index.html\n[Plotly]: https://plotly.com/\n[GitHub]: https://github.com/domvwt/esparto\n',
    'author': 'Dominic Thorn',
    'author_email': 'dominic.thorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://domvwt.github.io/esparto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
