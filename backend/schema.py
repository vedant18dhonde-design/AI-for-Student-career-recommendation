from pydantic import BaseModel
class Career(BaseModel):
    age: int
    gender:str
    field_studied :str
    university_GPA: float
    Internships_completed: int
    Projects_completed: int
    Certifications : int
    Soft_Skills_score : float
    Networking_score : float
    Interests : str
    

