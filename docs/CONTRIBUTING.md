# Contributing

For contributing, keep the following things in mind:

## Coding & Github etiquette

### Code
1. Please write in PEP-8 (auto-formatter <3)
2. Please use type-hinting as much as possible
3. Preferable to use a one-line doc-string to document a function
4. Please use the __ prefix to indicate private variables.
5. Please use the following import order:
```python
import a_standard
import b_standard

import a_third_party
import b_third_party

from a_soc import f
from a_soc import g
from b_soc import d
```
[source] (https://stackoverflow.com/a/20763446)
### Github
1. Think of a commit message as "This commit I will []", e.g. git commit -m "add README.md"
2. add co-authors when working together (pair - programming)!

#### Alias:
```git config --global alias.commit-db "commit --trailer 'Co-authored-by: hujanbiru <pangilon@protonmail.com>' --trailer 'Co-authored-by: OlivierBroekman <olivier.broekman@ru.nl>'"```
