"""Recommendations service — courses, jobs, internships, skill gap, learning roadmap."""

from typing import Any, Dict, List, Optional


# ── Knowledge Base ────────────────────────────────────────────────────────────

COURSES_DB = {
    "Python": [
        {"name": "Python for Everybody", "platform": "Coursera", "url": "https://coursera.org/learn/python", "level": "Beginner", "duration": "8 weeks", "free": True},
        {"name": "Complete Python Bootcamp", "platform": "Udemy", "url": "https://udemy.com/course/complete-python-bootcamp", "level": "Beginner", "duration": "22 hours", "free": False},
    ],
    "Machine Learning": [
        {"name": "Machine Learning Specialization", "platform": "Coursera", "url": "https://coursera.org/specializations/machine-learning-introduction", "level": "Intermediate", "duration": "3 months", "free": False},
        {"name": "Fast.ai Practical Deep Learning", "platform": "fast.ai", "url": "https://fast.ai", "level": "Intermediate", "duration": "Self-paced", "free": True},
    ],
    "Data Science": [
        {"name": "IBM Data Science Professional Certificate", "platform": "Coursera", "url": "https://coursera.org/professional-certificates/ibm-data-science", "level": "Beginner", "duration": "4 months", "free": False},
        {"name": "Data Science with Python", "platform": "edX", "url": "https://edx.org/course/data-science-with-python", "level": "Intermediate", "duration": "6 weeks", "free": True},
    ],
    "React": [
        {"name": "The Complete React Guide", "platform": "Udemy", "url": "https://udemy.com/course/react-the-complete-guide-incl-redux", "level": "Intermediate", "duration": "40 hours", "free": False},
        {"name": "React Tutorial", "platform": "freeCodeCamp", "url": "https://freecodecamp.org", "level": "Beginner", "duration": "Self-paced", "free": True},
    ],
    "SQL": [
        {"name": "SQL for Data Science", "platform": "Coursera", "url": "https://coursera.org/learn/sql-for-data-science", "level": "Beginner", "duration": "4 weeks", "free": False},
        {"name": "SQLZoo", "platform": "SQLZoo", "url": "https://sqlzoo.net", "level": "Beginner", "duration": "Self-paced", "free": True},
    ],
    "AWS": [
        {"name": "AWS Cloud Practitioner Essentials", "platform": "AWS", "url": "https://aws.amazon.com/training", "level": "Beginner", "duration": "6 hours", "free": False},
    ],
    "TensorFlow": [
        {"name": "TensorFlow Developer Certificate", "platform": "Coursera", "url": "https://coursera.org/professional-certificates/tensorflow-in-practice", "level": "Intermediate", "duration": "4 months", "free": False},
    ],
    "Communication": [
        {"name": "Communication Skills for Engineers", "platform": "Coursera", "url": "https://coursera.org/learn/engineering-project-management-communication", "level": "Beginner", "duration": "3 weeks", "free": False},
    ],
    "Cybersecurity": [
        {"name": "Google Cybersecurity Certificate", "platform": "Coursera", "url": "https://coursera.org/professional-certificates/google-cybersecurity", "level": "Beginner", "duration": "6 months", "free": False},
    ],
}

JOBS_DB = {
    "Software Engineer": [
        {"company": "Google", "role": "Software Engineer", "location": "Mountain View, CA", "type": "Full-time", "url": "https://careers.google.com", "salary_range": "$120k-$200k"},
        {"company": "Microsoft", "role": "Software Development Engineer", "location": "Redmond, WA", "type": "Full-time", "url": "https://careers.microsoft.com", "salary_range": "$110k-$180k"},
        {"company": "Amazon", "role": "SDE I", "location": "Seattle, WA", "type": "Full-time", "url": "https://amazon.jobs", "salary_range": "$100k-$160k"},
    ],
    "Data Scientist": [
        {"company": "Netflix", "role": "Data Scientist", "location": "Los Gatos, CA", "type": "Full-time", "url": "https://jobs.netflix.com", "salary_range": "$130k-$220k"},
        {"company": "Meta", "role": "Research Scientist", "location": "Menlo Park, CA", "type": "Full-time", "url": "https://metacareers.com", "salary_range": "$140k-$250k"},
    ],
    "Machine Learning Engineer": [
        {"company": "OpenAI", "role": "ML Engineer", "location": "San Francisco, CA", "type": "Full-time", "url": "https://openai.com/careers", "salary_range": "$150k-$300k"},
        {"company": "DeepMind", "role": "Research Engineer", "location": "London, UK", "type": "Full-time", "url": "https://deepmind.com/careers", "salary_range": "£80k-£160k"},
    ],
    "default": [
        {"company": "Various Tech Companies", "role": "Entry Level Developer", "location": "Remote", "type": "Full-time", "url": "https://linkedin.com/jobs", "salary_range": "$60k-$120k"},
        {"company": "Startups", "role": "Full Stack Developer", "location": "Remote", "type": "Full-time", "url": "https://angel.co/jobs", "salary_range": "$70k-$130k"},
    ],
}

INTERNSHIPS_DB = [
    {"company": "Google", "role": "STEP Intern", "location": "Mountain View, CA", "duration": "12 weeks", "url": "https://careers.google.com/students", "stipend": "$8,000/month"},
    {"company": "Microsoft", "role": "SWE Intern", "location": "Redmond, WA", "duration": "12 weeks", "url": "https://careers.microsoft.com/students", "stipend": "$7,000/month"},
    {"company": "Amazon", "role": "SDE Intern", "location": "Seattle, WA", "duration": "12 weeks", "url": "https://amazon.jobs/students", "stipend": "$7,500/month"},
    {"company": "Meta", "role": "Software Engineer Intern", "location": "Menlo Park, CA", "duration": "12 weeks", "url": "https://metacareers.com/students", "stipend": "$9,000/month"},
    {"company": "Apple", "role": "Software Engineer Intern", "location": "Cupertino, CA", "duration": "12 weeks", "url": "https://apple.com/jobs/students", "stipend": "$8,500/month"},
    {"company": "Tesla", "role": "Data Science Intern", "location": "Palo Alto, CA", "duration": "16 weeks", "url": "https://tesla.com/careers", "stipend": "$6,000/month"},
    {"company": "LinkedIn", "role": "Backend Intern", "location": "Sunnyvale, CA", "duration": "12 weeks", "url": "https://careers.linkedin.com", "stipend": "$7,000/month"},
    {"company": "Spotify", "role": "ML Engineer Intern", "location": "New York, NY", "duration": "12 weeks", "url": "https://spotify.com/jobs", "stipend": "$7,500/month"},
]

COMPANIES_DB = [
    {"name": "Google", "industry": "Technology", "size": "100,000+", "rating": 4.4, "url": "https://careers.google.com", "perks": ["Free meals", "Health insurance", "Stock options", "Learning budget"]},
    {"name": "Microsoft", "industry": "Technology", "size": "100,000+", "rating": 4.2, "url": "https://careers.microsoft.com", "perks": ["Remote work", "Health insurance", "Stock options", "401k"]},
    {"name": "Amazon", "industry": "E-commerce/Cloud", "size": "100,000+", "rating": 3.8, "url": "https://amazon.jobs", "perks": ["Stock options", "Relocation", "Health insurance"]},
    {"name": "Meta", "industry": "Social Media/AI", "size": "70,000+", "rating": 4.0, "url": "https://metacareers.com", "perks": ["Free meals", "Stock options", "Health insurance", "Gym"]},
    {"name": "Apple", "industry": "Technology", "size": "100,000+", "rating": 4.3, "url": "https://apple.com/jobs", "perks": ["Product discounts", "Health insurance", "Stock options"]},
    {"name": "Netflix", "industry": "Entertainment/Streaming", "size": "10,000+", "rating": 4.1, "url": "https://jobs.netflix.com", "perks": ["Unlimited PTO", "High salaries", "Stock options"]},
    {"name": "Salesforce", "industry": "CRM/SaaS", "size": "70,000+", "rating": 4.2, "url": "https://salesforce.com/careers", "perks": ["Volunteer days", "Health insurance", "Stock options"]},
    {"name": "Stripe", "industry": "FinTech", "size": "7,000+", "rating": 4.5, "url": "https://stripe.com/jobs", "perks": ["Remote work", "Stipends", "High salaries"]},
]

SKILLS_TREE = {
    "Software Engineer": {
        "core": ["Data Structures", "Algorithms", "System Design", "OOP"],
        "technical": ["Python/Java/C++", "REST APIs", "Git", "SQL"],
        "soft": ["Problem Solving", "Communication", "Teamwork"],
    },
    "Data Scientist": {
        "core": ["Statistics", "Machine Learning", "Data Analysis", "Visualization"],
        "technical": ["Python", "R", "SQL", "TensorFlow/PyTorch", "Tableau"],
        "soft": ["Critical Thinking", "Storytelling with Data", "Communication"],
    },
    "Machine Learning Engineer": {
        "core": ["Machine Learning", "Deep Learning", "MLOps", "Mathematics"],
        "technical": ["Python", "TensorFlow", "PyTorch", "Docker", "Cloud ML"],
        "soft": ["Research Skills", "Problem Solving", "Collaboration"],
    },
    "default": {
        "core": ["Programming", "Problem Solving", "Mathematics"],
        "technical": ["Python", "Git", "SQL"],
        "soft": ["Communication", "Teamwork", "Time Management"],
    },
}


class RecommendationsService:

    def get_courses(self, career: str, skills: List[str] = None) -> List[dict]:
        courses = []
        skills = skills or SKILLS_TREE.get(career, SKILLS_TREE["default"])["technical"]
        for skill in skills[:5]:
            for key in COURSES_DB:
                if key.lower() in skill.lower() or skill.lower() in key.lower():
                    courses.extend(COURSES_DB[key])
                    break
        # Deduplicate
        seen = set()
        unique = []
        for c in courses:
            if c["name"] not in seen:
                seen.add(c["name"])
                unique.append(c)
        return unique[:8]

    def get_jobs(self, career: str) -> List[dict]:
        return JOBS_DB.get(career, JOBS_DB["default"])

    def get_internships(self, career: str = None, field: str = None) -> List[dict]:
        return INTERNSHIPS_DB[:6]

    def get_companies(self, career: str = None) -> List[dict]:
        return COMPANIES_DB[:8]

    def get_skill_gap(self, career: str, student_skills: List[str]) -> dict:
        target_skills = SKILLS_TREE.get(career, SKILLS_TREE["default"])
        all_required = (
            target_skills["core"] + target_skills["technical"] + target_skills["soft"]
        )
        student_lower = [s.lower() for s in student_skills]
        missing = [s for s in all_required if s.lower() not in student_lower]
        matched = [s for s in all_required if s.lower() in student_lower]

        coverage = round(len(matched) / len(all_required) * 100, 1) if all_required else 0
        return {
            "career": career,
            "required_skills": all_required,
            "matched_skills": matched,
            "missing_skills": missing,
            "skill_coverage_percent": coverage,
            "priority_courses": self.get_courses(career, missing[:3]),
        }

    def get_learning_roadmap(self, career: str, gpa: float, internships: int, placement_prob: float) -> dict:
        skills = SKILLS_TREE.get(career, SKILLS_TREE["default"])
        phase1 = {"phase": "Foundation (Month 1-2)", "tasks": skills["core"][:3], "resources": self.get_courses(career)[:2]}
        phase2 = {"phase": "Technical Skills (Month 3-4)", "tasks": skills["technical"][:4], "resources": self.get_courses(career)[2:4]}
        phase3 = {"phase": "Projects & Portfolio (Month 5-6)", "tasks": ["Build 2 projects", "Contribute to open source", "Create GitHub portfolio"], "resources": []}
        phase4 = {"phase": "Job Ready (Month 7-8)", "tasks": ["Apply to internships", "Practice LeetCode", "Network on LinkedIn", "Prep for interviews"], "resources": []}

        urgency = "high" if placement_prob < 50 else "medium" if placement_prob < 75 else "low"
        return {
            "career_goal": career,
            "current_readiness": f"{placement_prob:.0f}%",
            "urgency": urgency,
            "total_duration": "8 months",
            "phases": [phase1, phase2, phase3, phase4],
            "internship_targets": self.get_internships()[:3],
            "certifications": [
                {"name": f"{career} Professional Certificate", "platform": "Coursera"},
                {"name": "AWS Cloud Practitioner", "platform": "AWS"},
            ],
        }


recommendations_service = RecommendationsService()
