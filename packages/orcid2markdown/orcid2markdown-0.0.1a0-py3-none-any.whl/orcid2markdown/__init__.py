import requests
import bibtexparser
from typing import List, Tuple, Dict, Union
from collections import defaultdict
from habanero import cn
from dataclasses import dataclass
from tqdm import tqdm


@dataclass
class ORCID2Markdown:
    orcid: str
    first_name: str
    other_names: List[str]
    _headers = {"Content-type": "application/json"}
    MARKDOWN_TEMPLATE = """
* _Title_: {title}
* _Authors_: {authors}
* _Journal_: {journal}
* _Date_: {year} / {month}
* _Volume_: {volume}
* [DOI](https://doi.org/{doi})

"""

    def _match_name(self, author: str) -> bool:
        """
        Attempts to match first / other_names with a given author name.
        Warning: This method is not really smart.
        Args:
            author (str): A given author name

        Returns:
        bool
            True if finds a match False otherwise
        """
        if self.first_name in author:
            return True
        else:
            return any([name in author for name in self.other_names])

    @property
    def _orcid_works(self) -> Dict:
        """
        Query ORCID API for the _work_ sections
        Returns:
            A list of dicts containing an entry for each work.

        """
        # print(f"Obtaning work data from ORCID: {self.orcid} ")
        _ORCID_URL = f"https://pub.orcid.org/v3.0/{self.orcid}/works"
        return requests.get(_ORCID_URL, headers=self._headers).json()

    @property
    def _works_dois(self) -> List[str]:
        """
        Get Document Object Identifier (DOI) from the a works response.
        Returns:
            A list of strings with each paper associated DOI

        """
        # print("Parsing work data into DOIs...")
        works = self._orcid_works
        dois = []
        for entry in works["group"]:
            eid = entry["external-ids"]
            doi = self._get_doi_from_eids(eid)
            if doi == -1:
                print(f"Failed to get DOI for {entry['work-summary'][0]['path']}")
            else:
                dois.append(doi)
        return dois

    @property
    def _bibtex_entries(self) -> List[defaultdict]:
        """
        Get a dictionary representation of Bibtex entries from each DOI
        Returns:
            A list of dictionaries containing each bibtex.
        """
        parsed = []
        print("Obtaining bibtex entries for each DOI in ORCID at Crossref...")
        # Obtain entries as defaultdict
        for doi in tqdm(self._works_dois):
            bib = self._get_bibentry_from_doi(doi)
            if bib != -1:
                parsed.append(defaultdict(lambda: "N.A", bibtexparser.loads(bib).entries[0]))
        return parsed

    @property
    def _auth_list(self) -> Tuple[List[defaultdict], List[defaultdict]]:
        """
        Tuple containing two lists:
            - First list is a list where the the first author is same as `self.first_name`
            - Second list is a list where we are co-authors.
        Returns:
        Tuple
            Returns a tuple with two lists.
        """
        first_author = []
        co_author = []
        for bibentry in self._bibtex_entries:
            # Bib have authors seperated by `and`. Split and get first.
            authors = bibentry['author'].split("and")
            first_auth = authors[0]
            # Try to match name
            if self._match_name(first_auth):
                new_auth = f"**{first_auth.strip()}**"
                if len(authors) > 1:
                    new_auth += ","
                for i, auth in enumerate(authors[1:]):
                    auth.strip()
                    if i == len(authors[1:]) - 1 and len(authors) > 1:
                        new_auth += f"and {auth}"
                    else:
                        new_auth += f"{auth},"
                # Save new name.
                bibentry['author'] = new_auth
                first_author.append(bibentry)
            else:
                new_auth = ""
                for i, auth in enumerate(authors):
                    # Remove whitespaces.
                    auth = auth.strip()
                    if self._match_name(auth):
                        # We matched our name so lets make it bold
                        auth = f"**{auth}**"
                    # Use `and` to gather together.
                    if i == len(authors) - 1:
                        new_auth += f"and {auth}"
                    else:
                        new_auth += f"{auth}, "
                bibentry['author'] = new_auth
                co_author.append(bibentry)
        return first_author, co_author

    def _get_doi_from_eids(self, eids: Dict) -> Union[str, int]:
        """gets doi from external id dict

        Parameters
        ----------
        eids : dict
            a 'external-ids' dict from orcid

        Returns
        -------
        str
            a doi id hopefully
        """
        eid = eids['external-id']
        for entry in eid:
            if entry['external-id-type'] == "doi":
                return entry['external-id-value']
            else:
                continue
        # Returns -1 if failed
        return -1

    def _get_bibentry_from_doi(self, doi: str) -> Union[int, str]:
        """
        Gets bibenty from DOI
        Returns:
            A str representation of the bibentry for given doi
        """
        try:
            return cn.content_negotiation(ids=doi, format="bibtex")
        except:
            print(f"Failed to get bibtex entry for {doi}")
            return -1

    def to_markdown(self, filename: str) -> str:
        """
        Saves ORCId to a markdown file
        Args:
            filename (str): path to filename

        Returns:
        str
            Also return the markdown string representation.
        """
        # Get first and coauthor paper information
        first, co = self._auth_list
        filedata = "**Note:** Page automatically generated with ORCID2Markdown.\n{: .notice--warning}"
        filedata += "\n# First Author \n ---"
        # Go thru first author first.
        for dic in first:
            _append = self.MARKDOWN_TEMPLATE.format(title=dic['title'].replace("\n", "").replace("\t", ""),
                                                    authors=dic['author'],
                                                    journal=dic['journal'],
                                                    year=dic['year'],
                                                    month=dic['month'],
                                                    volume=dic['volume'],
                                                    doi=dic['doi'])
            filedata += _append
            if dic != first[-1]:
                filedata += "---"

        filedata += "# Co-Author \n ---"
        for dic in co:
            _append = self.MARKDOWN_TEMPLATE.format(title=dic['title'].replace("\n", "").replace("\t", ""),
                                                    authors=dic['author'],
                                                    journal=dic['journal'],
                                                    year=dic['year'],
                                                    month=dic['month'],
                                                    volume=dic['volume'],
                                                    doi=dic['doi'])
            filedata += _append
            filedata += "---"
        # Save into file
        with open(filename, "w") as f:
            f.write(filedata)
        return filedata
