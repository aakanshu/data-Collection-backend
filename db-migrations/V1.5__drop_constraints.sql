BEGIN;

ALTER TABLE users 
DROP COLUMN created,
DROP COLUMN created_by,
DROP COLUMN last_modified,
DROP COLUMN last_modified_by;

COMMIT;
