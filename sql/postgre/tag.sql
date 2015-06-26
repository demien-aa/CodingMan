BEGIN;

CREATE TABLE tag (
  id INTEGER NOT NULL,
  name character varying(512) NOT NULL,
);

alter table tag add CONSTRAINT tag_pkey primary key (id);

END;