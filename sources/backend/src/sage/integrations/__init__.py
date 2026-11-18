"""Adapters for external services: Vertex AI (LLM + embeddings), Firestore, BigQuery, Storage.

Main areas:
- llm: Google Gen AI SDK client, in Vertex AI mode (text generation + embeddings).
- firestore: chunk storage and vector search (find_nearest).
- bigquery: best-effort analytics logging of questions (MOCK: still a stub, see its docstring).
- storage: extra instructions for the prompt, read from a Cloud Storage bucket.
"""
