BEGIN;

CREATE TABLE user_responses(
    id SERIAL PRIMARY KEY NOT NULL,
    user_id SERIAL NOT NULL REFERENCES users(id),
    user_workflow_id SERIAL NOT NULL REFERENCES user_workflows(id),
    workflow_details_id SERIAL NOT NULL REFERENCES workflow_details(id),
    response JSON NOT NULL,
    response_status VARCHAR(30) NOT NULL DEFAULT 'REVIEW',
    created TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by SERIAL NOT NULL,
    last_modified TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_modified_by SERIAL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX ON user_responses(user_id, user_workflow_id, workflow_details_id, response_status) 
WHERE active=TRUE;

COMMIT;
