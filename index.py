from flask import Flask, request, json, jsonify, flash, redirect, abort, session, render_template
from os.path import join, dirname, realpath
from User import User
import os

app = Flask(__name__)
# declare lists for clubs, users, and club_list for specifically Jennifer's preferred clubs
global club_list
global all_users
global all_clubs
global Jennifer
club_list = []
all_users = []
# create instance of user Jennifer with the designated password and a random id number (not yet secured)
Jennifer = User('ilovearun6789', 123)
all_users.append(Jennifer)
SITE_ROOT = join(os.path.realpath(os.path.dirname(__file__)))
filename = os.path.join(SITE_ROOT, 'club_list.json')
with open(filename) as f:
    all_clubs = json.load(f)


@app.route('/')
def main():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Welcome to PennClubReview!"


@app.route('/register', methods=['POST'])
def register_user():
        # register and store new user into list of all users
    global all_users
    username = request.form['username']
    password = request.form['password']
    new_user = User(password, username)
    all_users.append(new_user)


@app.route('/login', methods=['POST'])
def admin_login():
        # login page for PennClubReview
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('Password is incorrect')
    return main()


@app.route('/api')
def api():
    return "Welcome to the PennClubReview API!."


@app.route('/api/clubs', methods=['GET', 'POST'])
def clubs():
    global all_clubs
    # serve the list of clubs in JSON format
    if request.method == 'GET':
        return jsonify(all_clubs)
    # create a new club, with its club information specified as parameters in request body
    if request.method == 'POST':
        request_json = request.get_json()
        club_name = request_json.get("name")
        club_size = request_json.get("size")
        all_clubs.append({"name": club_name, "size": club_size})
        return jsonify({"name": club_name, "size": club_size})


@app.route('/api/rankings', methods=['GET', 'POST'])
def rankings():
    global Jennifer
    global club_list
    # change the ranking of a specified club in Jennifer's rankings, there can't be any ties between clubs
    if request.method == 'POST':
        request_json = request.get_json()
        club_name = request_json.get("name")
        club_rank = request_json.get("rank")
        if club_name in club_list:
            club_list.insert(club_rank - 1, club_list.pop(club_list.index(club_name)))
            Jennifer.update_club_ranking(club_name, club_rank)
            return jsonify(club_list)
        else:
            club_list.insert(club_rank - 1, club_name)
            Jennifer.update_club_ranking(club_name, club_rank)
            return jsonify(club_list)

    # serve Jennifer's rankings in JSON format
    if request.method == 'GET':
        return jsonify(club_list)


@app.route('/api/user/<id>', methods=['GET'])
def id(id):
    global all_users
    # return a user whose id is specified as a route parameter
    if request.method == 'GET':
        for user in all_users:
            return user.get_user_id()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run()
