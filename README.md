# Swiss Pairing System Tournament API

This API keeps track of players and matches in a game tournament, using the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

This project uses Python and PostgreSQL.

## API
The API stores info in postgreSQL and has the following functions:

connect() -> Allows connection to database.<br>deleteMatches() -> Remove all the match records from the database.<br>deletePlayers() -> Remove all the player records from the database.<br>countPlayers() -> Returns the number of players currently registered.<br>registerPlayer(name) -> Adds a player to the tournament database.<br>playerStandings() -> Returns a list of the players and their win records, sorted by wins.<br>reportMatch() -> Records the outcome of a single match between two players.<br>swissPairings() -> Returns a list of pairs of players for the next round of a match.



## Run code
The project is configured to run in a Virtualbox VM with Ubuntu using Vagrant. PostgreSQL and Bleach where previously installed and are necessary to run the code.

To run the code:
- Install [Virtualbox](https://www.virtualbox.org/);

- Install [Vagrant](https://www.vagrantup.com/);

- Fork and clone this repository to your system.

- Through command line, navigate to the project folder and run the code:
`$ vagrant up`

- After that, run:
`$ vagrant ssh`

- Navigate to shared folder vagrant/src:
`$ cd /vagrant/src`

- Enter psql command line:
`$ psql`

- Create tournament database:
`vagrant=> CREATE DATABASE tournament`

- Connect to database created:
`vagrant=> \c tournament`

- Import database schema from file:
`tournament=> \i tournament.sql`

- Run the file tournament_test.py to test API (after pressing CTRL+D to exit psql command-line):
`$ python tournament_test.py`