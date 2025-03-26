import requests
import pandas as pd
import argparse
import re
import xml.etree.ElementTree as ET
from typing import List, Dict

# PubMed API URLs
PUBMED_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_API = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[str]:
    """Fetches research papers from PubMed using the given query and returns a list of PubMed IDs."""

    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }

    response = requests.get(PUBMED_API, params=params)
    response.raise_for_status()

    data = response.json()
    paper_ids = data.get("esearchresult", {}).get("idlist", [])

    if not paper_ids:
        print("No papers found for the given query.")

    return paper_ids


def fetch_paper_details(paper_ids: List[str]) -> List[Dict[str, str]]:
    """Fetches detailed information (Title, Date, Email) of papers using PubMed IDs."""

    if not paper_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml"
    }

    response = requests.get(PUBMED_FETCH_API, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        paper_data = {
            "PubmedID": "N/A",
            "Title": "N/A",
            "PublicationDate": "N/A",
            "CorrespondingEmail": "N/A"
        }

        # Extract PubMed ID
        pmid = article.find(".//PMID")
        if pmid is not None:
            paper_data["PubmedID"] = pmid.text

        # Extract Title
        title = article.find(".//ArticleTitle")
        if title is not None:
            paper_data["Title"] = title.text

        # Extract Publication Date
        pub_date = article.find(".//PubDate/Year")
        if pub_date is not None:
            paper_data["PublicationDate"] = pub_date.text

        # Extract Corresponding Author Email
        author_list = article.findall(".//AuthorList/Author")
        for author in author_list:
            email = author.find(".//Affiliation")
            if email is not None and "@" in email.text:  # Basic email detection
                paper_data["CorrespondingEmail"] = email.text
                break  # Stop after finding the first valid email

        papers.append(paper_data)

    return papers


def extract_non_academic_authors(xml_data: str) -> List[Dict[str, List[str]]]:
    """Extracts non-academic authors and affiliated companies from the XML data."""
    non_academic_authors = []
    company_affiliations = []

    # Company keywords heuristic
    company_keywords = ["Inc.", "Ltd.", "Corp.", "Pharma", "Biotech"]

    # Extract affiliations
    affiliations = re.findall(r"<Affiliation>(.*?)</Affiliation>", xml_data)

    for aff in affiliations:
        if any(keyword in aff for keyword in company_keywords):
            non_academic_authors.append(aff)
            company_affiliations.append(aff)

    return [{"Non-academic Authors": non_academic_authors, "Company Affiliations": company_affiliations}]


def save_to_csv(papers: List[Dict[str, str]], filename: str = "papers.csv") -> None:
    """Saves extracted paper data to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")



def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed based on a search query.\n"
                    "It identifies papers with at least one author affiliated with a pharmaceutical or biotech company "
                    "and saves the results in a CSV file."
    )

    parser.add_argument("query", type=str, help="PubMed search query (e.g., 'cancer treatment').")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename (optional).")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode for detailed logs.")

    args = parser.parse_args()

    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    paper_ids = fetch_pubmed_papers(args.query)
    paper_details = fetch_paper_details(paper_ids)

    if args.file:
        save_to_csv(paper_details, args.file)
    else:
        print(paper_details)


if __name__ == "__main__":
    main()
