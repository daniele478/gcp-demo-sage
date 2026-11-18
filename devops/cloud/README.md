# Infrastruttura di Sage (Terraform)

Un solo ambiente: queste risorse coprono l'intero progetto di corso, non c'è una
separazione dev/test/prod. Ogni studente applica questo modulo sul proprio progetto GCP.

## Risorse create

| File | Risorsa | A cosa serve |
|---|---|---|
| `services.tf` | `google_project_service` | Abilita le API GCP usate dal progetto |
| `docs.tf` | `google_storage_bucket` | Bucket dei documenti sorgente (`<project_id>-sage-docs` o `<prefisso>-sage-docs`) |
| `firestore.tf` | `google_firestore_database`, `google_firestore_index` | Firestore Native + indice vettoriale sul campo `embedding` della collection `chunks` |
| `sage_backend.tf` | `google_artifact_registry_repository`, `google_cloud_run_v2_service`, `google_service_account`, `google_project_iam_member` | Repository Docker, servizio che espone `/api/ask`, service account runtime a privilegio minimo e relativi ruoli |
| `locals.tf` | `locals` | Regole uniche per i nomi delle risorse (vedi sotto) |
| `variables.tf`, `providers.tf` | — | Variabili di input e provider/backend GCS |

BigQuery (dataset `sage_analytics`, tabella `question_log`) **non è ancora** gestito da
Terraform: l'analytics nel backend è uno stub, vedi
`sources/backend/src/sage/integrations/bigquery/question_log.py`.

Niente Secret Manager: Sage chiama Vertex AI con Application Default Credentials, non
servono API key esterne da custodire come segreto.

## Nomi delle risorse: `resource_prefix`

`locals.tf` è l'unico punto in cui si decide come si chiamano le risorse. Con
`resource_prefix` vuoto (default) il progetto è dedicato e i nomi sono quelli fissi
(`sage-backend`, `(default)`, `<project_id>-sage-docs`). Con `resource_prefix` valorizzato
(es. `its-ict-sage-mario-rossi`) il progetto è condiviso e ogni nome parte dal prefisso,
adattato alle regole di ogni servizio:

- Cloud Run e Artifact Registry: `<prefisso>-sage-backend`
- Bucket: `<prefisso>-sage-docs` (e `<prefisso>-tfstate` per lo state)
- Firestore: un database per persona, chiamato come il prefisso (in un progetto c'è un solo `(default)`)
- BigQuery: dataset `<prefisso con _ al posto di ->_sage_analytics` (i dataset non ammettono trattini)
- Service account: `<prefisso>-sage-backend-run`, accorciato con un hash se supera i 30 caratteri

## Perché l'immagine Cloud Run non è gestita da Terraform

`sage_backend.tf` imposta `container_image` su un placeholder pubblico e poi lo ignora
(`lifecycle.ignore_changes`). L'immagine reale viene pubblicata dalla pipeline applicativa
(`.github/workflows/deploy.yml`, `gcloud run deploy --image ...`), tenuta volutamente
separata dalla pipeline Terraform (`.github/workflows/terraform.yml`): una modifica al
codice non richiede di rieseguire un piano Terraform, e viceversa.

## Comandi

```bash
cd devops/cloud

# una tantum: crea il bucket di state se non esiste già
gcloud storage buckets create gs://<prefix o project_id>-tfstate \
  --project <project_id> --location europe-west6 --uniform-bucket-level-access

# backend.hcl e terraform.tfvars sono già presenti e versionati: controlla i valori
terraform init -backend-config=backend.hcl
terraform plan  -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

In CI, lo stesso flusso gira nel workflow `terraform.yml`, avviato manualmente (tab
**Actions** del repository → *terraform* → *Run workflow*, oppure `gh workflow run
terraform.yml`): `plan`, poi un job `approval` che attende un'approvazione manuale su una
issue GitHub prima di eseguire `apply` sul piano già salvato.
