"""Generation step of the RAG pipeline: build the grounded prompt, call the LLM."""

from pathlib import Path

from google.api_core.exceptions import GoogleAPICallError
from google.genai.errors import APIError

from sage.domain.qa.exceptions import SageError
from sage.domain.qa.models import Chunk
from sage.integrations.llm.generate import generate_text

_PROMPT_TEMPLATE = (Path(__file__).parent / "prompts" / "answer_prompt.txt").read_text(
    encoding="utf-8"
)
_NO_DOCUMENTS_CONTEXT = (
    "Nessun documento disponibile (base di conoscenza non ancora popolata o non configurata)."
)
_NO_INSTRUCTIONS = "Nessuna istruzione aggiuntiva."


def build_prompt(question: str, chunks: list[Chunk], instructions: str = "") -> str:
    context = (
        "\n\n".join(f"[{chunk.source}] {chunk.text}" for chunk in chunks)
        if chunks
        else _NO_DOCUMENTS_CONTEXT
    )
    return _PROMPT_TEMPLATE.format(
        instructions=instructions or _NO_INSTRUCTIONS, context=context, question=question
    )


async def generate_answer(question: str, chunks: list[Chunk], instructions: str = "") -> str:
    prompt = build_prompt(question, chunks, instructions)
    try:
        return await generate_text(prompt)
    except (APIError, GoogleAPICallError) as exc:
        # SageError is what the HTTP layer translates into a 502 (see webapp/apis/qa/router.py).
        raise SageError(f"Generazione della risposta non riuscita: {exc}") from exc
