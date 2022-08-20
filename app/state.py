from app import read, gvs
import asyncio


class State:

    @classmethod
    async def setup(cls):
        cls.codes = read.read_txt_lines(gvs.CODES_FILE)
        cls.codes_lock = asyncio.Lock()

    @classmethod
    async def mark_code_used(cls, code: str):
        cls.codes.remove(code)
        async with cls.codes_lock:
            with open(gvs.CODES_FILE, "w") as f:
                f.write("\n".join(cls.codes))
