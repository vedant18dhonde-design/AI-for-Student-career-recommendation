career_map = {
    "computer science": [
        "Software Engineer",
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Engineer",
    ],
    "information technology": ["Backend Developer", "Cloud Engineer", "DevOps Engineer"],
    "electronics": ["Embedded Systems Engineer", "IoT Engineer", "Robotics Engineer"],
    "mechanical": ["CAD Designer", "Automobile Engineer", "Manufacturing Engineer"],
    "civil": ["Structural Engineer", "Construction Manager", "Urban Planner"],
}


def recommend(field: str):
    if not field:
        return ["Software Engineer"]
    key = field.strip().lower()
    return career_map.get(key, ["Software Engineer"])