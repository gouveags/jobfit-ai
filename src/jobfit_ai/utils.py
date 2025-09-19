import aiofiles


async def md_file_to_text(md_file_path: str) -> str:
    async with aiofiles.open(md_file_path, "r") as file:
        md_text = await file.read()
    return md_text.replace("\n", " ")
