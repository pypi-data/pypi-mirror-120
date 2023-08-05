# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyclonedx', 'cyclonedx.model', 'cyclonedx.output', 'cyclonedx.parser']

package_data = \
{'': ['*'], 'cyclonedx': ['schema/*', 'schema/ext/*']}

install_requires = \
['importlib-metadata>=4.8.1,<5.0.0',
 'packageurl-python>=0.9.4,<0.10.0',
 'requirements_parser>=0.2.0,<0.3.0',
 'setuptools>=50.3.2,<51.0.0',
 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'cyclonedx-python-lib',
    'version': '0.3.0',
    'description': 'A library for producing CycloneDX SBOM (Software Bill of Materials) files.',
    'long_description': '# Python Library for generating CycloneDX\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/CycloneDX/cyclonedx-python-lib/Python%20CI)\n![Python Version Support](https://img.shields.io/badge/python-3.6+-blue)\n![PyPI Version](https://img.shields.io/pypi/v/cyclonedx-python-lib?label=PyPI&logo=pypi)\n[![GitHub license](https://img.shields.io/github/license/CycloneDX/cyclonedx-python-lib)](https://github.com/CycloneDX/cyclonedx-python-lib/blob/main/LICENSE)\n[![GitHub issues](https://img.shields.io/github/issues/CycloneDX/cyclonedx-python-lib)](https://github.com/sCycloneDX/cyclonedx-python-lib/issues)\n[![GitHub forks](https://img.shields.io/github/forks/CycloneDX/cyclonedx-python-lib)](https://github.com/CycloneDX/cyclonedx-python-lib/network)\n[![GitHub stars](https://img.shields.io/github/stars/CycloneDX/cyclonedx-python-lib)](https://github.com/CycloneDX/cyclonedx-python-lib/stargazers)\n\n----\n\nThis CycloneDX module for Python can generate valid CycloneDX bill-of-material document containing an aggregate of all\nproject dependencies.\n\nThis module is not designed for standalone use. If you\'re looking for a CycloneDX tool to run to generate (SBOM) software\nbill-of-materials documents, why not checkout:\n\n- [cyclonedx-python](https://github.com/CycloneDX/cyclonedx-python)\n\nAdditionally, the following tool can be used as well (and this library was written to help improve it)\n- [Jake](https://github.com/sonatype-nexus-community/jake)\n\nAdditionally, you can use this module yourself in your application to programmatically generate SBOMs.\n\nCycloneDX is a lightweight BOM specification that is easily created, human-readable, and simple to parse.\n\n## Installation\n\nInstall from pypi.org as you would any other Python module:\n\n```\npip install cyclonedx-python-lib\n```\n\n## Architecture\n\nThis module break out into three key areas:\n\n1. **Parser**: Use a parser that suits your needs to automatically gather information about your environment or\n   application\n2. **Model**: Internal models used to unify data from different parsers\n3. **Output**: Choose and configure an output which allows you to define output format as well as the CycloneDX schema\n   version\n\n### Parsing\n\nYou can use one of the parsers to obtain information about your project or environment. Available parsers:\n\n| Parser | Class / Import | Description |\n| ------- | ------ | ------ |\n| Environment | `from cyclonedx.parser.environment import EnvironmentParser` | Looks at the packaged installed in your current Python environment. |\n| PoetryParser | `from cyclonedx.parser.poetry import PoetryParser` | Parses `poetry.lock` content passed in as a string. |\n| PoetryFileParser | `from cyclonedx.parser.poetry import PoetryFileParser` | Parses the `poetry.lock` file at the supplied path. |\n| RequirementsParser | `from cyclonedx.parser.requirements import RequirementsParser` | Parses a multiline string that you provide that conforms to the `requirements.txt` [PEP-508](https://www.python.org/dev/peps/pep-0508/) standard. |\n| RequirementsFileParser | `from cyclonedx.parser.requirements import RequirementsFileParser` | Parses a file that you provide the path to that conforms to the `requirements.txt` [PEP-508](https://www.python.org/dev/peps/pep-0508/) standard. |\n\n#### Example\n\n```\nfrom cyclonedx.parser.environment import EnvironmentParser\n\nparser = EnvironmentParser()\n```\n\n### Modelling\n\nYou can create a BOM Model from either a Parser instance or manually using the methods avaialbel directly on the `Bom` class.\n\nThe model also supports definition of vulnerabilities for output using the CycloneDX schema extension for \n[Vulnerability Disclosures](https://cyclonedx.org/use-cases/#vulnerability-disclosure) as of version 0.3.0.\n\n**Note:** Known vulnerabilities associated with Components can be sourced from various data sources, but this library \nwill not source them for you. Perhaps look at [Jake](https://github.com/sonatype-nexus-community/jake) if you\'re interested in this.\n\n#### Example from a Parser\n\n```\nfrom cyclonedx.model.bom import Bom\nfrom cyclonedx.parser.environment import EnvironmentParser\n\nparser = EnvironmentParser()\nbom = Bom.from_parser(parser=parser)\n```\n\n### Generating Output\n\nOnce you have an instance of a `Bom` you can produce output in either `JSON` or `XML` against any of the supporting CycloneDX schema versions as you require.\n\nWe provide two helper methods:\n1. Output to string (for you to do with as you require)\n2. Output directly to a filename you provide\n\n##### Example as JSON\n\n```\nfrom cyclonedx.output import get_instance, OutputFormat\n\noutputter = get_instance(bom=bom, output_format=OutputFormat.JSON)\noutputter.output_as_string()\n```\n\n##### Example as XML\n```\nfrom cyclonedx.output import get_instance, SchemaVersion\n\noutputter = get_instance(bom=bom, schema_version=SchemaVersion.V1_2)\noutputter.output_to_file(filename=\'/tmp/sbom-v1.2.xml\')\n```\n\n## Schema Support\n\nThis library is a work in progress and complete support for all parts of the CycloneDX schema will come in future releases.\n\nHere is a summary of the parts of the schema supported by this library:\n\n_Note: We refer throughout using XPath, but the same is true for both XML and JSON output formats._\n\n<table width="100%">\n   <thead>\n      <tr>\n         <th>XPath</th>\n         <th>Support v1.3</th>\n         <th>Support v1.2</th>\n         <th>Support v1.1</th>\n         <th>Support v1.0</th>\n         <th>Notes</th>\n      </tr>\n   </thead>\n   <tbody>\n      <tr>\n         <td><code>/bom</code></td>\n         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>\n         <td>\n            This is the root element and is supported with all it\'s defined attributes.\n         </td>\n      </tr>\n      <tr>\n         <td><code>/bom/metadata</code></td>\n         <td>Y</td><td>Y</td><td>N/A</td><td>N/A</td>\n         <td>\n            Only <code>timestamp</code> is currently supported \n         </td>\n      </tr>\n      <tr>\n         <td><code>/bom/components</code></td>\n         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>\n         <td>&nbsp;</td>\n      </tr>\n      <tr>\n         <th colspan="6"><strong><code>/bom/components/component</code></strong></th>\n      </tr>\n      <tr>\n         <td><code>./author</code></td>\n         <td>Y</td><td>Y</td><td>N/A</td><td>N/A</td>\n         <td>&nbsp;</td>\n      </tr>\n      <tr>\n         <td><code>./name</code></td>\n         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>\n         <td>&nbsp;</td>\n      </tr>\n      <tr>\n         <td><code>./version</code></td>\n         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>\n         <td>&nbsp;</td>\n      </tr>\n      <tr>\n         <td><code>./purl</code></td>\n         <td>Y</td><td>Y</td><td>Y</td><td>Y</td>\n         <td>&nbsp;</td>\n      </tr>\n   </tbody>\n</table>\n\n### Notes on Schema Support\n\n1. N/A is where the CycloneDX standard does not include this\n2. If the table above does not refer to an element, it is not currently supported\n\n## Python Support\n\nWe endeavour to support all functionality for all [current actively supported Python versions](https://www.python.org/downloads/).\nHowever, some features may not be possible/present in older Python versions due to their lack of support.\n\n## Changelog\n\nSee our [CHANGELOG](./CHANGELOG.md).\n\n## Copyright & License\nCycloneDX Python Lib is Copyright (c) OWASP Foundation. All Rights Reserved.\n\nPermission to modify and redistribute is granted under the terms of the Apache 2.0 license.\n',
    'author': 'Paul Horton',
    'author_email': 'phorton@sonatype.com',
    'maintainer': 'Paul Horton',
    'maintainer_email': 'phorton@sonatype.com',
    'url': 'https://github.com/CycloneDX/cyclonedx-python-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
