from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import urllib, urllib.request
import xml.etree.ElementTree as ET
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="arXiv Paper Search API",
    description="API to search for academic papers on arXiv",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define response models
class Author(BaseModel):
    name: str

class Paper(BaseModel):
    title: str
    authors: List[Author]
    summary: str
    published: str
    link: str

class SearchResponse(BaseModel):
    total_results: int
    papers: List[Paper]

def fetch_arxiv_papers(search_query: str, max_results: int = 100, start: int = 0, 
                      sort_by: str = 'lastUpdatedDate', sort_order: str = 'descending'):
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = search_query.replace('+', ' ')
    
    query_params = {
        'search_query': search_query,
        'start': start,
        'max_results': max_results,
        'sortBy': sort_by,
        'sortOrder': sort_order
    }
    
    url = base_url + urllib.parse.urlencode(query_params)
    
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            
        root = ET.fromstring(data)
        papers = []
        
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            paper = {
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text.strip(),
                'authors': [{'name': author.find('{http://www.w3.org/2005/Atom}name').text} 
                          for author in entry.findall('{http://www.w3.org/2005/Atom}author')],
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text.strip(),
                'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                'link': entry.find('{http://www.w3.org/2005/Atom}id').text
            }
            papers.append(paper)
        
        return papers
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search/", response_model=SearchResponse)
async def search_papers(
    query: str = Query(..., description="Search query for arXiv papers"),
    max_results: Optional[int] = Query(100, description="Maximum number of results to return"),
    start: Optional[int] = Query(0, description="Starting index for pagination"),
    sort_by: Optional[str] = Query('lastUpdatedDate', description="Sort by field"),
    sort_order: Optional[str] = Query('descending', description="Sort order")
):
    """
    Search for papers on arXiv.
    
    Example queries:
    - cat:cs.AI (Category-based search for AI)
    - ti:"artificial intelligence" (Title-based search)
    - all:"machine learning" (Search in all fields)
    """
    papers = fetch_arxiv_papers(query, max_results, start, sort_by, sort_order)
    return SearchResponse(total_results=len(papers), papers=papers)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)