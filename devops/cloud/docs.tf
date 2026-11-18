resource "google_storage_bucket" "sage_docs" {
  name     = local.docs_bucket_name
  project  = var.project_id
  location = var.region

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  force_destroy = true
}
