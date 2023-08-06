# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scru160', 'scru160.cli']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['scru160 = scru160.cli:generate',
                     'scru160-inspect = scru160.cli:inspect']}

setup_kwargs = {
    'name': 'scru160',
    'version': '0.2.2',
    'description': 'SCRU-160: Sortable, Clock and Random number-based Unique identifier',
    'long_description': '# SCRU-160: Sortable, Clock and Random number-based Unique identifier\n\nSCRU-160 ID is yet another attempt to supersede [UUID] in the use cases that\nneed decentralized, globally unique time-ordered identifiers. SCRU-160 is\ninspired by [ULID] and [KSUID] and has the following features:\n\n- 160-bit length\n- Sortable by generation time (in binary and in text)\n- Two case-insensitive encodings: 32-character base32hex and 40-character hex\n- More than 32,768 unique, time-ordered but unpredictable IDs per millisecond\n- Nearly 111-bit randomness for collision resistance\n\n```python\nfrom scru160 import scru160, scru160f\n\nprint(scru160())  # e.g. "05TVFQQ8UGDNKHDJ79AEGPHU7QP7996H"\nprint(scru160())  # e.g. "05TVFQQ8UGDNNVCCNUH0Q8JDD3IPHB8R"\n\nprint(scru160f())  # e.g. "017bf7eb48f41b7d6bd295bc5adc43436bc969df"\nprint(scru160f())  # e.g. "017bf7eb48f41b7e1bc98aec348dfa1539b41288"\n```\n\n[uuid]: https://en.wikipedia.org/wiki/Universally_unique_identifier\n[ulid]: https://github.com/ulid/spec\n[ksuid]: https://github.com/segmentio/ksuid\n\n## Command-line interface\n\n`scru160` generates SCRU-160 IDs.\n\n```bash\n$ scru160\n05U0G9S45SUOL4C8FNQFKQ5M6VEROV9J\n$ scru160 -f\n017c08279e9f4e32b6f58d023b9fc41a22302750\n$ scru160 -n 4\n05U0G9TQQ8FONQQCC655GMBTBBHUIKK7\n05U0G9TQQ8FOOJ7IR79Q6QFJ3OSNRF92\n05U0G9TQQ8FORTQU0K5OOSANILGP72HO\n05U0G9TQQ8FOTV6SEJVMV6OJQDP15MHC\n```\n\n`scru160-inspect` prints the components of given SCRU-160 IDs as human- and\nmachine-readable JSON objects.\n\n```bash\n$ scru160 -fn 2 | scru160-inspect\n{\n  "input":        "017c083c130732153679e83c4fc65664e6a964a1",\n  "canonical":    "05U0GF0J0SP1ADJPT0U4VHIMCJJAIP51",\n  "timestamputc": "2021-09-21 12:02:07.239+00:00",\n  "timestamp":    "1632225727239",\n  "counter":      "12821",\n  "random16":     "13945",\n  "random80":     "1096701577047146014270625",\n  "hexfields":    ["017c083c1307", "3215", "3679", "e83c4fc65664e6a964a1"]\n}\n{\n  "input":        "017c083c13073216a2ab5d302cebfca0916625a0",\n  "canonical":    "05U0GF0J0SP1D8LBBKO2PQVSK28MC9D0",\n  "timestamputc": "2021-09-21 12:02:07.239+00:00",\n  "timestamp":    "1632225727239",\n  "counter":      "12822",\n  "random16":     "41643",\n  "random80":     "440068763580938823542176",\n  "hexfields":    ["017c083c1307", "3216", "a2ab", "5d302cebfca0916625a0"]\n}\n```\n\n## License\n\nCopyright 2021 LiosK\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use\nthis file except in compliance with the License. You may obtain a copy of the\nLicense at\n\nhttp://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software distributed\nunder the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied. See the License for the\nspecific language governing permissions and limitations under the License.\n',
    'author': 'LiosK',
    'author_email': 'contact@mail.liosk.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scru160/python',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7.12,<4.0.0',
}


setup(**setup_kwargs)
