use monitor;
set names utf8;

#slow详情表
CREATE TABLE `slowlogdetail` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `ipaddr` varchar(60) NOT NULL DEFAULT '' COMMENT '连接db的客户端IP',
  `querytime` varchar(60) NOT NULL DEFAULT '' COMMENT '查询时间',
  `locktime` varchar(60) NOT NULL DEFAULT '' COMMENT 'lock时间',
  `parserowcount` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '搜索的行数',
  `returnrowcount` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '返回的行数',
  `execstarttime` datetime NOT NULL DEFAULT '2012-12-12 12:12:12' COMMENT '开始时间',
  `dbname` varchar(30) NOT NULL DEFAULT '' COMMENT '库名',
  `sqltext` text NOT NULL COMMENT '原始SQL文本',
  `hashvalue` varchar(100) NOT NULL DEFAULT '' COMMENT '一致性hash',
  PRIMARY KEY (`id`),
  KEY `idx_execstarttime` (`execstarttime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='慢日志详细信息';

#slow-hash值表
CREATE TABLE `slowagginfo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `dbnameid` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '库名id',
  `dbname` varchar(30) NOT NULL DEFAULT '' COMMENT '数据库名',
  `sqltext` text NOT NULL COMMENT '处理过后的SQL文本',
  `sqlstatus` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '确认SQL:0：不知道，1：知道',
  `hashvalue` varchar(100) NOT NULL DEFAULT '' COMMENT '一致性hash',
  `lasttime` datetime NOT NULL DEFAULT '2012-12-12 12:12:12' COMMENT '最后修改时间',
  PRIMARY KEY (`id`),
  KEY `idx_lasttime` (`lasttime`),
  KEY `idx_dbnameid` (`dbnameid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='慢SQL日志'