BEGIN;

CREATE TYPE ref_question AS ENUM ('video', 'text');

DROP TABLE IF EXISTS questions;
CREATE TABLE questions(
    id SERIAL PRIMARY KEY NOT NULL,
    workflow_details_id SERIAL NOT NULL REFERENCES workflow_details(id),
    name VARCHAR(500) NOT NULL,
    description text,
    help_text text,
    is_required BOOLEAN NOT NULL DEFAULT FALSE,
    question_type ref_question NOT NULL,
    default_value text,
    question_serial_num INTEGER NOT NULL,
    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by SERIAL NOT NULL,
    last_modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_modified_by SERIAL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX ON questions(workflow_details_id) WHERE active=TRUE;

COMMIT;
