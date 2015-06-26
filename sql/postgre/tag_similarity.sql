BEGIN;

CREATE TABLE tag_similarity (
  base_tag_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  similarity INTEGER NOT NULL,
);

alter table tag_similarity add CONSTRAINT tag_similarity_pkey primary key (base_tag_id, tag_id);

END;