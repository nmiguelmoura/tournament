#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    c.execute("UPDATE players set points='%s'", (0,))
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM players")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT COUNT(*) "
              "FROM players ")
    result = c.fetchall()[0][0]
    DB.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO players (name, points) values (%s, 0)", (name,))
    DB.commit()

    # para apagar
    c.execute("SELECT id FROM players WHERE name=%s", (name, ))
    id = c.fetchall()[0][0]

    DB.close()

    # para apagar
    return id


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute(
        "SELECT players.id as pid, players.name, players.points, (SELECT COUNT(*) FROM matches where matches.playera=players.id OR matches.playerb=players.id) "
        "FROM players "
        "ORDER BY players.points DESC")
    result = c.fetchall()
    DB.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    winner = int(winner)
    loser = int(loser)

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO matches (playera, playerb, victory) values (%s, %s, %s)", (winner, loser, winner,))
    c.execute("SELECT points FROM players WHERE id='%s'", (winner,))
    points = c.fetchall()[0][0] + 1
    c.execute("UPDATE players SET points='%s' WHERE players.id='%s'", (points, winner,))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    DB = psycopg2.connect('dbname=tournament')
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    player_count = c.fetchall()[0][0]
    c.execute("SELECT id, name, points FROM players ORDER BY points DESC")
    player_series = c.fetchall()

    pairs = make_pairs(c, player_series, player_count)
    DB.close()


    return pairs

def make_pairs(cursor, players, players_to_pair):
    pairs = []
    matches_number = players_to_pair / 2
    for num in range(0, players_to_pair):
        for i in range(0, players_to_pair):
            if i != num and players[i] != False and players[num] != False:
                print num
                print i
                pl_a = players[num]
                pl_b = players[i]
                pair_available = test_pair(cursor, pl_a, pl_b)
                print '####'
                print pair_available
                print '####'
                if pair_available:
                    pairs.append((pl_a[0], pl_a[1], pl_b[0], pl_b[1]))
                    players[num] = False
                    players[i] = False
                    break

    return pairs


def test_pair(cursor, player_a, player_b):
    player_a_id = player_a[0]
    player_b_id = player_b[0]
    cursor.execute("SELECT COUNT(*) FROM matches "
                   "WHERE (playera='%s' AND playerb='%s') "
                   "OR (playera='%s' AND playerb='%s')", (player_a_id, player_b_id, player_b_id, player_a_id))
    if cursor.fetchall()[0][0] == 0:
        return True
    else:
        return False

deletePlayers()
a = registerPlayer('Nuno')          # 3
b = registerPlayer('Pedro')         # 2
c = registerPlayer('Carolina')      # 1
d = registerPlayer('Miguel')        # 1
e = registerPlayer('Cris')          # 2
f = registerPlayer('Marta')         # 2
g = registerPlayer('Andre')         # 1
h = registerPlayer('Joao')          # 0

                                    # Nuno      3
                                    # Pedro     2
                                    # Marta     2
                                    # Cris      2
                                    # Miguel    1
                                    # Carolina  1
                                    # Andre     1
                                    # Joao      0

reportMatch(a, b)
reportMatch(c, d)
reportMatch(e, f)
reportMatch(g, h)

reportMatch(a, c)
reportMatch(e, g)
reportMatch(b, d)
reportMatch(f, h)

reportMatch(a, e)
reportMatch(b, c)
reportMatch(f, g)
reportMatch(d, h)

print playerStandings()
print swissPairings()
