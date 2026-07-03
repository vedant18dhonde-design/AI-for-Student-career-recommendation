from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

payload = {
    "age": 22,
    "gender": "female",
    "field_studied": "Computer Science",
    "university_GPA": 3.6,
    "Internships_completed": 1,
    "Projects_completed": 2,
    "Certifications": 1,
    "Soft_Skills_score": 4.0,
    "Networking_score": 3.5,
    "Interests": "AI and development"
}

resp = client.post('/recommend-career', json=payload)
print('status', resp.status_code)
print('json', resp.json())
