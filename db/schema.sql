CREATE EXTENSION IF NOT EXISTS vector;

create table if not exists chunks(
id text primary key,
country text not null,
page int,
source text not null,
section text,
content text not null,
embedding vector(384) not null
);