DROP TABLE IF EXISTS `cm_tag`;
CREATE TABLE `cm_tag` (
    `id` int(11) NOT NULL auto_increment COMMENT 'pk',
    `app_id` int(11) NOT NULL,
    `times` int(11) NOT NULL,
    `tag` varchar(100) NOT NULL COMMENT 'tag',
    PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
create index index_cm_tag_tag on cm_tag (tag);
create index index_cm_tag_tag_app_id on cm_tag (tag, app_id);


DROP TABLE IF EXISTS `cm_app`;
CREATE TABLE `cm_app` (
  `id` INTEGER NOT NULL,
  `name` character varying(512) NOT NULL,
  `description` character varying(5000) NOT NULL,
  `icon` character varying(512) NOT NULL,
  `weight` INTEGER,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
create index index_app_id on cm_app (id); 


DROP TABLE IF EXISTS `cm_tag_app_rel`;
CREATE TABLE `cm_tag_app_rel` (
  `app_id `INTEGER NOT NULL,
  `tag` character varying(256) NOT NULL,
  `times` INTEGER NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `cm_tag_similarity`;
CREATE TABLE `cm_tag_similarity` (
  `base_tag` character varying(256) NOT NULL,
  `tag` character varying(256) NOT NULL,
  `similarity` FLOAT NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;

