# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['borderline']
setup_kwargs = {
    'name': 'borderline',
    'version': '0.3.0',
    'description': 'Tests that new imports within a module respect the public API boundary.',
    'long_description': '# Borderline\n\nStop letting modules reach into other modules.\n\n---\n\n![python-package](https://github.com/ctk3b/borderline/actions/workflows/python-package.yml/badge.svg)\n[![PyPI version fury.io](https://badge.fury.io/py/borderline.svg)](https://pypi.python.org/pypi/borderline/)\n\nThis library provides one thing and one thing only: a test class called `TestModuleImports`. \n\nTo use the test, subclass it in the test suite of the module you want to isolate and define that module\'s borderlines.\nThe test will fail if a module is not respecting those borderlines.\n\nFor example, a module called `report_builder` could have the following definition:\n\n```python\nclass TestReportBuilder(ModuleImports):\n    module = "reporting.report_builder"\n    \n    # The public API of the module.\n    # External modules should only import from here.\n    public_submodules = (\n        "reporting.report_builder.api",\n    )\n    # Modules that are considered outside of `module` and should not be imported\n    # by `module` unless they are a legitimate dependency.\n    external_modules = (\n        "reporting",\n    )\n    # Modules outside of `module` that ARE legitimate dependencies.\n    external_dependencies = (\n        "reporting.review.api",\n        "reporting.common",\n    )\n\n    # Directory to store imports that are currently allowed.\n    # This is useful when you are trying to isolate an existing module\n    # that is not respecting its borderlines.\n    grandfather_filedir = Path(\n        "reporting/report_builder/tests/data/borderline", parents=True, exist_ok=True\n    )\n```\n',
    'author': 'Christoph Klein',
    'author_email': 'ckleinemail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ctk3b/borderline',
    'py_modules': modules,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
