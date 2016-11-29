CREATE TABLE players( name TEXT,
                      id SERIAL PRIMARY KEY
);

CREATE TABLE matches ( winner INTEGER REFERENCES players(id),
                       loser INTEGER REFERENCES players(id),
                       id SERIAL PRIMARY KEY
);

CREATE VIEW count_wins AS SELECT players.id, count(matches.winner) as num
  FROM players LEFT JOIN matches
  ON players.id=matches.winner
  GROUP BY players.id
  ORDER BY num DESC;

CREATE VIEW count_player_matches AS SELECT players.id, count(matches) as num
  FROM players LEFT JOIN matches
  ON matches.winner=players.id OR matches.loser=players.id
  GROUP BY players.id
  ORDER BY num DESC;

CREATE VIEW count_wins_matches AS SELECT count_wins.id, count_wins.num as wins,
  count_player_matches.num as matches
  FROM count_wins JOIN count_player_matches
  ON count_wins.id=count_player_matches.id
  ORDER BY count_wins.num DESC;