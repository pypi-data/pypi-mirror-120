# ORCID2Markdown

Introduction
============
---
ORCID2Markdown is a small tool for automatically parsing an ORCID _works_ entry into a Markdown format appropriate for
use in static website generators like Jekyll.\
The output format is the following:

```markdown

# First Author Papers
---
* _Title_: {title}
* _Authors_: **{first_author}**, {secondary_authors}
* _Journal_: {journal}
* _Date_: {year} / {month}
* _Volume_: {volume}
* https://doi.org/{doi}
---
# Co Author Papers
---
* _Title_: {title}
* _Authors_: {authors}... **{your_name}**... {authors}
* _Journal_: {journal}
* _Date_: {year} / {month}
* _Volume_: {volume}
* https://doi.org/{doi}
```

Issues
======
ORCID2Markdown uses biblatexparser to parse bibentries obtained from
querying Crossref for a bibentry using _habanero_. This leads to LaTeX-style formatted text to be totally lost.
Therefore, LaTeX-styled text needs to be fixed _manually_.

Installation
=====
```bash
pip install orcid2markdown
```

Usage
====
Using is simple:
```python
from orcid2markdown import ORCID2Markdown
oid = ORCID2Markdown(orcid="your_orcid",
                     first_name="your first name",
                     other_names=["a list of", "possible", "other names you have as author"])
oid.to_markdown("my_papers.md")
```
> :warning: Note: Depending on the number of works, it might take a while. I tested in a around 340 works orcid, and it tooks roughly 5 minutes.