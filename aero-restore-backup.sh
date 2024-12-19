#!/bin/bash

BACKUP_FILE="../.aero-db-backup.sql"

# Ensure the backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
  echo "Backup file not found!"
  exit 1
fi

read -p "[  WARNING  ] Are you sure you want to restore the database from the backup? This will overwrite existing data. (y/n): " CONFIRMATION

if [[ "$CONFIRMATION" != "y" ]]; then
  echo "Database restoration aborted."
  exit 0
fi

DB_ROOT_PASSWORD=$(docker compose exec aero-db cat /run/secrets/db_root_password)
docker compose exec -T -e MYSQL_PWD="$DB_ROOT_PASSWORD" aero-db sh -c 'exec mariadb -u"root"' < "$BACKUP_FILE"
echo "Database restoration completed."

