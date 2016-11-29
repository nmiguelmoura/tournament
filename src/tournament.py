#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print "Couldn't establish connection to database"


def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    query = "TRUNCATE TABLE matches"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    query = "DELETE FROM players"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    query = "SELECT COUNT(*) FROM players"
    cursor.execute(query)
    result = cursor.fetchone()[0]
    db.close()
    return result


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # If data cames from external source, use bleach to sanitize input
    # name = bleach.clean(name)

    db, cursor = connect()
    query = "INSERT INTO players (name) values (%s)"
    params = (name,)
    cursor.execute(query, params)
    db.commit()
    db.close()


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

    # Join players table with count_wins_matches view.
    db, cursor = connect()
    query = "SELECT players.id, players.name, count_wins_matches.wins, " \
            "count_wins_matches.matches " \
            "FROM players JOIN count_wins_matches " \
            "ON players.id=count_wins_matches.id " \
            "ORDER BY count_wins_matches.wins DESC"
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Use bleach if data comes from external source
    # winner = int(bleach.clean(winner))
    # loser = int(bleach.clean(loser))

    db, cursor = connect()
    query = "INSERT INTO matches (winner, loser) values (%s, %s)"
    params = (winner, loser,)
    cursor.execute(query, params)
    db.commit()
    db.close()


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

    player_count = countPlayers()

    standings = playerStandings()

    db, cursor = connect()
    pairs = make_pairs(cursor, standings, player_count)
    db.close()

    return pairs


def make_pairs(cursor, players, players_to_pair):
    # Initialize pairs list
    pairs = []

    # Get number of matches.
    matches_number = players_to_pair / 2

    # Pair players according to the number of points.
    # For each player on list, try to pair with another with similar points.
    for num in range(0, players_to_pair):
        if players[num] != False:
            # If player was not removed, get pair.
            for i in range(0, players_to_pair):
                if i != num and players[i] != False and players[num] != False:
                    # If player is not the same for i and num and if player i
                    # and num exist, try to pair

                    pl_a = players[num]
                    pl_b = players[i]

                    # Check if pair didn t already matched.
                    pair_available = test_pair(cursor, pl_a, pl_b)

                    if pair_available:
                        # Run if pair didn t matched already.
                        # Append tupple with pair id and name to pairs list.
                        # (id_a, name_a, id_b, name_b)
                        pairs.append((pl_a[0], pl_a[1], pl_b[0], pl_b[1]))

                        # Remove players from players list
                        players[num] = False
                        players[i] = False

                        # Stop nested loop;
                        break
    # Return the lit with tupples for each match in round
    return pairs


def test_pair(cursor, player_a, player_b):
    # Get players ids.
    player_a_id = player_a[0]
    player_b_id = player_b[0]

    # Check if players already matched.
    query = "SELECT COUNT(*) FROM matches " \
            "WHERE (winner='%s' AND loser='%s') OR (winner='%s' AND loser='%s')"
    params = (player_a_id, player_b_id, player_b_id, player_a_id)
    cursor.execute(query, params)

    if cursor.fetchone()[0] == 0:
        # Run if player never matched.
        return True
    else:
        # Run if player already matched.
        return False
