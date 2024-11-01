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
    user_id = session.get('user_id')
    if user_id is None:
        flash('You must be logged in to access this page.', 'error')
        return redirect(url_for('login'))
    user = User.getUserByID(user_id)
    username = user[1]
    return render_template('profile.html', username=username, user_id=user_id)

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
        profile_image = request.form['profile_image']
        location = request.form['location']

        if not username or not password or not fname or not lname or not email or not location:
            flash('All required fields must be filled out.', 'error')
            return redirect(url_for('registration'))
        else:
            name = str(fname) +' '+ str(lname)
            User.addUser(user_id, username, name, email, password, profile_image, location)
            return redirect(url_for('index'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and Password are required.', 'error')
            return redirect(url_for('login'))
        
        user = User.getUser(username)
                
        if user is None:
            flash('Invalid Username. Register for free!', 'error')
            return redirect(url_for('registration'))
        elif user[2] != password:
            flash('Incorrect Password.', 'error')
            return redirect(url_for('login'))
        else:
            session['user_id'] = user[0]
            flash('Login successful.', 'success')
            return redirect(url_for('index', user=user))
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

        

