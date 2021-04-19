BEGIN;

CREATE TABLE analytics (
    id SERIAL PRIMARY KEY NOT NULL,
    user_id SERIAL NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    user_data JSON,
    device_info JSON,
    network_info JSON,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE INDEX on analytics(event_name);

COMMIT;
