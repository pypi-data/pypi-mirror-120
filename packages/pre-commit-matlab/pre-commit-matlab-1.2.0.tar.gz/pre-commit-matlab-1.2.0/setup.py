# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pre_commit_matlab']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['matlab-reflow-comments = '
                     'pre_commit_matlab.matlab_reflow_comments:main']}

setup_kwargs = {
    'name': 'pre-commit-matlab',
    'version': '1.2.0',
    'description': 'A Collection of pre-commit hooks for MATLAB',
    'long_description': "[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pre-commit-matlab)](https://pypi.org/project/pre-commit-matlab/)\n[![PyPI](https://img.shields.io/pypi/v/pre-commit-matlab)](https://pypi.org/project/pre-commit-matlab/)\n[![PyPI - License](https://img.shields.io/pypi/l/pre-commit-matlab?color=magenta)](https://github.com/sco1/pre-commit-matlab/blob/master/LICENSE)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sco1/pre-commit-matlab/main.svg)](https://results.pre-commit.ci/latest/github/sco1/pre-commit-matlab/main)\n[![lint-and-test](https://github.com/sco1/pre-commit-matlab/actions/workflows/lint_test.yml/badge.svg?branch=main)](https://github.com/sco1/pre-commit-matlab/actions/workflows/lint_test.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)\n# pre-commit-matlab\nA collection of [pre-commit](https://pre-commit.com/) hooks for MATLAB\n\nOk... it's just one hook so far but maybe someday there will be more 😃\n\n## Using pre-commit-matlab with pre-commit\nAdd this to your `.pre-commit-config.yaml`\n\n```yaml\n-   repo: https://github.com/sco1/pre-commit-matlab\n    rev: v1.2.0\n    hooks:\n    -   id: matlab-reflow-comments\n        args: [--line-length=100]\n```\n\n## Hooks\n### `matlab-reflow-comments`\nReflow inline comments (lines beginning with `%`) or block comments (delimited by `%{` and `%}`) in MATLAB file(s) (`*.m`) to the specified line length.\n\nBlank comment lines are passed back into the reformatted source code.\n\n* Use `--line-length` to specify line length. (Default: `75`)\n* Use `--reflow-block-comments` to control block comment reflow. (Default: `True`)\n* Use `--ignore-indented` to ignore comments with inner indentation. (Default: `True`)\n  * **NOTE:** This logic *is not* applied to the contents of a block comment.\n* Use `--alternate-capital-handling` to treat comment lines that begin with a capital letter as the start of a new comment block. (Default: `False`)\n  * **NOTE:** This logic *is not* applied to the contents of a block comment.\n\nIf `ignore-indented` is `True`, comments that contain inner indentation of at least two spaces is passed back into the reformatted source code as-is. Leading whitespace in the line is not considered.\n\nFor example:\n\n```matlab\n    % This is not indented\n% This is not indented\n%  This is indented\n%    This is indented\n```\n\nIf `alternate-capital-handling` is `True`, if the line buffer has contents then a line beginning with a capital letter is treated as the start of a new comment block.\n\nFor example:\n\n```matlab\n% This is a comment line\n% This is a second comment line that will not be reflowed into the previous line\n```\n\n**NOTE:** As an opinionated flag, this may lead to false positives so it is off by default. If enabled, pay close attention to the resulting diff to ensure that your comments are being reflowed as desired.\n",
    'author': 'sco1',
    'author_email': 'sco1.git@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sco1/',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
