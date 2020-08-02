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
        query = "SELECT firstName, lastName, phone, email, team.teamName " \
            "as 'Team' FROM Coaches JOIN Teams team on Coaches.teamID = team.teamID"
        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template('coaches.html', Coaches_Rows=result)
    elif request.method == 'POST':
        print("Add new people!")
        fname = request.form['fninput']
        lname = request.form['lninput']
        phone = request.form['phonenum']
        email = request.form['email']
        team = request.form['team']

        query = 'INSERT INTO Coaches (firstName, lastName, phone, email, teamID) ' \
                'VALUES (%s,%s,%s,%s,(SELECT teamID FROM Teams WHERE teamName = %s))'
        data = (fname, lname, phone, email, team)
        execute_query(db_connection, query, data)
        return render_template('add_coaches_successful.html')


@webapp.route('/players')
def players():
    db_connection = connect_to_database()
    query = "SELECT firstName, lastName, phone, email, team.teamName as 'Team' " \
            "FROM Players JOIN Teams team on Players.teamID = team.teamID"
    result = execute_query(db_connection, query).fetchall()
    return render_template('players.html', Players_Rows=result)


@webapp.route('/referees')
def referees():
    db_connection = connect_to_database()
    query = "SELECT firstName, lastName, phone, email FROM Referees"
    result = execute_query(db_connection, query).fetchall()
    return render_template('referees.html', Referee_Rows=result)


@webapp.route('/teams')
def teams():
    db_connection = connect_to_database()
    query = "select teamID as ID, teamName as Team, (SELECT count(*) FROM Games " \
            "where (homeTeamID = teamID and homeTeamScore > awayTeamScore) " \
            "or (awayTeamID = teamID and awayTeamScore > homeTeamScore)) as Wins, " \
            "(SELECT count(*) FROM Games where (homeTeamID = teamID and homeTeamScore < awayTeamScore) " \
            "or (awayTeamID = teamID and awayTeamScore < homeTeamScore)) as Losses, (SELECT count(*) " \
            "FROM Games where (homeTeamID = teamID and homeTeamScore = awayTeamScore) " \
            " or (awayTeamID = teamID and awayTeamScore = homeTeamScore)) as Ties from Teams;"
    result = execute_query(db_connection, query)
    for r in result:
        print(r[0], r[1])
    return render_template('teams.html', rows=result)


@webapp.route('/games')
def games():
    db_connection = connect_to_database()

    query = "select team1.teamName as 'Home Team', " \
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
    result = execute_query(db_connection, query)
    for r in result:
        print(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
    return render_template('games.html', rows=result)


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
