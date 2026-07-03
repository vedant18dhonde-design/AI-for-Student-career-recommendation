"""Pagination, sorting, and filtering helpers."""

from typing import Any, Dict, List, Optional, Tuple

from fastapi import Query


class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1, description="Page number"),
        page_size: int = Query(default=10, ge=1, le=100, description="Items per page"),
        sort_by: str = Query(default="created_at", description="Sort field"),
        sort_order: str = Query(default="desc", description="Sort direction: asc or desc"),
        search: Optional[str] = Query(default=None, description="Search query"),
    ):
        self.page = page
        self.page_size = page_size
        self.sort_by = sort_by
        self.sort_order = 1 if sort_order.lower() == "asc" else -1
        self.search = search

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size

    @property
    def sort_spec(self) -> List[Tuple[str, int]]:
        return [(self.sort_by, self.sort_order)]


def build_search_filter(search: Optional[str], fields: List[str]) -> Dict:
    """Build a MongoDB regex search filter across multiple fields."""
    if not search:
        return {}
    regex = {"$regex": search, "$options": "i"}
    return {"$or": [{field: regex} for field in fields]}
