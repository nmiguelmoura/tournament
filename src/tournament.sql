DROP DATABASE IF EXISTS tournament;
CREATE DATABASE TOURNAMENT;
\c tournament

CREATE TABLE players( name TEXT,
                      id SERIAL PRIMARY KEY
);

CREATE TABLE matches ( winner INTEGER FOREIGN KEY REFERENCES players(id),
                       looser INTEGER FOREIGN KEY REFERENCES players(id),
                       id SERIAL PRIMARY KEY
);