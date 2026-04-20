import requests
import xml.etree.ElementTree as ET
from config import ARXIV_API_URL, MAX_RESULTS


class RetrievalAgent:
    def expand_query(self, base_query):
        # Currently just returns the original query
        # This is a placeholder for future improvements (e.g. query expansion)
        return [base_query]

    def fetch(self, query):
        # Build the arXiv API request URL using the query
        url = (
            f"{ARXIV_API_URL}"
            f"?search_query=all:{query}"
            f"&start=0&max_results={MAX_RESULTS}"
        )

        # ----------------------------
        # MAKE HTTP REQUEST
        # ----------------------------
        try:
            # Send GET request with a timeout (prevents hanging forever)
            response = requests.get(url, timeout=15)

            # Raise an error if status code is not 200 (OK)
            response.raise_for_status()
        except requests.RequestException as e:
            # Handle network errors, timeouts, bad responses, etc.
            print(f"[Retrieval] Request failed: {e}")
            return []

        # ----------------------------
        # PARSE XML RESPONSE
        # ----------------------------
        try:
            # Convert raw XML response into an ElementTree object
            root = ET.fromstring(response.content)
        except ET.ParseError:
            # Handle malformed XML
            print("[Retrieval] XML parsing failed")
            return []

        # Define XML namespaces used by arXiv API
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom"
        }

        # Store extracted papers
        papers = []

        # ----------------------------
        # EXTRACT DATA FROM XML
        # ----------------------------
        for entry in root.findall("atom:entry", ns):
            try:
                # Extract relevant fields from each entry
                title = entry.find("atom:title", ns)
                published = entry.find("atom:published", ns)
                doi = entry.find("arxiv:doi", ns)

                # Clean and validate extracted text
                title = title.text.strip() if title is not None and title.text else ""
                published = published.text.strip() if published is not None and published.text else ""

                # Extract year from published date (first 4 characters)
                year = published[:4] if len(published) >= 4 else None

                # Clean DOI if present
                doi = doi.text.strip() if doi is not None and doi.text else None

                # Extract list of authors
                authors = []
                for a in entry.findall("atom:author", ns):
                    name = a.find("atom:name", ns)
                    if name is not None and name.text:
                        authors.append(name.text.strip())

                # Only include papers that have a valid title
                if title:
                    papers.append({
                        "title": title,
                        "authors": authors,
                        "year": year,
                        "doi": doi
                    })

            except Exception:
                # Skip any entry that causes unexpected errors
                continue

        # Return list of extracted papers
        return papers