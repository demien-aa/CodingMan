BEGIN;

/**
app table
*/
CREATE TABLE app (
  id INTEGER NOT NULL,
  name character varying(512) NOT NULL,
  description character varying(5000) NOT NULL,
  icon character varying(512) NOT NULL,
  weight INTEGER,
);

alter table app add CONSTRAINT app_pkey primary key (id);


/**
tag_app_rel table
*/
CREATE TABLE tag_app_rel (
  id INTEGER NOT NULL,
  app_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  times INTEGER NOT NULL,
);

alter table tag_app_rel add CONSTRAINT tag_app_rel_pkey primary key (id);


/**
cm_tag table
*/
CREATE TABLE cm_tag (
  id INTEGER NOT NULL,
  app_id INTEGER NOT NULL,
  times INTEGER NOT NULL,
  tag INTEGER NOT NULL,
);

alter table cm_tag add CONSTRAINT cm_tag_pkey primary key (id);

/**
tag table
*/
CREATE TABLE tag (
  id INTEGER NOT NULL,
  name character varying(512) NOT NULL,
);

alter table tag add CONSTRAINT tag_pkey primary key (id);

/**
tag_similarity table
*/
CREATE TABLE tag_similarity (
  base_tag_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  similarity INTEGER NOT NULL,
);

END;
