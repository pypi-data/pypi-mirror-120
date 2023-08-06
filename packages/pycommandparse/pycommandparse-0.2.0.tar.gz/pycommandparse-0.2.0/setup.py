# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycommandparse', 'pycommandparse.parsers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycommandparse',
    'version': '0.2.0',
    'description': 'A collection of classes that help parse commands.',
    'long_description': '# Pycommandparse\n## Structure\nIn pycommandparse, each function is bound to a `pycommandparse.Command` instance.\nThe Parser takes these as inputs.\n\nInternally, the parser has a dictionary with keys having all names and aliases with the values being the corresponding `Command` instances.\n\nThe Parser matches the imcoming commands to the given names/aliases and runs the command with the arguments.\n\n## Examples\n\n\n### Defining and Adding Commands\n\nMethod 1: Directly defining the command.\n\n```py\nfrom pycommandparse.parsers import BaseParser\n\nparser = BaseParser()\n\n# Ways to define commands\n\n## 1. directly via pycommandparse.Command\nfrom pycommandparse import Command\n\ndef mult(x, y):\n    return int(x)*int(y)\n\nmultiplication = Command(name="multiply", \n                    command=mult, \n                    usage="multiply *args", description="Multiplies 2 numbers you input", \n                    number_of_args=2, \n                    aliases=[\'product\'])\n\nparser.add_command(multiplication)\n\nparser.parse_run("multiply 3 5") # Outputs "15"\n```\n\nMethod 2: Decorators.\n\n```py\nfrom pycommandparse.parsers import BaseParser\n\n\n## 2. Using decorator\n\n### Not specifying number_of_args will allow any number of arguments.\n\n@parser.command(name="add", \n            aliases=[\'sum\'], \n            usage="add *numbers", \n            description="Adds what you input.")\ndef add(*numbers):\n    return sum([int(number) for number in numbers])\n\nparser.parse_run("add 3 5 6 7") # Outputs "21"\nparser.parse_run("add 2 4") # Outputs "6"\n```',
    'author': 'thelegendbeacon',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
