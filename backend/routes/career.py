from fastapi import APIRouter

from ..schema import Career
from ..utils import recommend

router = APIRouter()


@router.post("/recommend-career")
def recommend_career(student: Career):
    careers = recommend(student.field_studied)
    return {"Recommended Careers": careers}