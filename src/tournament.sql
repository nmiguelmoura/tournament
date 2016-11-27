CREATE TABLE players( name TEXT,
                      points INTEGER,
                      id SERIAL PRIMARY KEY
);

CREATE TABLE matches ( playerA INTEGER,
                       playerB INTEGER,
                       victory TEXT
);