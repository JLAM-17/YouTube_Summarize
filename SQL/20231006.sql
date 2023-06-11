create table utilities (
    name primary key,
    value varchar(255),
    created_at timestamp default current_timestamp
)

insert into utilities (name, value) values ('YouTubeAPIKey', 'AIzaSyAbA0ASzbDjyBvna8trks_OcfOywjYQI8M')
ALTER USER youtube_makers WITH PASSWORD 'rNxE1dSy!QKI#dt26#0n'