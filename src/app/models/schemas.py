from pydantic import BaseModel, Field
from typing import List

class Author(BaseModel):
    name: str = Field(..., description="Author's name")

class Paper(BaseModel):
    title: str = Field(..., description="Paper title")
    authors: List[Author] = Field(..., description="List of authors")
    summary: str = Field(..., description="Paper abstract")
    published: str = Field(..., description="Publication date")
    link: str = Field(..., description="Paper URL")

class SearchResponse(BaseModel):
    total_results: int = Field(..., description="Total number of results")
    papers: List[Paper] = Field(..., description="List of papers")