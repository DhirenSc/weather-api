-- we don't know how to generate root <with-no-name> (class Root) :(
create table locations
(
	location_id varchar(11) not null
		primary key,
	city varchar(50) not null,
	state varchar(50) not null,
	timestamp timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP
);

create table daily_data
(
	location_id varchar(11) not null,
	day int not null,
	description varchar(100) null,
	high_temp float null,
	low_temp float null,
	humidity int null,
	primary key (day, location_id),
	constraint daily_fk_location
		foreign key (location_id) references locations (location_id)
);

create table logs
(
	log_id int auto_increment
		primary key,
	ip varchar(45) null,
	city varchar(50) null,
	state varchar(50) null,
	timestamp timestamp default CURRENT_TIMESTAMP null
);