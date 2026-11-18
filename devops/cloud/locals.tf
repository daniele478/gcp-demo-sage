locals {
  # Cloud Run, Artifact Registry, service account: "<prefisso>-<app_name>" in un progetto
  # condiviso, oppure solo "<app_name>" in un progetto dedicato (prefisso vuoto).
  app_name = (
    var.resource_prefix == ""
    ? var.app_name
    : "${var.resource_prefix}-${var.app_name}"
  )

  # Bucket dei documenti: se docs_bucket_name è valorizzato si riusa un bucket già esistente
  # (da importare nello state), altrimenti "<project_id>-sage-docs" nel progetto dedicato o
  # "<prefisso>-sage-docs" in quello condiviso.
  docs_bucket_name = (
    var.docs_bucket_name != ""
    ? var.docs_bucket_name
    : (
      var.resource_prefix == ""
      ? "${var.project_id}-sage-docs"
      : "${var.resource_prefix}-sage-docs"
    )
  )

  # In un progetto c'è un solo database "(default)"; in un progetto condiviso ogni studente
  # ha il proprio database, chiamato come il prefisso.
  firestore_database_name = var.resource_prefix == "" ? "(default)" : var.resource_prefix

  # account_id di un service account: massimo 30 caratteri. Se "<app_name>-run" non ci sta,
  # si tronca e si aggiunge un hash del nome completo per mantenerlo univoco e stabile.
  sage_run_account_id = (
    length("${local.app_name}-run") <= 30
    ? "${local.app_name}-run"
    : "${substr(local.app_name, 0, 17)}-${substr(md5(local.app_name), 0, 8)}-run"
  )
}
