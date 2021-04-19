BEGIN;

CREATE TABLE accesstoken(
    id VARCHAR(300) PRIMARY KEY,
    ttl SERIAL NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by INTEGER NOT NULL,
    FOREIGN KEY(created_by) REFERENCES users (id)
);

CREATE INDEX on users(email);

COMMIT;
