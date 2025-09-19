from openai.lib._parsing._responses import TextFormatT
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from logging import getLogger

from jobfit_ai.models import Resume, JobDescription, ComparisonScores
from jobfit_ai.prompts import (
    system_match_resume_to_job_description_prompt,
    system_structure_job_description_prompt,
    system_structure_resume_prompt,
    user_prompt_match_resume_to_job_description,
    user_prompt_structure_job_description,
    user_prompt_structure_resume,
)

load_dotenv()

logger = getLogger(__name__)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


async def llm(
    system_prompt: str, user_prompt: str, text_format: TextFormatT
) -> TextFormatT:
    try:
        response = await client.responses.parse(
            model=OPENAI_MODEL,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            text_format=text_format,
        )
        return response.output_parsed
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        raise e


async def structure_resume(candidate_resume_text: str) -> Resume:
    return await llm(
        system_prompt=system_structure_resume_prompt,
        user_prompt=user_prompt_structure_resume(candidate_resume_text),
        text_format=Resume,
    )


async def structure_job_description(job_description_text: str) -> JobDescription:
    return await llm(
        system_prompt=system_structure_job_description_prompt,
        user_prompt=user_prompt_structure_job_description(job_description_text),
        text_format=JobDescription,
    )


async def match_resume_to_job_description(
    structured_resume: Resume, structured_job_description: JobDescription
) -> ComparisonScores:
    return await llm(
        system_prompt=system_match_resume_to_job_description_prompt,
        user_prompt=user_prompt_match_resume_to_job_description(
            structured_resume, structured_job_description
        ),
        text_format=ComparisonScores,
    )
