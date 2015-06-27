BEGIN;

/**
app table
*/
CREATE TABLE app (
  id INTEGER NOT NULL,
  name character varying(512) NOT NULL,
  description character varying(5000) NOT NULL,
  icon character varying(512) NOT NULL,
  weight INTEGER
);

alter table app add CONSTRAINT app_pkey primary key (id);


/**
tag_app_rel table
*/
CREATE TABLE tag_app_rel (
  app_id INTEGER NOT NULL,
  tag character varying(256) NOT NULL,
  times INTEGER NOT NULL
);


/**
cm_tag table
*/
CREATE TABLE cm_tag (
  app_id INTEGER NOT NULL,
  tag character varying(256) NOT NULL,
  times INTEGER NOT NULL
);


/**
tag_similarity table
*/
CREATE TABLE tag_similarity (˙
  base_tag character varying(256) NOT NULL,
  tag character varying(256) NOT NULL,
  similarity FLOAT NOT NULL
);

ALTER TABLE ONLY tag_similarity
    ADD CONSTRAINT tag_similarity_tag_uniq UNIQUE (base_tag, tag);

END;
