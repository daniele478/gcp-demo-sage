variable "project_id" {
  description = "ID del progetto GCP"
  type        = string
}

variable "region" {
  description = "Regione GCP in cui creare le risorse"
  type        = string
}

variable "resource_prefix" {
  description = "Prefisso usato per i nomi delle risorse"
  type        = string
}

variable "docs_bucket_name" {
  description = <<-EOT
    Nome del bucket dei documenti da riusare se ne esiste già uno.
    Vuoto (default) = nome derivato in locals.tf ("<prefisso>-sage-docs" oppure
    "<project_id>-sage-docs"). Se lo valorizzi, importa il bucket nello state prima
    del primo apply: terraform import google_storage_bucket.sage_docs <nome>.
  EOT
  type        = string
  default     = ""
}
