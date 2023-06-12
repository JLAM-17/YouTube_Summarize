create table utilities (
    name varchar(255) primary key,
    value varchar(255),
    created_at timestamp default current_timestamp
)

insert into utilities (name, value) values ('YouTubeAPIKey', 'AIzaSyAbA0ASzbDjyBvna8trks_OcfOywjYQI8M')
insert into utilities (name, value) values ('OpenAIAPIKey', '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')

ALTER USER youtube_makers WITH PASSWORD 'rNxE1dSy!QKI#dt26#0n'

grant select on utilities to Youtube_Makers