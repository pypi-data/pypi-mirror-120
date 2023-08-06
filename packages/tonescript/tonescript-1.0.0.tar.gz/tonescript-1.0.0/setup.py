# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tonescript']

package_data = \
{'': ['*']}

install_requires = \
['lark>=0.11.3,<0.12.0']

setup_kwargs = {
    'name': 'tonescript',
    'version': '1.0.0',
    'description': 'Python package for working with ToneScript, a syntax for describing the characteristics of the call progress tones used in telephony.',
    'long_description': '# tonescript\n\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/gdereese/tonescript/CI/main?style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/tonescript?style=for-the-badge)\n\nPython package for working with ToneScript, a syntax for describing the characteristics of the call progress tones used in telephony. It is the primary method for configuring tones in Sipura, Linksys, and Cisco VoIP systems.\n\n## Features\n\n* Parses ToneScript into its components: frequencies, cadence sections, and tone segments\n* Constructs ToneScript from component objects\n* Renders ToneScript objects into WAV audio files\n\n## Installation\n\n```shell\npip install tonescript\n```\n\n## Overview of ToneScript syntax\n\nFor example, the **ToneScript** that defines the standard North American dial tone is as follows:\n\n```text\n350@-13,440@-13;10(*/0/1+2)\n```\n\n`350@-13,440@-13` is the **FreqScript** portion, which describes the frequency components used to make up the sound heard in the tone. The audio frequency (in Hz) and level (in dBm) are specified for each component, and each component is separated by a comma (`,`).\n\nThis FreqScript defines 2 frequency components:\n\n1. 350 Hz @ -13 dBm\n2. 440 Hz @ -13 dBm\n\n`10(*/0/1+2)` is the **CadScript** portion, which describes the cadence of the tone, or the rhythm of its defined frequency components and silence.\n\nThe tone is divided into sections, each of which has its own sequence of tone segments.\n\nA tone segment plays using one or more of the frequency components defined in the FreqScript for a specified duration (in seconds), followed by an optional period of silence.\n\nA cadence section can also have its own duration; the tone segments within it are played and looped as needed until the section duration has elapsed.\n\nWhen specifying duration values, an asterisk (`*`) indicates that the duration is continuous.\n\nThe above CadScript defines a single section which plays for 10 seconds. The section has a single tone segment:\n\n* `*` = Plays continuously\n* `0` = No silence\n* `1+2` = Uses the first and second frequency components in the list\n\n## Usage\n\n### Parsing a ToneScript\n\n```python\nimport tonescript as ts\n\n# standard North American dial tone\nscript = "350@-13,440@-13;10(*/0/1+2)"\n\ntone = ts.parse(script)\n\nprint(str(tone))\n```\n\n**Output:**\n\n```shell\nFrequency components:\n    1) 350 Hz @ -13 dBm\n    2) 440 Hz @ -13 dBm\nCadence sections:\n    1) For 10 s:\n        1) Always on, frequencies 1, 2\n```\n\n### Constructing a ToneScript\n\n```python\nfrom decimal import Decimal\n\nimport tonescript as ts\nimport tonescript.model as ts_model\n\n# standard North American dial tone\ntone = ts_model.ToneScript(\n    ts_model.FreqScript([\n        ts_model.FrequencyComponent(350, Decimal("-13")),\n        ts_model.FrequencyComponent(440, Decimal("-13"))\n    ]),\n    ts_model.CadScript([\n        ts_model.CadenceSection(Decimal("10"), [\n            ts_model.ToneSegment(Decimal("inf"), Decimal("0"), [1, 2])\n        ])\n    ])\n)\n\nscript = ts.unparse(tone)\n\nprint(script)\n```\n\n**Output:**\n\n```shell\n350@-13,440@-13;10(*/0/1+2)\n```\n\n### Rendering a ToneScript into a WAV audio file\n\n```python\nimport tonescript as ts\n\n# standard North American dial tone\ntone = ts.parse("350@-13,440@-13;10(*/0/1+2)")\n\n# 16-bit PCM, 44.1 kHz sample rate\nts.render(tone, "./dial_tone.wav", 44100, 2)\n```\n\n## Support\n\nPlease use the project\'s [Issues page](https://github.com/gdereese/tonescript/issues) to report any issues.\n\n## Contributing\n\n### Installing for development\n\n```shell\npoetry install\n```\n\n### Linting source files\n\n```shell\npoetry run pylint --rcfile .pylintrc src/tonescript\n```\n\n### Running tests\n\n```shell\npoetry run pytest\n```\n\n## License\n\nThis library is licensed under the terms of the [MIT license](https://choosealicense.com/licenses/mit/).\n',
    'author': 'Gary DeReese',
    'author_email': 'garydereese@sbcglobal.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gdereese/tonescript',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
