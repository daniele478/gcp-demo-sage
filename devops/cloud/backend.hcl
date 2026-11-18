# Backend GCS dello state Terraform. Questo file è versionato in questo repository (non è nel
# .gitignore). Il bucket deve esistere prima di `terraform init` — vedi il README per il
# comando `gcloud storage buckets create` da eseguire una tantum (lo fa anche in automatico
# il job "plan" della pipeline .github/workflows/terraform.yml).
# Progetto dedicato: <project_id>-tfstate. Progetto condiviso: <resource_prefix>-tfstate.
bucket = "its-ict-sage-daniele-buscemi-tfstate"
prefix = "sage"
