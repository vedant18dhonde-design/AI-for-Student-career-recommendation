"""Standardized API response helpers."""

from typing import Any, Dict, List, Optional

from fastapi.responses import JSONResponse


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
    meta: Optional[Dict] = None,
) -> JSONResponse:
    body: Dict[str, Any] = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    if meta:
        body["meta"] = meta
    return JSONResponse(status_code=status_code, content=body)


def error_response(
    message: str = "An error occurred",
    status_code: int = 400,
    errors: Optional[Any] = None,
) -> JSONResponse:
    body: Dict[str, Any] = {"success": False, "message": message}
    if errors is not None:
        body["errors"] = errors
    return JSONResponse(status_code=status_code, content=body)


def created_response(data: Any = None, message: str = "Created successfully") -> JSONResponse:
    return success_response(data=data, message=message, status_code=201)


def paginated_response(
    data: List[Any],
    total: int,
    page: int,
    page_size: int,
    message: str = "Success",
) -> JSONResponse:
    total_pages = max(1, -(-total // page_size))  # ceiling division
    meta = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
    return success_response(data=data, message=message, meta=meta)
