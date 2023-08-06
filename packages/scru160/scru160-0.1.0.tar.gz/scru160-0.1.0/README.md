# SCRU-160: Sortable, Clock and Random number-based Unique identifier

SCRU-160 ID is yet another attempt to supersede [UUID] in the use cases that
need decentralized, globally unique time-ordered identifiers. SCRU-160 is
inspired by [ULID] and [KSUID] and has the following features:

- 160-bit length
- Sortable by generation time (in binary and in text)
- Two case-insensitive encodings: 32-character base32hex and 40-character hex
- More than 32,768 unique, time-ordered but unpredictable IDs per millisecond
- Nearly 111-bit randomness for collision resistance

```python
from scru160 import scru160, scru160f

print(scru160())  # e.g. "05TVFQQ8UGDNKHDJ79AEGPHU7QP7996H"
print(scru160())  # e.g. "05TVFQQ8UGDNNVCCNUH0Q8JDD3IPHB8R"

print(scru160f())  # e.g. "017bf7eb48f41b7d6bd295bc5adc43436bc969df"
print(scru160f())  # e.g. "017bf7eb48f41b7e1bc98aec348dfa1539b41288"
```

[uuid]: https://en.wikipedia.org/wiki/Universally_unique_identifier
[ulid]: https://github.com/ulid/spec
[ksuid]: https://github.com/segmentio/ksuid

## License

Copyright 2021 LiosK

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
