BEGIN;

CREATE TABLE app_to_tag (
  id INTEGER NOT NULL,
  app_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
);

alter table app_to_tag add CONSTRAINT app_to_tag_pkey primary key (id);

END;