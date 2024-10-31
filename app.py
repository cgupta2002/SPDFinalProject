from flask import Flask, render_template, url_for, request, redirect, flash, session
from tools import Tool
from reviews import Review
from users import User
from messages import Message

app = Flask(__name__)
app.secret_key = '2bshd9ei3nd40fk'

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/marketplace')
def market():
    return render_template('market.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/messages')
def message():
    return render_template('message.html')

@app.route('/marketplace/add', methods=['GET', 'POST'])
def add_tool():
    if request.method == 'GET':

        return render_template('add_tool.html')
    elif request.method == 'POST':
        tools = Tool.getAllTools()
        last_id = tools[-1]['id']
        
        return render_template('market.html')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        users = User.getAllUsers()
        last_id = int(users[-1]['user_id'])
        user_id = last_id + 1
        username = request.form['username']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        profile_image = request.form['profile_picture']
        location = request.form['location']

        if not username or not password or not fname or not lname or not email or not location:
            flash('All required fields must be filled out.', 'error')
        else:
            name = str(fname) + str(lname)
            User.addUser(user_id, username, name, email, password, profile_image, location)
            return redirect(url_for('index'))
    