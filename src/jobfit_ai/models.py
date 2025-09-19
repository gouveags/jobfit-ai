from typing import List, Optional
from pydantic import BaseModel


class CandidateExperience(BaseModel):
    title: str
    company: str
    start_date: Optional[str]
    end_date: Optional[str]
    responsibilities: List[str]


class Resume(BaseModel):
    name: str
    email: Optional[str]
    location: Optional[str]
    summary: Optional[str]
    skills: List[str]
    experiences: List[CandidateExperience]
    projects: Optional[List[str]]
    education: Optional[List[str]]
    years_experience: Optional[int]


class JobDescription(BaseModel):
    title: str
    location: Optional[str]
    employment_type: Optional[str]
    responsibilities: List[str]
    requirements: List[str]
    nice_to_have: Optional[List[str]]
    skills: List[str]
    years_experience: Optional[int]


class ComparisonScores(BaseModel):
    technical_skills_score: float
    experience_years_score: float
    responsibilities_alignment_score: float
    education_score: float
    location_fit_score: float
    overall_softskills_score: float
