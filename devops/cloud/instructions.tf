# Istruzioni aggiuntive che l'API legge a ogni domanda e aggiunge al prompt (es. lo stile
# della risposta). Sono volutamente separate dai documenti della base di conoscenza: non
# vengono indicizzate in Firestore, quindi aggiornarle è solo un nuovo upload nel bucket,
# senza redeploy e senza re-ingestion.
resource "google_storage_bucket" "instructions" {
  name     = local.instructions_bucket_name
  project  = var.project_id
  location = var.region

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  force_destroy = true
}

# Il service account runtime deve poter scaricare il file delle istruzioni: il permesso è
# limitato a questo bucket (non a livello di progetto), come per il resto del servizio.
resource "google_storage_bucket_iam_member" "sage_run_instructions" {
  bucket = google_storage_bucket.instructions.name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.sage_run.email}"
}
