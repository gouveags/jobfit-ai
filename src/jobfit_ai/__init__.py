from jobfit_ai.llm import (
    match_resume_to_job_description,
    structure_job_description,
    structure_resume,
)
import time
import asyncio
from logging import getLogger
import logging
from jobfit_ai.main import evaluate_fit
from jobfit_ai.utils import md_file_to_text

logging.basicConfig(
    level=logging.INFO,
)

logger = getLogger(__name__)


async def process_job_description(file_path: str):
    logger.info("Starting job description processing...")

    job_description_text = await md_file_to_text(file_path)
    job_description = await structure_job_description(job_description_text)

    logger.info("Completed job description processing")
    return job_description


async def process_resume(file_path: str):
    logger.info("Starting resume processing...")

    resume_text = await md_file_to_text(file_path)
    resume = await structure_resume(resume_text)

    logger.info("Completed resume processing")
    return resume


async def async_main() -> None:
    start_time = time.time()

    job_description, resume = await asyncio.gather(
        process_job_description("src/jobfit_ai/samples/job_description.md"),
        process_resume("src/jobfit_ai/samples/resume.md"),
    )

    logger.info("Both processing tasks completed, starting comparison...")
    scores = await match_resume_to_job_description(resume, job_description)

    fit = evaluate_fit(scores)["fit"]
    logger.info(f"Fit: {fit}")

    elapsed_time = time.time() - start_time
    logger.info(f"Duration time: {elapsed_time:.2f} seconds")

    return fit


def main() -> None:
    """Synchronous entry point that runs the async main function."""
    return asyncio.run(async_main())
