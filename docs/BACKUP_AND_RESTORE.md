# Database & Media Backup and Restore Guide: PKV Global Infotech

This guide outlines the standard operating procedures for backing up and restoring data for the PKV Global Infotech Django platform.

---

## 1. Important Safety Standard: Isolated Restore

> [!CAUTION]
> **NEVER restore directly into the active database using `--clean` or overwrite commands (`pg_restore --clean -d "$DATABASE_URL"`).**
> Doing so against an active database drops live production tables, interrupts active connections, and risks catastrophic data loss if the backup file is incomplete or corrupted.
>
> **Always restore backups into a separate, distinct test database (`RESTORE_TEST_DATABASE_URL`) first to verify table integrity and data readability.**

---

## 2. PostgreSQL Backup & Verification Procedure (Production & Staging)

### Step 1: Create a Consistent Database Dump
Run this command from your automated backup runner or administrative terminal:
```bash
# Set timestamp and backup filename
BACKUP_FILE="pkv_backup_$(date +%Y%m%d_%H%M%S).dump"

# Take binary custom-format dump
pg_dump "$DATABASE_URL" \
    --format=custom \
    --no-owner \
    --no-privileges \
    --file="$BACKUP_FILE"

echo "Backup created successfully: $BACKUP_FILE"
```

### Step 2: Restore into a Distinct Empty Test Database
Do NOT restore into `$DATABASE_URL`. Provision or target a clean, separate test database specified by `RESTORE_TEST_DATABASE_URL`:
```bash
# Ensure RESTORE_TEST_DATABASE_URL points to an isolated, empty database
# Example: postgres://user:password@hostname:5432/pkv_restore_test_db

pg_restore \
    --no-owner \
    --no-privileges \
    --exit-on-error \
    --dbname="$RESTORE_TEST_DATABASE_URL" \
    "$BACKUP_FILE"

echo "Restore into test database completed successfully."
```

### Step 3: Verify Data Readability from the Test Database
Verify that core models and enquiries can be queried without errors:
```bash
# Run verification using Django pointing to RESTORE_TEST_DATABASE_URL
DATABASE_URL="$RESTORE_TEST_DATABASE_URL" python manage.py shell -c "
from website.models import Contact, Project, Service, CompanySetting

print('Restored Enquiries count:', Contact.objects.count())
print('Restored Products count:', Project.objects.count())
print('Restored Services count:', Service.objects.count())

# Verify latest enquiry can be read
latest = Contact.objects.order_by('-created').first()
if latest:
    print(f'Latest enquiry read: {latest.name} (Topic: {latest.topic}, Status: {latest.status})')
"
```

---

## 3. SQLite Local & Staging Fallback Procedure

### Step 1: Hot Backup via SQLite API
```bash
# Use SQLite's online backup tool to prevent locking issues
sqlite3 db.sqlite3 ".backup 'staging_backup_$(date +%Y%m%d).sqlite3'"
```

### Step 2: Restore to a Distinct Test File
```bash
# Copy into an isolated test destination
cp "staging_backup_$(date +%Y%m%d).sqlite3" "restore_test_db.sqlite3"
```

### Step 3: Verify Test Database Readability
```bash
DATABASE_URL="sqlite:///$(pwd)/restore_test_db.sqlite3" python manage.py shell -c "
from website.models import Contact, Project, Service

print('Verified Enquiries count:', Contact.objects.count())
print('Verified Products count:', Project.objects.count())
"

# Remove temporary test database after verification
rm "restore_test_db.sqlite3"
```

---

## 4. Uploaded Media Files (Screenshots & Graphics)

On containerized environments (like Render), files saved to local disk `media/` are ephemeral.

### Backup Media Directory:
```bash
tar -czvf "media_backup_$(date +%Y%m%d_%H%M%S).tar.gz" media/
```

### Restore Media to Persistent Storage / Test Volume:
```bash
# Extract into target media mount (e.g. Render Persistent Disk mount at /var/data/media)
tar -xzvf "media_backup_YYYYMMDD_HHMMSS.tar.gz" -C /path/to/persistent/media/
```
