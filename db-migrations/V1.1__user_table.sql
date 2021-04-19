BEGIN;

CREATE TABLE users (
    id SERIAL NOT NULL PRIMARY KEY, 
    name VARCHAR(255) NOT NULL, 
    email VARCHAR(255) NOT NULL UNIQUE, 
    password_hash VARCHAR(100), 
    photo_url VARCHAR(255), 
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by SERIAL NOT NULL,
    last_modified TIMESTAMP NOT NULL DEFAULT NOW(),
    last_modified_by SERIAL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX ON users(active);

COMMIT;
