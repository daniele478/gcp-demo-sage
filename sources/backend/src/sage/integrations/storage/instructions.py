"""Reads the extra instructions (a Markdown file) from Cloud Storage.

Le istruzioni non vengono messe in cache di proposito: la lettura avviene a ogni domanda, così
modificare il file nel bucket cambia subito le risposte, senza redeploy e senza riavviare il
servizio. Un oggetto assente o un permesso mancante non devono mai far fallire la risposta:
in quel caso si prosegue senza istruzioni, come fa il retrieval quando Firestore non risponde.
"""

import logging

from sage.config import get_app_config
from sage.integrations.storage.client import get_storage_client

log = logging.getLogger(__name__)


def read_instructions() -> str:
    """Return the contents of the instructions blob, or "" when it is not available."""
    config = get_app_config()
    if not config.instructions_bucket_name:
        return ""

    blob_uri = f"gs://{config.instructions_bucket_name}/{config.instructions_blob_name}"
    try:
        blob = (
            get_storage_client()
            .bucket(config.instructions_bucket_name)
            .blob(config.instructions_blob_name)
        )
        text = blob.download_as_text(encoding="utf-8")
    except Exception:
        # Non-GoogleAPICallError failures (credenziali, rete) degradano allo stesso modo:
        # le istruzioni sono un extra, la risposta deve uscire comunque.
        log.warning("Istruzioni non leggibili da %s: proseguo senza", blob_uri, exc_info=True)
        return ""

    log.info("Istruzioni caricate da %s (%d caratteri)", blob_uri, len(text))
    return text.strip()
