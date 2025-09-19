from jobfit_ai.models import JobDescription, Resume


system_structure_resume_prompt = """You are an expert AI assistant that extracts structured data from candidate resumes.
Your task is to parse the resume text and convert it into a structured JSON object
that follows the given schema exactly.

Schema (Pydantic-compatible):

{{
  "name": str,
  "email": str | null,
  "location": str | null,
  "summary": str | null,
  "skills": [str],
  "experiences": [
    {{
      "title": str,
      "company": str,
      "start_date": str | null,   # format: YYYY-MM or YYYY
      "end_date": str | null,     # "Present" if ongoing
      "responsibilities": [str]
    }}
  ],
  "projects": [str] | null,
  "education": [str] | null,
  "years_experience": int | null   # inferred total
}}

Guidelines:
- Do not invent information. If not found, return null.
- Normalize dates into YYYY-MM when possible.
- Keep skills as atomic items (e.g., "React.js", "Node.js").
- Keep responsibilities short bullet-like phrases.
- Only output valid JSON.
"""

system_structure_job_description_prompt = """You are an expert AI assistant that extracts structured data from job descriptions.
Your task is to read a natural language job posting and convert it into a structured JSON object
that follows the given schema exactly.

Schema (Pydantic-compatible):

{{
  "title": str,
  "location": str | null,
  "employment_type": str | null,       # e.g. full-time, contract, internship
  "responsibilities": [str],
  "requirements": [str],               # must-have requirements
  "nice_to_have": [str] | null,        # optional requirements
  "skills": [str],                     # key technical and soft skills
  "years_experience": int | null       # minimum required years
}}

Guidelines:
- Do not invent information. If something is missing, set it to null.
- Keep text concise (no long paragraphs).
- Extract lists as atomic bullet points (not long sentences).
- Only output valid JSON.
"""

system_match_resume_to_job_description_prompt = """You are an expert hiring assistant that compares a candidate resume against a job description.
Your job is to evaluate the candidate on each dimension of the job requirements and assign
scores between 0 and 1 (where 0 = no match, 1 = perfect match, and decimals are partial matches).

Use the following schema:

{{
  "technical_skills_score": float,
  "experience_years_score": float,
  "responsibilities_alignment_score": float,
  "education_score": float,
  "location_fit_score": float,
  "overall_softskills_score": float
}}

Guidelines:
- Compare candidate structured data vs job structured data directly.
- Normalize scores to be between 0.0 and 1.0.
- If information is missing, assign 0.0 for that category.
- Be objective and concise. Do not output reasoning here, only the JSON with scores.

"""


def user_prompt_match_resume_to_job_description(
    structured_resume: Resume, structured_job_description: JobDescription
) -> str:
    return f"""Here is the job description (structured JSON):
{structured_job_description}

Here is the candidate resume (structured JSON):
{structured_resume}

Compare them and output the JSON scores.

"""


def user_prompt_structure_resume(candidate_resume_text: str) -> str:
    return f"""Here is the candidate resume text:

---
{candidate_resume_text}
---

Extract the structured data as JSON.
"""


def user_prompt_structure_job_description(job_description_text: str) -> str:
    return f"""Here is the job description text:

---
{job_description_text}
---

Extract the structured data as JSON.
"""
