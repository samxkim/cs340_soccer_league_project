from flask import Flask, render_template
from flask import request

from db_connector.db_connector import connect_to_database, execute_query

# Creates Flask instance
webapp = Flask(__name__)


@webapp.route('/')
def index():
    return render_template('index.html')


@webapp.route('/coaches', methods=['POST', 'GET'])
def coaches():
    db_connection = connect_to_database()
    if request.method == 'GET':
        # SQL query to show Coaches
        query = "SELECT coachID, firstName, lastName, phone, email, team.teamName " \
                "as 'Team' FROM Coaches LEFT JOIN Teams team on Coaches.teamID = team.teamID"
        result = execute_query(db_connection, query).fetchall()

        # SQL query for list of team dropdown
        team_query = 'SELECT teamID, teamName FROM Teams'
        team_results = execute_query(db_connection, team_query).fetchall()
        return render_template('coaches.html', Coaches_Rows=result, teams=team_results)
    # Insert specific data
    elif request.method == 'POST':
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']
        team = request.form['team']

        phone_verify = "SELECT count(phone) FROM Coaches WHERE phone = '%s'" % phone
        phone_verify_result = execute_query(db_connection, phone_verify).fetchone()

        email_verify = "SELECT count(email) FROM Coaches WHERE email = '%s'" % email
        email_verify_result = execute_query(db_connection, email_verify).fetchone()

        # If there are no duplicates of the phone and email
        if phone_verify_result[0] == 0 and email_verify_result[0] == 0:
            if team == "NULL_TEAM":
                # SQL query if NULL team
                query = 'INSERT INTO Coaches (firstName, lastName, phone, email, teamID) ' \
                        'VALUES (%s,%s,%s,%s,NULL)'
                data = (fname, lname, phone, email)
                execute_query(db_connection, query, data)
            else:
                query = 'INSERT INTO Coaches (firstName, lastName, phone, email, teamID) ' \
                        'VALUES (%s,%s,%s,%s,(SELECT teamID FROM Teams WHERE teamID = %s))'
                data = (fname, lname, phone, email, team)
                execute_query(db_connection, query, data)

            # Text passed for next page
            prev_page = 'coaches'
            object_added = 'Coach'
            return render_template('added_successful.html', Previous_Page=prev_page,
                                   obj_add=object_added)
        else:
            prev_page = 'coaches'
            return render_template('duplicate_entry.html', Previous_Page=prev_page)


@webapp.route('/update_coaches/<int:coach_id>', methods=['POST', 'GET'])
def update_coaches(coach_id):
    db_connection = connect_to_database()
    # Display specific coach data
    if request.method == 'GET':
        coach_query = "SELECT coachID, firstName, lastName, phone, email, team.teamName " \
                      "as 'Team' FROM Coaches LEFT JOIN Teams team on Coaches.teamID = team.teamID " \
                      "WHERE coachID = %s" % coach_id
        coach_result = execute_query(db_connection, coach_query).fetchone()

        team_query = 'SELECT teamID, teamName FROM Teams'
        team_results = execute_query(db_connection, team_query).fetchall()

        prev_page = 'coaches'
        object_name = 'Coaches'
        return render_template('coachplayer_update.html', Previous_Page=prev_page,
                               obj_main=coach_result, teams=team_results, obj_name=object_name)
    # Insert coach data
    elif request.method == 'POST':
        coachid = request.form['CoachesID']
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']
        team = request.form['current_team']

        phone_verify = "SELECT count(phone) FROM Coaches WHERE phone = '%s' AND coachID != %s" % (phone, coachid)
        phone_verify_result = execute_query(db_connection, phone_verify).fetchone()

        email_verify = "SELECT count(email) FROM Coaches WHERE email = '%s' AND coachID != %s" % (email, coachid)
        email_verify_result = execute_query(db_connection, email_verify).fetchone()

        if phone_verify_result[0] == 0 and email_verify_result[0] == 0:
            if team == "NULL_TEAM":
                query = "UPDATE Coaches SET firstName = %s, lastName = %s, phone = %s, email = %s, teamID = NULL " \
                        "WHERE coachID = %s"
                data = (fname, lname, phone, email, coachid)
                result = execute_query(db_connection, query, data)
            else:
                query = "UPDATE Coaches SET firstName = %s, lastName = %s, phone = %s, email = %s, teamID = %s " \
                        "WHERE coachID = %s"
                data = (fname, lname, phone, email, team, coachid)
                result = execute_query(db_connection, query, data)

            prev_page = 'coaches'
            object_name = 'Coaches'

            return render_template('updated_successful.html', Previous_Page=prev_page,
                                   obj_main=fname, obj_name=object_name)
        else:
            prev_page = 'coaches'
            return render_template('duplicate_entry.html', Previous_Page=prev_page)


@webapp.route('/delete_coaches/<int:coach_id>')
def delete_coaches(coach_id):
    """deletes a coach with the given id"""
    db_connection = connect_to_database()
    name_query = "SELECT firstName FROM Coaches WHERE coachID = %s"
    name_data = (coach_id,)
    coach_firstname = execute_query(db_connection, name_query, name_data).fetchone()

    # SQL query to delete coach
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
    # Display player info
    if request.method == 'GET':
        query = "SELECT playerID, firstName, lastName, phone, email, team.teamName as 'Team' " \
                "FROM Players LEFT JOIN Teams team on Players.teamID = team.teamID"
        result = execute_query(db_connection, query).fetchall()

        team_query = 'SELECT teamID, teamName FROM Teams'
        team_results = execute_query(db_connection, team_query).fetchall()

        return render_template('players.html', Players_Rows=result, teams=team_results)
    # Insert player info
    elif request.method == 'POST':
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']
        team = request.form['team']

        phone_verify = "SELECT count(phone) FROM Players WHERE phone = '%s'" % phone
        phone_verify_result = execute_query(db_connection, phone_verify).fetchone()

        email_verify = "SELECT count(email) FROM Players WHERE email = '%s'" % email
        email_verify_result = execute_query(db_connection, email_verify).fetchone()

        if phone_verify_result[0] == 0 and email_verify_result[0] == 0:
            if team == "NULL_TEAM":
                query = 'INSERT INTO Players (firstName, lastName, phone, email, teamID) ' \
                        'VALUES (%s,%s,%s,%s,NULL)'
                data = (fname, lname, phone, email)
                execute_query(db_connection, query, data)
            else:
                query = 'INSERT INTO Players (firstName, lastName, phone, email, teamID) ' \
                        'VALUES (%s,%s,%s,%s,(SELECT teamID FROM Teams WHERE teamID = %s))'
                data = (fname, lname, phone, email, team)
                execute_query(db_connection, query, data)
            prev_page = 'players'
            object_added = 'Player'
            return render_template('added_successful.html', Previous_Page=prev_page, obj_add=object_added)
        else:
            prev_page = 'players'
            return render_template('duplicate_entry.html', Previous_Page=prev_page)


@webapp.route('/update_players/<int:player_id>', methods=['POST', 'GET'])
def update_players(player_id):
    db_connection = connect_to_database()
    # Display existing player info
    if request.method == 'GET':
        player_query = "SELECT playerID, firstName, lastName, phone, email, team.teamName as 'Team' " \
                       "FROM Players LEFT JOIN Teams team on Players.teamID = team.teamID " \
                       "WHERE playerID = %s" % player_id
        player_result = execute_query(db_connection, player_query).fetchone()

        team_query = 'SELECT teamID, teamName FROM Teams'
        team_results = execute_query(db_connection, team_query).fetchall()

        prev_page = 'players'
        object_name = 'Players'
        return render_template('coachplayer_update.html', Previous_Page=prev_page,
                               obj_main=player_result, teams=team_results, obj_name=object_name)
    # Update player info
    elif request.method == 'POST':
        playerid = request.form['PlayersID']
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']
        team = request.form['current_team']

        phone_verify = "SELECT count(phone) FROM Players WHERE phone = '%s' AND playerID != %s" % (phone, playerid)
        phone_verify_result = execute_query(db_connection, phone_verify).fetchone()

        email_verify = "SELECT count(email) FROM Players WHERE email = '%s' AND playerID != %s" % (email, playerid)
        email_verify_result = execute_query(db_connection, email_verify).fetchone()

        if phone_verify_result[0] == 0 and email_verify_result[0] == 0:
            if team == "NULL_TEAM":
                query = "UPDATE Players SET firstName = %s, lastName = %s, phone = %s, email = %s, teamID = NULL " \
                        "WHERE playerID = %s"
                data = (fname, lname, phone, email, playerid)
                result = execute_query(db_connection, query, data)
            else:
                query = "UPDATE Players SET firstName = %s, lastName = %s, phone = %s, email = %s, teamID = %s " \
                        "WHERE playerID = %s"
                data = (fname, lname, phone, email, team, playerid)
                result = execute_query(db_connection, query, data)

            prev_page = 'players'
            object_name = 'Players'

            return render_template('updated_successful.html', Previous_Page=prev_page,
                                   obj_main=fname, obj_name=object_name)
        else:
            prev_page = 'players'
            return render_template('duplicate_entry.html', Previous_Page=prev_page)


@webapp.route('/delete_players/<int:player_id>')
def delete_players(player_id):
    """deletes a player with the given id"""
    db_connection = connect_to_database()
    name_query = "SELECT firstName FROM Players WHERE playerID = %s"
    name_data = (player_id,)
    player_firstname = execute_query(db_connection, name_query, name_data).fetchone()

    # SQL query to delete player
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
    # Display all referees
    if request.method == 'GET':
        query = "SELECT refereeID, firstName, lastName, phone, email FROM Referees"
        result = execute_query(db_connection, query).fetchall()
        return render_template('referees.html', Referee_Rows=result)
    # Insert referee data
    elif request.method == 'POST':
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']

        phone_verify = "SELECT count(phone) FROM Referees WHERE phone = '%s'" % phone
        phone_verify_result = execute_query(db_connection, phone_verify).fetchone()

        email_verify = "SELECT count(email) FROM Referees WHERE email = '%s'" % email
        email_verify_result = execute_query(db_connection, email_verify).fetchone()

        if phone_verify_result[0] == 0 and email_verify_result[0] == 0:
            query = 'INSERT INTO Referees (firstName, lastName, phone, email) ' \
                    'VALUES (%s,%s,%s,%s)'
            data = (fname, lname, phone, email)
            execute_query(db_connection, query, data)
            prev_page = 'referees'
            object_added = 'Referee'
            return render_template('added_successful.html', Previous_Page=prev_page, obj_add=object_added)
        else:
            prev_page = 'referees'
            return render_template('duplicate_entry.html', Previous_Page=prev_page)


@webapp.route('/update_referees/<int:referee_id>', methods=['POST', 'GET'])
def update_referees(referee_id):
    db_connection = connect_to_database()
    # Display selected referee data
    if request.method == 'GET':
        referee_query = "SELECT refereeID, firstName, lastName, phone, email " \
                        "FROM Referees WHERE refereeID = %s" % referee_id
        referee_result = execute_query(db_connection, referee_query).fetchone()

        prev_page = 'referees'
        object_name = 'Referees'
        return render_template('referee_update.html', Previous_Page=prev_page,
                               obj_main=referee_result, obj_name=object_name)
    # Update referee data
    elif request.method == 'POST':
        refereeid = request.form['RefereesID']
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']

        phone_verify = "SELECT count(phone) FROM Referees WHERE phone = '%s' AND refereeID != %s" % (phone, refereeid)
        phone_verify_result = execute_query(db_connection, phone_verify).fetchone()

        email_verify = "SELECT count(email) FROM Referees WHERE email = '%s' AND refereeID != %s" % (email, refereeid)
        email_verify_result = execute_query(db_connection, email_verify).fetchone()

        if phone_verify_result[0] == 0 and email_verify_result[0] == 0:
            query = "UPDATE Referees SET firstName = %s, lastName = %s, phone = %s, email = %s " \
                    "WHERE refereeID = %s"
            data = (fname, lname, phone, email, refereeid)
            result = execute_query(db_connection, query, data)

            prev_page = 'referees'
            object_name = 'Referee'

            return render_template('updated_successful.html', Previous_Page=prev_page,
                                   obj_main=fname, obj_name=object_name)
        else:
            prev_page = 'referees'
            return render_template('duplicate_entry.html', Previous_Page=prev_page)


@webapp.route('/delete_referees/<int:referee_id>')
def delete_referees(referee_id):
    """deletes a referee with the given id"""
    db_connection = connect_to_database()
    # SQL query to select referee
    name_query = "SELECT firstName FROM Referees WHERE refereeID = %s"
    name_data = (referee_id,)
    referee_firstname = execute_query(db_connection, name_query, name_data).fetchone()

    games_referees_delete_query = "DELETE FROM Games_Referees where refereeID = %s"
    execute_query(db_connection, games_referees_delete_query, name_data)

    # SQL query to delete selected referee
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
    # Display team information
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
    # Insert team information
    elif request.method == 'POST':
        tname = request.form['teaminput']

        tname_verify = "SELECT count(teamName) FROM Teams WHERE teamName = '%s'" % tname
        tname_verify_result = execute_query(db_connection, tname_verify).fetchone()
        if tname_verify_result[0] == 0:
            query = 'INSERT INTO Teams (teamName) ' \
                    'VALUES (%s)'
            data = (tname,)
            execute_query(db_connection, query, data)
            prev_page = 'teams'
            object_added = 'Team'
            return render_template('added_successful.html', Previous_Page=prev_page, obj_add=object_added)
        else:
            prev_page = 'teams'
            return render_template('duplicate_team_entry.html', Previous_Page=prev_page)


@webapp.route('/update_teams/<int:team_id>', methods=['POST', 'GET'])
def update_teams(team_id):
    db_connection = connect_to_database()
    # Display selected team info
    if request.method == 'GET':
        teams_query = 'SELECT teamID, teamName FROM Teams where teamID = %s'
        data = (team_id,)
        teams_result = execute_query(db_connection, teams_query, data).fetchone()

        prev_page = 'teams'
        object_name = 'Teams'
        return render_template('teams_update.html', Previous_Page=prev_page, obj_main=teams_result,
                               obj_name=object_name)
    elif request.method == 'POST':
        teamID = request.form['teamID']
        teamName = request.form['teamName']

        query = 'UPDATE Teams SET teamName = %s WHERE teamID = %s'
        data = (teamName, teamID)
        execute_query(db_connection, query, data)

        prev_page = 'teams'
        object_name = 'Teams'

        return render_template('updated_successful.html', Previous_Page=prev_page, obj_main=teamName,
                               obj_name=object_name)


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

    # SQL queries to delete teams
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
    # Show game data
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
        # Insert game data
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


@webapp.route('/games_needing_teams', methods=['POST', 'GET'])
def games_needing_teams():
    """filter for games needing teams"""
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "select gameID, ifNull(team1.teamName, 'NONE') as 'Home Team', " \
                "ifNull(team2.teamName, 'NONE') as 'Away Team', " \
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
                "left join Teams team1 on game.homeTeamID = team1.teamID " \
                "left join Teams team2 on game.awayTeamID = team2.teamID " \
                "where homeTeamID is null or awayTeamID is null " \
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


@webapp.route('/games_needing_referee', methods=['POST', 'GET'])
def games_needing_referee():
    """filter for games needing referee(s)"""
    db_connection = connect_to_database()
    if request.method == 'GET':
        query = "select gameID, ifNull(team1.teamName, 'NONE') as 'Home Team', " \
                "ifNull(team2.teamName, 'NONE') as 'Away Team', " \
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
                "left join Teams team1 on game.homeTeamID = team1.teamID " \
                "left join Teams team2 on game.awayTeamID = team2.teamID " \
                "where gameID not in (SELECT gameID from Games_Referees) " \
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


@webapp.route('/games_update/<int:game_id>', methods=['POST', 'GET'])
def games_update(game_id):
    db_connection = connect_to_database()
    # display existing data
    if request.method == 'GET':
        query = "select gameID, ifNull(team1.teamName, 'NONE') as 'Home Team', " \
                "ifNull(team2.teamName, 'NONE') as 'Away Team', " \
                "date(gameDateTime) as Date, " \
                "homeTeamScore as 'Home Team Score', " \
                "awayTeamScore as 'Away Team Score', " \
                "canceled as 'Canceled?', " \
                "completed as 'Completed?', " \
                "(select GROUP_CONCAT(CONCAT(firstName,' ',lastName) SEPARATOR ', ') from Referees r " \
                "join Games_Referees g where r.refereeID = g.refereeID " \
                "and gameID = game.gameID " \
                "group by gameID) as Referees " \
                "from Games game " \
                "left join Teams team1 on game.homeTeamID = team1.teamID " \
                "left join Teams team2 on game.awayTeamID = team2.teamID " \
                "where gameID = %s;"
        data = (game_id,)
        game_result = execute_query(db_connection, query, data).fetchone()

        home_team_query = 'SELECT teamID, teamName FROM Teams ORDER BY teamName'
        home_team_results = execute_query(db_connection, home_team_query).fetchall()
        away_team_query = 'SELECT teamID, teamName FROM Teams'
        away__team_results = execute_query(db_connection, away_team_query).fetchall()

        referee_query = "SELECT refereeID, firstName, lastName from Referees where refereeID in " \
                        "(SELECT refereeID from Games_Referees where gameID = %s);"
        ref_results = execute_query(db_connection, referee_query, data).fetchall()

        all_refs_query = "select refereeID, firstName, lastName FROM Referees ORDER BY lastName"
        all_refs_results = execute_query(db_connection, all_refs_query).fetchall()
        prev_page = 'games'
        object_name = 'Games'
        return render_template('games_update.html', Previous_Page=prev_page,
                               obj_main=game_result, hometeams=home_team_results, allrefs=all_refs_results,
                               awayteams=away__team_results, obj_name=object_name, referees=ref_results)
    elif request.method == 'POST':

        gameID = request.form['gameID']
        homeTeamID = request.form['current_home_team']
        awayTeamID = request.form['current_away_team']
        if request.form['homescore']:
            homeTeamScore = request.form['homescore']
        else:
            homeTeamScore = 0
        if request.form['awayscore']:
            awayTeamScore = request.form['awayscore']
        else:
            awayTeamScore = 0
        if request.form['canceled']:
            canceled = request.form['canceled']
        else:
            canceled = 0
        if request.form['completed']:
            completed = request.form['completed']
        else:
            completed = 0
        date = request.form['dateinput']
        query = "UPDATE Games SET gameDateTime = %s, homeTeamID = %s, awayTeamID = %s, homeTeamScore = %s, " \
                "awayTeamScore = %s, canceled = %s, completed = %s WHERE gameID = %s"
        data = (date, homeTeamID, awayTeamID, homeTeamScore, awayTeamScore,
                canceled, completed, gameID)
        execute_query(db_connection, query, data)

        if int(request.form['referee1']) > 0:
            refereeID = request.form['referee1']
            ref_exists = "SELECT count(*) FROM Games_Referees where gameID = %s and refereeID = %s"
            data = (gameID, refereeID)
            ref_exists_result = execute_query(db_connection, ref_exists, data).fetchone()
            if ref_exists_result[0] == 0:
                query = 'INSERT INTO Games_Referees(gameID, refereeID) values (%s, %s)'
                data = (gameID, refereeID)
                execute_query(db_connection, query, data)

        if int(request.form['referee2']) > 0:
            refereeID = request.form['referee2']
            ref_exists = "SELECT count(*) FROM Games_Referees where gameID = %s and refereeID = %s"
            data = (gameID, refereeID)
            ref_exists_result = execute_query(db_connection, ref_exists, data).fetchone()
            if ref_exists_result[0] == 0:
                query = 'INSERT INTO Games_Referees(gameID, refereeID) values (%s, %s)'
                data = (gameID, refereeID)
                execute_query(db_connection, query, data)

        if int(request.form['referee3']) > 0:
            refereeID = request.form['referee3']
            ref_exists = "SELECT count(*) FROM Games_Referees where gameID = %s and refereeID = %s"
            data = (gameID, refereeID)
            ref_exists_result = execute_query(db_connection, ref_exists, data).fetchone()
            if ref_exists_result[0] == 0:
                query = 'INSERT INTO Games_Referees(gameID, refereeID) values (%s, %s)'
                data = (gameID, refereeID)
                execute_query(db_connection, query, data)

        prev_page = 'games'
        object_name = 'Games'

        return render_template('updated_successful.html', Previous_Page=prev_page, obj_main=game_id, obj_name=object_name)


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


@webapp.errorhandler(404)
def heh_error(e):
    return render_template('404.html'), 404


@webapp.errorhandler(500)
def another_heh_error(e):
    return render_template('500.html'), 500


# To start flask locally
# if __name__ == '__main__':
#     webapp.run(debug=True)
