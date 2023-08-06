# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scru160']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scru160',
    'version': '0.2.0',
    'description': 'SCRU-160: Sortable, Clock and Random number-based Unique identifier',
    'long_description': '# SCRU-160: Sortable, Clock and Random number-based Unique identifier\n\nSCRU-160 ID is yet another attempt to supersede [UUID] in the use cases that\nneed decentralized, globally unique time-ordered identifiers. SCRU-160 is\ninspired by [ULID] and [KSUID] and has the following features:\n\n- 160-bit length\n- Sortable by generation time (in binary and in text)\n- Two case-insensitive encodings: 32-character base32hex and 40-character hex\n- More than 32,768 unique, time-ordered but unpredictable IDs per millisecond\n- Nearly 111-bit randomness for collision resistance\n\n```python\nfrom scru160 import scru160, scru160f\n\nprint(scru160())  # e.g. "05TVFQQ8UGDNKHDJ79AEGPHU7QP7996H"\nprint(scru160())  # e.g. "05TVFQQ8UGDNNVCCNUH0Q8JDD3IPHB8R"\n\nprint(scru160f())  # e.g. "017bf7eb48f41b7d6bd295bc5adc43436bc969df"\nprint(scru160f())  # e.g. "017bf7eb48f41b7e1bc98aec348dfa1539b41288"\n```\n\n[uuid]: https://en.wikipedia.org/wiki/Universally_unique_identifier\n[ulid]: https://github.com/ulid/spec\n[ksuid]: https://github.com/segmentio/ksuid\n\n## License\n\nCopyright 2021 LiosK\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use\nthis file except in compliance with the License. You may obtain a copy of the\nLicense at\n\nhttp://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software distributed\nunder the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied. See the License for the\nspecific language governing permissions and limitations under the License.\n',
    'author': 'LiosK',
    'author_email': 'contact@mail.liosk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scru160/python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.12,<4.0.0',
}


setup(**setup_kwargs)
