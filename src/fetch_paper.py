import urllib, urllib.request
import xml.etree.ElementTree as ET

def fetch_arxiv_papers(search_query, max_results=100, start=0, sort_by='lastUpdatedDate', sort_order='descending'):
    # Construct the URL with parameters
    base_url = 'http://export.arxiv.org/api/query?'
    query_params = {
        'search_query': search_query,
        'start': start,
        'max_results': max_results,
        'sortBy': sort_by,
        'sortOrder': sort_order
    }
    
    # Create the full URL
    url = base_url + urllib.parse.urlencode(query_params)
    
    # Fetch the data
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
    
    # Parse XML response
    root = ET.fromstring(data)
    
    # Extract papers information
    papers = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        paper = {
            'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
            'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
            'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
            'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
            'link': entry.find('{http://www.w3.org/2005/Atom}id').text
        }
        papers.append(paper)
    
    return papers

# Example usage
if __name__ == "__main__":
    # Search for AI papers
    ai_papers = fetch_arxiv_papers('cat:cs.AI')
    
    # Search for deep learning papers
    dl_papers = fetch_arxiv_papers('cat:cs.LG')
    
    # Print results
    print("=== AI Papers ===")
    for i, paper in enumerate(ai_papers[:5], 1):  # Print first 5 papers
        print(f"\n{i}. {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Published: {paper['published']}")
        print(f"Link: {paper['link']}")
        print("-" * 80)
    
    print("\n=== Machine Learning Papers ===")
    for i, paper in enumerate(dl_papers[:5], 1):  # Print first 5 papers
        print(f"\n{i}. {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Published: {paper['published']}")
        print(f"Link: {paper['link']}")
        print("-" * 80)