"""Instructions step: load the extra instructions that apply to every answer."""

import asyncio

from sage.integrations.storage.instructions import read_instructions


async def load_instructions() -> str:
    # The Cloud Storage client is sync, like the Firestore and BigQuery ones.
    return await asyncio.to_thread(read_instructions)
