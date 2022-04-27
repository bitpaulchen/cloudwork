drop table if exists user;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `about_me` varchar(128) DEFAULT NULL,
  `password_hash` varchar(128)  NOT NULL,
  `avatar` varchar(256) default null ,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_user_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=latin1;
ALTER TABLE user AUTO_INCREMENT = 1;

CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(140) DEFAULT NULL,
  `post_uid` varchar(120) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `short_desc` TEXT DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_post_timestamp` (`timestamp`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=201 DEFAULT CHARSET=latin1;


CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `body` text null,
  `timestamp` datetime DEFAULT NULL,
  `post_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `post_id` (`post_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_timestamp` (`timestamp`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`post_id`) REFERENCES `post` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=306 DEFAULT CHARSET=latin1;


CREATE TABLE `followers` (
  `follower_id` int(11) DEFAULT NULL,
  `followed_id` int(11) DEFAULT NULL,
  KEY `followed_id` (`followed_id`),
  KEY `follower_id` (`follower_id`),
  CONSTRAINT `followers_ibfk_1` FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`),
  CONSTRAINT `followers_ibfk_2` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


update post set short_desc= case post_uuid
    when '45ace124-c55e-11ec-9cfd-9801a7a5e02d' then 'xxx'
when 'f6c20472-c55d-11ec-9cfd-9801a7a5e02d' then 'yyy' end
where post_uuid in ('45ace124-c55e-11ec-9cfd-9801a7a5e02d','f6c20472-c55d-11ec-9cfd-9801a7a5e02d');
