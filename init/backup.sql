create table if not exists tax_crawler.mission_record
(
	page_url varchar(255) not null comment '标识之一',
	mission_time float not null comment '标识之一',
	mission_status varchar(32) not null comment '任务处理结果',
	poster varchar(32) not null comment '任务投递者',
	carrier varchar(32) not null comment '任务消费者',
	constraint mission_record_pk
		unique (page_url, mission_time)
);

create table if not exists tax_crawler.mission_result
(
	url varchar(255) not null comment 'URL作为唯一标识符',
	mission_time float not null comment 'kafka and redis投递时间',
	topic varchar(255) not null,
	location varchar(255) null,
	content mediumtext not null comment '爬虫内容',
	file_links text null,
	constraint mission_result_url_uindex
		unique (url)
);

alter table tax_crawler.mission_result
	add primary key (url);

