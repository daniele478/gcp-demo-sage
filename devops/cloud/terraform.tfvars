# Valori del progetto GCP. Questo file è versionato in questo repository (non è nel
# .gitignore); tutte le altre variabili (vedi variables.tf) hanno un default sensato per il
# corso.

project_id = "its-ict-sage-csp26"
region     = "europe-west6"

# Progetto condiviso tra più persone: il prefisso distingue le risorse di ogni studente
# nello stesso progetto (project_id sopra è il progetto condiviso). Con un progetto dedicato
# va lasciato vuoto.
resource_prefix = "its-ict-sage-daniele-buscemi"
