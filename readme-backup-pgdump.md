
Envoyer 



sudo nano /usr/local/bin/backup_postgres_pgdump_dev.sh

backup_postgres_pgdump_dev.sh
sudo chmod +x /usr/local/bin/backup_postgres_pgdump_dev.sh
env -i /usr/local/bin/backup_postgres_pgdump_dev.sh





# PARAMETRES VPS PGDUMP

Paramèrtrage du VPS pour la sauvegarde automatique des volumes de BDD


## 1. Script

Le script comprend le code à exécuter pour faire le dump de la base de données.

Créer/éditer le fichier backup_postgres.sh (control + o pour enregister)
```bash
sudo nano /usr/local/bin/backup_postgres_pgdump_dev.sh
```

Contenu du fichier backup_postgres.sh
```bash
 #!/bin/bash

# Configuration
CONTAINER_NAME="postgres_db"  # Nom de ton conteneur Docker PostgreSQL
DB_NAME="mydatabase"             # Nom de la base à sauvegarder
DB_USER="db_reservation_salles"                # Utilisateur PostgreSQL
DB_PASS="P@ss_ResaSallesDB"               # Mot de passe PostgreSQL
BACKUP_DIR="/var/backups/postgres"      # Dossier de sauvegarde
DATE=$(date +%Y-%m-%d_%H-%M-%S)          # Date pour le nom du fichier
LOG_FILE="/var/log/backup_postgres.log"  # Chemin du fichier log

# Crée le dossier de sauvegarde s'il n'existe pas
mkdir -p "$BACKUP_DIR" 2>> "$LOG_FILE"
echo "[$(date)] Début du backup de $DB_NAME" >> "$LOG_FILE"

TMP_FILE="$BACKUP_DIR/$DB_NAME-$DATE.sql"

# Effectue le dump via Docker
/usr/bin/docker exec -e PGPASSWORD="$DB_PASS" "$CONTAINER_NAME" \
/usr/bin/pg_dump -U "$DB_USER" -d "$DB_NAME" > "$TMP_FILE" 2>> "$LOG_FILE"

# Vérifie que le fichier n'est pas vide
if [ ! -s "$TMP_FILE" ]; then
    echo "[$(date)] ERREUR: dump vide" >> "$LOG_FILE"
    rm -f "$TMP_FILE"
    exit 1
fi


echo "[$(date)] Backup terminé avec succès : $TMP_FILE" >> "$LOG_FILE"
# (Optionnel) Compresse le dump
gzip "$TMP_FILE"

# (Optionnel) Supprime les sauvegardes de plus de 7 jours
find "$BACKUP_DIR" -name "$DB_NAME-*.sql.gz" -type f -mtime +7 -delete

```

Rendre le script executable
```bash
sudo chmod +x /usr/local/bin/backup_postgres.sh
```
Tester le script dans l'environnement vide de cron
```bash
env -i /usr/local/bin/backup_postgres.sh
``` 
Un nouveau fichier *nomBasePostgres-date.sql.gz* doit apparaitre dans le dossier /var/backups/postgres


## 2. Paramètrer CRON 

Ligne a jouetr pour exécuter le script chaque jour à 2h00 et enregistrer les log
```bash
crontab -e

0 2 * * * /usr/local/bin/backup_postgres.sh >> /var/log/backup_postgres.log 2>&1