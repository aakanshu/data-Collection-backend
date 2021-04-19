BEGIN;

CREATE TABLE workflows(
    id SERIAL PRIMARY KEY NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by SERIAL NOT NULL,
    last_modified TIMESTAMP NOT NULL DEFAULT NOW(),
    last_modified_by SERIAL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY(created_by) REFERENCES users(id),
    FOREIGN KEY(last_modified_by) REFERENCES users(id)
);
CREATE INDEX ON workflows(active);

CREATE TABLE user_workflows(
    id SERIAL PRIMARY KEY NOT NULL,
    user_id SERIAL NOT NULL,
    workflow_id SERIAL NOT NULL,
    times INTEGER NOT NULL DEFAULT 1,
    completed INTEGER NOT NULL DEFAULT 0,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by SERIAL NOT NULL,
    last_modified TIMESTAMP NOT NULL DEFAULT NOW(),
    last_modified_by SERIAL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(workflow_id) REFERENCES workflows(id),
    FOREIGN KEY(created_by) REFERENCES users(id),
    FOREIGN KEY(last_modified_by) REFERENCES users(id)
);
CREATE INDEX ON user_workflows(user_id, workflow_id);

CREATE TYPE ref_language AS ENUM ('en', 'ru');

CREATE TABLE workflow_details(
    id SERIAL PRIMARY KEY NOT NULL,
    workflow_id SERIAL NOT NULL,
    name VARCHAR(300) NOT NULL,
    description TEXT,
    description_image VARCHAR(300),
    language ref_language NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by SERIAL NOT NULL,
    last_modified TIMESTAMP NOT NULL DEFAULT NOW(),
    last_modified_by SERIAL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    FOREIGN KEY(created_by) REFERENCES users(id),
    FOREIGN KEY(workflow_id) REFERENCES workflows(id),
    FOREIGN KEY(last_modified_by) REFERENCES users(id)
);

CREATE INDEX ON workflow_details(workflow_id);

COMMIT;
