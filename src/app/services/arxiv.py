from typing import List, Dict, Any
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from fastapi import HTTPException

class ArxivService:
    BASE_URL = 'http://export.arxiv.org/api/query?'
    
    @staticmethod
    def fetch_papers(
        search_query: str, 
        max_results: int = 100, 
        start: int = 0, 
        sort_by: str = 'lastUpdatedDate', 
        sort_order: str = 'descending'
    ) -> List[Dict[str, Any]]:
        try:
            url = ArxivService._build_url(search_query, max_results, start, sort_by, sort_order)
            return ArxivService._fetch_and_parse(url)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ArXiv API error: {str(e)}")

    @staticmethod
    def _build_url(search_query: str, max_results: int, start: int, sort_by: str, sort_order: str) -> str:
        query_params = {
            'search_query': search_query.replace('+', ' '),
            'start': start,
            'max_results': max_results,
            'sortBy': sort_by,
            'sortOrder': sort_order
        }
        return ArxivService.BASE_URL + urllib.parse.urlencode(query_params)

    @staticmethod
    def _fetch_and_parse(url: str) -> List[Dict[str, Any]]:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        return ArxivService._parse_response(data)

    @staticmethod
    def _parse_response(data: str) -> List[Dict[str, Any]]:
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