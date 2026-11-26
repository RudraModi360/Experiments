# Backup & Rotation Policy

Create executable `rotate_backups.sh` supporting:
`./rotate_backups.sh --ref-date YYYY-MM-DD` (defaults to `2026-11-26` if omitted).

1. Archive `./projects` into `./backups/backup-<REF_DATE>.tar.gz`.
   - Respect patterns in `./projects/.backupignore` (`*.tmp`, `build_cache`).
   - Skip broken symlinks cleanly without failing or aborting.
   - Preserve spaces in file and directory names.
2. Enforce retention on `./backups/backup-YYYY-MM-DD.tar.gz` relative to `<REF_DATE>`:
   - Keep all backups from the last 7 days inclusive (`<REF_DATE>` and the 6 preceding days: `2026-11-20` .. `2026-11-26` when ref-date is `2026-11-26`).
   - For older backups, keep ONLY the 4 most recent Sunday backups (`2026-11-15`, `2026-11-08`, `2026-11-01`, `2026-10-25` when ref-date is `2026-11-26`).
   - Delete all other older `backup-*.tar.gz` files.
