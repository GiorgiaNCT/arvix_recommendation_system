from fastapi import APIRouter, Query
from typing import Optional
from app.services.arxiv import ArxivService
from app.models.schemas import SearchResponse

router = APIRouter()

@router.get("/search/", response_model=SearchResponse)
async def search_papers(
    query: str = Query(..., description="Search query for arXiv papers"),
    max_results: Optional[int] = Query(100, description="Maximum number of results to return"),
    start: Optional[int] = Query(0, description="Starting index for pagination"),
    sort_by: Optional[str] = Query('lastUpdatedDate', description="Sort by field"),
    sort_order: Optional[str] = Query('descending', description="Sort order")
) -> SearchResponse:
    papers = ArxivService.fetch_papers(query, max_results, start, sort_by, sort_order)
    return SearchResponse(total_results=len(papers), papers=papers)

@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "arxiv-api"}