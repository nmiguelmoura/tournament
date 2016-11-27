CREATE TABLE players( name TEXT,
                      points INTEGER,
                      id SERIAL PRIMARY KEY
);

CREATE TABLE matches ( playerA TEXT,
                       playerB TEXT,
                       victory TEXT
);