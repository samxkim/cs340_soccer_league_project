from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query

# create the web application
webapp = Flask(__name__)


@webapp.route('/browse_bsg_people')
# the name of this function is just a cosmetic thing
def browse_people():
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()
    query = "SELECT fname, lname, homeworld, age, id from bsg_people;"
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('people_browse.html', rows=result)


@webapp.route('/add_new_people', methods=['POST', 'GET'])
def add_new_people():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = 'SELECT id, name from bsg_planets'
        result = execute_query(db_connection, query).fetchall()
        print(result)

        return render_template('people_add_new.html', planets=result)
    elif request.method == 'POST':
        print("Add new people!")
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
        data = (fname, lname, age, homeworld)
        execute_query(db_connection, query, data)
        return 'Person added!'


@webapp.route('/')
def index():
    return render_template('index.html')


@webapp.route('/coaches', methods=['POST', 'GET'])
def coaches():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "SELECT coachID, firstName, lastName, phone, email, team.teamName " \
                "as 'Team' FROM Coaches JOIN Teams team on Coaches.teamID = team.teamID"
        result = execute_query(db_connection, query).fetchall()
        return render_template('coaches.html', Coaches_Rows=result)
    elif request.method == 'POST':
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']
        team = request.form['team']

        query = 'INSERT INTO Coaches (firstName, lastName, phone, email, teamID) ' \
                'VALUES (%s,%s,%s,%s,(SELECT teamID FROM Teams WHERE teamName = %s))'
        data = (fname, lname, phone, email, team)
        execute_query(db_connection, query, data)
        prev_page = 'coaches'
        object_added = 'Coach'
        return render_template('added_successful.html', Previous_Page=prev_page, obj_add=object_added)


@webapp.route('/update_coaches/<int:coach_id>', methods=['POST', 'GET'])
def update_coaches(coach_id):
    db_connection = connect_to_database()
    # display existing data
    if request.method == 'GET':
        coach_query = "SELECT coachID, firstName, lastName, phone, email, team.teamName " \
                      "as 'Team' FROM Coaches JOIN Teams team on Coaches.teamID = team.teamID " \
                      "WHERE coachID = %s" % coach_id
        coach_result = execute_query(db_connection, coach_query).fetchone()

        team_query = 'SELECT teamID, teamName FROM Teams'
        team_results = execute_query(db_connection, team_query).fetchall()

        prev_page = 'coaches'
        object_name = 'Coaches'
        return render_template('coachplayer_update.html', Previous_Page=prev_page,
                               obj_main=coach_result, teams=team_results, obj_name=object_name)
    elif request.method == 'POST':
        coachid = request.form['CoachesID']
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']
        team = request.form['current_team']

        query = "UPDATE Coaches SET firstName = %s, lastName = %s, phone = %s, email = %s, teamID = %s " \
                "WHERE coachID = %s"
        data = (fname, lname, phone, email, team, coachid)
        result = execute_query(db_connection, query, data)

        prev_page = 'coaches'
        object_name = 'Coaches'

        return render_template('updated_successful.html', Previous_Page=prev_page,
                               obj_main=fname, obj_name=object_name)


@webapp.route('/delete_coaches/<int:coach_id>')
def delete_coaches(coach_id):
    """deletes a coach with the given id"""
    db_connection = connect_to_database()
    name_query = "SELECT firstName FROM Coaches WHERE coachID = %s"
    name_data = (coach_id,)
    coach_firstname = execute_query(db_connection, name_query, name_data).fetchone()

    query = "DELETE FROM Coaches WHERE coachID = %s"
    data = (coach_id,)

    result = execute_query(db_connection, query, data)

    prev_page = 'coaches'
    object_added = 'Coach'
    return render_template('deleted_successful.html', Previous_Page=prev_page, obj_add=object_added,
                           obj_name=coach_firstname)


@webapp.route('/players', methods=['POST', 'GET'])
def players():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "SELECT playerID, firstName, lastName, phone, email, team.teamName as 'Team' " \
                "FROM Players JOIN Teams team on Players.teamID = team.teamID"
        result = execute_query(db_connection, query).fetchall()
        return render_template('players.html', Players_Rows=result)
    elif request.method == 'POST':
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']
        team = request.form['team']

        query = 'INSERT INTO Players (firstName, lastName, phone, email, teamID) ' \
                'VALUES (%s,%s,%s,%s,(SELECT teamID FROM Teams WHERE teamName = %s))'
        data = (fname, lname, phone, email, team)
        execute_query(db_connection, query, data)
        prev_page = 'players'
        object_added = 'Player'
        return render_template('added_successful.html', Previous_Page=prev_page, obj_add=object_added)


@webapp.route('/update_players/<int:player_id>', methods=['POST', 'GET'])
def update_players(player_id):
    db_connection = connect_to_database()
    # display existing data
    if request.method == 'GET':
        player_query = "SELECT playerID, firstName, lastName, phone, email, team.teamName as 'Team' " \
                      "FROM Players JOIN Teams team on Players.teamID = team.teamID " \
                       "WHERE playerID = %s" % player_id
        player_result = execute_query(db_connection, player_query).fetchone()

        team_query = 'SELECT teamID, teamName FROM Teams'
        team_results = execute_query(db_connection, team_query).fetchall()

        prev_page = 'players'
        object_name = 'Players'
        return render_template('coachplayer_update.html', Previous_Page=prev_page,
                               obj_main=player_result, teams=team_results, obj_name=object_name)
    elif request.method == 'POST':
        playerid = request.form['PlayersID']
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']
        team = request.form['current_team']

        query = "UPDATE Players SET firstName = %s, lastName = %s, phone = %s, email = %s, teamID = %s " \
                "WHERE playerID = %s"
        data = (fname, lname, phone, email, team, playerid)
        result = execute_query(db_connection, query, data)

        prev_page = 'players'
        object_name = 'Players'

        return render_template('updated_successful.html', Previous_Page=prev_page,
                               obj_main=fname, obj_name=object_name)


@webapp.route('/delete_players/<int:player_id>')
def delete_players(player_id):
    """deletes a player with the given id"""
    db_connection = connect_to_database()
    name_query = "SELECT firstName FROM Players WHERE playerID = %s"
    name_data = (player_id,)
    player_firstname = execute_query(db_connection, name_query, name_data).fetchone()

    query = "DELETE FROM Players WHERE playerID = %s"
    data = (player_id,)

    result = execute_query(db_connection, query, data)

    prev_page = 'players'
    object_added = 'Player'
    return render_template('deleted_successful.html', Previous_Page=prev_page, obj_add=object_added,
                           obj_name=player_firstname)


@webapp.route('/referees', methods=['POST', 'GET'])
def referees():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "SELECT refereeID, firstName, lastName, phone, email FROM Referees"
        result = execute_query(db_connection, query).fetchall()
        return render_template('referees.html', Referee_Rows=result)
    elif request.method == 'POST':
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']

        query = 'INSERT INTO Referees (firstName, lastName, phone, email) ' \
                'VALUES (%s,%s,%s,%s)'
        data = (fname, lname, phone, email)
        execute_query(db_connection, query, data)
        prev_page = 'referees'
        object_added = 'Referee'
        return render_template('added_successful.html', Previous_Page=prev_page, obj_add=object_added)


# @webapp.route('/update_referees/<int:referee_id>', methods=['POST', 'GET'])
# def update_players(referee_id):
#     db_connection = connect_to_database()
#     # display existing data
#     if request.method == 'GET':
#         player_query = "SELECT playerID, firstName, lastName, phone, email, team.teamName as 'Team' " \
#                       "FROM Players JOIN Teams team on Players.teamID = team.teamID " \
#                        "WHERE playerID = %s" % player_id
#         player_result = execute_query(db_connection, player_query).fetchone()
#
#         team_query = 'SELECT teamID, teamName FROM Teams'
#         team_results = execute_query(db_connection, team_query).fetchall()
#
#         prev_page = 'players'
#         object_name = 'Players'
#         return render_template('coachplayer_update.html', Previous_Page=prev_page,
#                                obj_main=player_result, teams=team_results, obj_name=object_name)
#     elif request.method == 'POST':
#         playerid = request.form['PlayersID']
#         fname = request.form['fninput']
#         lname = request.form['lninput']
#         phone = request.form['phonenum']
#         email = request.form['email']
#         team = request.form['current_team']
#
#         query = "UPDATE Players SET firstName = %s, lastName = %s, phone = %s, email = %s, teamID = %s " \
#                 "WHERE playerID = %s"
#         data = (fname, lname, phone, email, team, playerid)
#         result = execute_query(db_connection, query, data)
#
#         prev_page = 'players'
#         object_name = 'Players'
#
#         return render_template('updated_successful.html', Previous_Page=prev_page,
#                                obj_main=fname, obj_name=object_name)


@webapp.route('/delete_referees/<int:referee_id>')
def delete_referees(referee_id):
    """deletes a referee with the given id"""
    db_connection = connect_to_database()
    name_query = "SELECT firstName FROM Referees WHERE refereeID = %s"
    name_data = (referee_id,)
    referee_firstname = execute_query(db_connection, name_query, name_data).fetchone()

    query = "DELETE FROM Referees WHERE refereeID = %s"
    data = (referee_id,)

    result = execute_query(db_connection, query, data)

    prev_page = 'referees'
    object_added = 'Referee'
    return render_template('deleted_successful.html', Previous_Page=prev_page, obj_add=object_added,
                           obj_name=referee_firstname)


@webapp.route('/teams', methods=['POST', 'GET'])
def teams():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "select teamID as ID, teamName as Team, (SELECT count(*) FROM Games " \
                "where (homeTeamID = teamID and homeTeamScore > awayTeamScore) " \
                "or (awayTeamID = teamID and awayTeamScore > homeTeamScore)) as Wins, " \
                "(SELECT count(*) FROM Games where (homeTeamID = teamID and homeTeamScore < awayTeamScore) " \
                "or (awayTeamID = teamID and awayTeamScore < homeTeamScore)) as Losses, (SELECT count(*) " \
                "FROM Games where (homeTeamID = teamID and homeTeamScore = awayTeamScore) " \
                "or (awayTeamID = teamID and awayTeamScore = homeTeamScore)) as Ties from Teams " \
                "ORDER by teamName;"
        result = execute_query(db_connection, query).fetchall()
        return render_template('teams.html', rows=result)
    elif request.method == 'POST':
        tname = request.form['teaminput']

        query = 'INSERT INTO Teams (teamName) ' \
                'VALUES (%s)'
        data = (tname,)
        execute_query(db_connection, query, data)
        prev_page = 'teams'
        object_added = 'Team'
        return render_template('added_successful.html', Previous_Page=prev_page, obj_add=object_added)


@webapp.route('/delete_teams/<int:id>')
def delete_teams(id):
    """deletes a team with the given id"""
    db_connection = connect_to_database()

    data = (id,)
    query = 'UPDATE Coaches set teamID = null where teamID = %s'
    execute_query(db_connection, query, data)
    query = 'UPDATE Games set homeTeamID = null where homeTeamID = %s'
    execute_query(db_connection, query, data)
    query = 'UPDATE Games set awayTeamID = null where awayTeamID = %s'
    execute_query(db_connection, query, data)
    query = 'UPDATE Players set teamID = null where teamID = %s'
    execute_query(db_connection, query, data)

    name_query = "SELECT teamName FROM Teams WHERE teamID = %s"
    team_name = execute_query(db_connection, name_query, data).fetchone()
    print(team_name)

    query = "DELETE FROM Teams WHERE teamID = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)

    prev_page = 'teams'
    object_added = 'Team'
    return render_template('deleted_successful.html', Previous_Page=prev_page, obj_add=object_added,
                           obj_name=team_name)


@webapp.route('/roster/<int:id>', methods=['GET'])
def roster(id):
    """Returns a team roster page"""
    if request.method == 'GET':
        db_connection = connect_to_database()
        data = (id,)
        name_query = 'SELECT teamName FROM Teams WHERE teamID = %s'
        team = execute_query(db_connection, name_query, data).fetchone()
        coach_query = 'SELECT * from Coaches WHERE teamID = %s'
        coach = execute_query(db_connection, coach_query, data).fetchall()
        player_query = 'SELECT * FROM Players WHERE teamID = %s'
        players = execute_query(db_connection, player_query, data).fetchall()
        return render_template('roster.html', team=team, coaches=coach, players=players)


@webapp.route('/leaguestandings', methods=['GET'])
def leaguestandings():
    if request.method == 'GET':
        db_connection = connect_to_database()
        query = 'select teamName as Team, (SELECT count(*) FROM Games where (homeTeamID = teamID ' \
                'and homeTeamScore > awayTeamScore) or (awayTeamID = teamID and awayTeamScore > homeTeamScore))*3 + ' \
                '(SELECT count(*) FROM Games 	where (homeTeamID = teamID and homeTeamScore = awayTeamScore) or ' \
                '(awayTeamID = teamID and awayTeamScore = homeTeamScore)) as Points from Teams order by Points desc;'
        teamlist = execute_query(db_connection, query).fetchall()
        return render_template('leaguestandings.html', results=teamlist)


@webapp.route('/games', methods=['POST', 'GET'])
def games():
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "select gameID, team1.teamName as 'Home Team', " \
                "team2.teamName as 'Away Team', " \
                "gameDateTime as Date, " \
                "homeTeamScore as 'Home Team Score', " \
                "awayTeamScore as 'Away Team Score', " \
                "canceled as 'Canceled?', " \
                "completed as 'Completed?', " \
                "(select GROUP_CONCAT(CONCAT(firstName,' ',lastName) SEPARATOR ', ') from Referees r " \
                "join Games_Referees g where r.refereeID = g.refereeID " \
                "and gameID = game.gameID " \
                "group by gameID) as Referees " \
                "from Games game " \
                "join Teams team1 on game.homeTeamID = team1.teamID " \
                "join Teams team2 on game.awayTeamID = team2.teamID " \
                "order by game.gameID;"
        result = execute_query(db_connection, query).fetchall()
        query = "SELECT teamID, teamName from Teams;"
        home_teams = execute_query(db_connection, query).fetchall()
        query = "SELECT teamID, teamName from Teams;"
        away_teams = execute_query(db_connection, query).fetchall()
        query = "SELECT refereeID, firstName, LastName from Referees;"
        refs = execute_query(db_connection, query).fetchall()
        return render_template('games.html', rows=result, homeTeams=home_teams, awayTeams=away_teams,
                               refereeList=refs)
    elif request.method == 'POST':
        date = request.form['dateinput']
        hometeam = int(request.form['homeinput'])
        awayteam = int(request.form['awayinput'])
        referee = int(request.form['refereeinput'])
        query = "INSERT INTO Games (gameDateTime, homeTeamID, homeTeamScore, awayTeamID, awayTeamScore, canceled, " \
                "completed) VALUES (%s, %s, 0, %s, 0, 0, 0);"
        data = (date, hometeam, awayteam)
        execute_query(db_connection, query, data)
        prev_page = 'games'
        object_added = 'Game'
        query = "INSERT INTO Games_Referees (gameID, refereeID) VALUES ((SELECT gameID from " \
                "Games where homeTeamID = %s and awayTeamID = %s and gameDateTime = %s), %s);"
        data = (hometeam, awayteam, date, referee)
        execute_query(db_connection, query, data)
        return render_template('added_successful.html', Previous_Page=prev_page, obj_add=object_added)


@webapp.route('/delete_games/<int:game_id>')
def delete_games(game_id):
    """deletes a game with the given id"""
    db_connection = connect_to_database()
    data = (game_id,)

    query = 'DELETE FROM Games_Referees WHERE gameID = %s'
    execute_query(db_connection, query, data)
    query = "DELETE FROM Games WHERE gameID = %s"

    result = execute_query(db_connection, query, data)

    prev_page = 'games'
    object_added = 'Game'
    return render_template('deleted_successful.html', Previous_Page=prev_page, obj_add=object_added,
                           obj_name='')


@webapp.route('/db_test')
def test_database_connection():
    print("Executing a sample query on the database using the credentials from db_credentials.py")
    db_connection = connect_to_database()
    query = "SELECT * from bsg_people;"
    result = execute_query(db_connection, query)
    return render_template('db_test.html', rows=result)


# display update form and process any updates, using the same function
@webapp.route('/update_people/<int:id>', methods=['POST', 'GET'])
def update_people(id):
    print('In the function')
    db_connection = connect_to_database()
    # display existing data
    if request.method == 'GET':
        print('The GET request')
        people_query = 'SELECT id, fname, lname, homeworld, age from bsg_people WHERE id = %s' % (id)
        people_result = execute_query(db_connection, people_query).fetchone()

        if people_result is None:
            return "No such person found!"

        planets_query = 'SELECT id, name from bsg_planets'
        planets_results = execute_query(db_connection, planets_query).fetchall()

        print('Returning')
        return render_template('people_update.html', planets=planets_results, person=people_result)
    elif request.method == 'POST':
        print('The POST request')
        character_id = request.form['character_id']
        fname = request.form['fname']
        lname = request.form['lname']
        age = request.form['age']
        homeworld = request.form['homeworld']

        query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE id = %s"
        data = (fname, lname, age, homeworld, character_id)
        result = execute_query(db_connection, query, data)
        print(str(result.rowcount) + " row(s) updated")

        return redirect('/browse_bsg_people')


@webapp.route('/delete_people/<int:id>')
def delete_people(id):
    """deletes a person with the given id"""
    db_connection = connect_to_database()
    query = "DELETE FROM bsg_people WHERE id = %s"
    data = (id,)

    result = execute_query(db_connection, query, data)
    return str(result.rowcount) + "row deleted"


@webapp.errorhandler(404)
def heh_error(e):
    return render_template('404.html'), 404


@webapp.errorhandler(500)
def another_heh_error(e):
    return render_template('500.html'), 500


# To start flask locally
if __name__ == '__main__':
    webapp.run(debug=True)
