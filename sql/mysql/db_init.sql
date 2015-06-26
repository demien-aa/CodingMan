DROP TABLE IF EXISTS `cm_tag`;
CREATE TABLE `cm_tag` (
    `id` int(11) NOT NULL auto_increment COMMENT 'pk',
    `app_id` int(11) NOT NULL,
    `times` int(11) NOT NULL,
    `tag` varchar(100) NOT NULL COMMENT 'tag',
    PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
