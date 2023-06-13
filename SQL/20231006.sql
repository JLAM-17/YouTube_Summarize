create table utilities (
    name varchar(255) primary key,
    value varchar(255),
    created_at timestamp default current_timestamp
)

insert into utilities (name, value) values ('YouTubeAPIKey', 'AIzaSyAbA0ASzbDjyBvna8trks_OcfOywjYQI8M')
insert into utilities (name, value) values ('OpenAIAPIKey', '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')

ALTER USER youtube_makers WITH PASSWORD 'rNxE1dSy!QKI#dt26#0n'

grant select on utilities to Youtube_Makers
grant all on videos to Youtube_Makers

create table videos (
    video_id varchar(255) primary key,
    title varchar(500),
	channel varchar(500),
	cover varchar(500),
	tags varchar(500),
	category varchar(100),
	default_language varchar(20),
	main_ideas varchar(500),
	summary text,
	sentiment_analysis varchar(100),
	sentiment_score float,	
    created_at timestamp default current_timestamp
)
alter table videos alter column sentiment_analysis type varchar(1000)
alter table videos alter column main_ideas type varchar(1000)