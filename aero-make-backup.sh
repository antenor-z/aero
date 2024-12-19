#/bin/bash
docker compose exec -e MYSQL_PWD=$(docker compose exec aero-db cat /run/secrets/db_root_password) aero-db sh -c 'exec mariadb-dump -u"root" --all-databases --single-transaction' > ../.aero-db-backup.sql
