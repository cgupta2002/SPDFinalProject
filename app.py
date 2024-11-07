from flask import Flask, render_template, url_for, request, redirect, flash, session
from tools import Tool
from reviews import Review
from users import User
from messages import Message, Conversation
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = '2bshd9ei3nd40fk'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    return render_template('index.html', user_id=user_id, user=user)

@app.route('/marketplace')
def market():
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    return render_template('market.html', user_id=user_id, user=user)

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    user_id = session.get('user_id')
    if user_id is None:
        flash('You must be logged in to access this page.', 'error')
        return redirect(url_for('login'))
    user = User.getUserByID(user_id)
    return render_template('profile.html', user=user, user_id=user_id)


@app.route('/messages')
def message():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    else:
        conversations = Conversation.get_user_conversations(user_id)
        conversation_list = []
        for conversation in conversations:
            messages = Conversation.get_conversation_messages(conversation[0])
            conversation_list.append(messages)
        user = User.getUserByID(user_id)
        print(conversation_list)
        users = User.getAllUsers()
        return render_template('message.html', conversation_list=conversation_list, users=users, user=user, user_id=user_id)


@app.route('/messages/<int:conversation_id>', methods=['GET', 'POST'])
def conversation(conversation_id=None):
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    convo = Conversation.get_all_conversation_messages(conversation_id)
    if convo[0]['receiver_id'] == user_id:
        receiver = User.getName(convo[0]['sender_id'])
    else:
        receiver = User.getName(convo[0]['receiver_id'])
    print(convo)
    return render_template('conversation.html', user_id = user_id, user=user,conversation_id=conversation_id, convo=convo, receiver=receiver)
        
    

@app.route('/new_message', methods=['GET', 'POST'])
def new_conversation():
    sender_id = session.get('user_id')
    user = User.getUserByID(sender_id)
    users = User.getAllUsers()
    if request.method == 'GET':
        return render_template('new_message.html', sender_id = sender_id, user=user, users=users)
    elif request.method == 'POST':
        recipient_id = request.form['recipient_id']
        content = request.form['content']
        timestamp = datetime.now()
        conversation_id = Conversation.create_conversation(sender_id, recipient_id)     
        Conversation.insert_message(conversation_id,sender_id, recipient_id, content, timestamp)   
        return redirect(url_for('message'))


@app.route('/send_message/<int:conversation_id>', methods=['POST'])
def send_message(conversation_id=None):
    sender_id = session.get('user_id')
    content = request.form['content']
    convo = Conversation.get_conversation_messages(conversation_id)
    receiver_id = convo['receiver_id']
    print(convo)
    Conversation.insert_message(conversation_id, sender_id, receiver_id,content, timestamp=datetime.now())
    return redirect(url_for('conversation', conversation_id=conversation_id))


@app.route('/marketplace/add', methods=['GET', 'POST'])
def add_tool():
    user_id = session.get('user_id')
    if request.method == 'GET':

        return render_template('add_tool.html', user_id=user_id, user=User.getUserByID(user_id))
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
        profile_image = request.files['profile_image']
        location = request.form['location']
        name = (str(fname) +' '+ str(lname)).title()
        if profile_image and allowed_file(profile_image.filename):
            filename = secure_filename(profile_image.filename)
            filepath = filename
            filepath = filepath.replace("\\", "/")
            profile_image.save(filepath)
            if not username or not password or not fname or not lname or not email or not location:
                flash('All required fields must be filled out.', 'error')
                return redirect(url_for('registration'))
            else:
                
                User.addUser(user_id, username, name, email, password, filepath, location)
                user = User.getUserByID(user_id)
                return redirect(url_for('index', user_id=user_id, user=user))
        elif not profile_image:
            User.addUserNoPic(user_id, username, name, email, password, location)
            user = User.getUserByID(user_id)
            return redirect(url_for('index', user_id=user_id, user=user))
        else:
            flash('Invalid file format. Please upload an image.')
            return redirect(url_for('registration'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    user_id = session.get('user_id')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Username and Password are required.', 'error')
            return redirect(url_for('login'))
        
        user = User.getUser(username)
        user_id = user['user_id']
                
        if user is None:
            flash('Invalid Username. Register for free!', 'error')
            return redirect(url_for('registration'))
        elif user['password'] != password:
            flash('Incorrect Password.', 'error')
            return redirect(url_for('login'))
        else:
            session['user_id'] = user['user_id']
            flash('Login successful.', 'success')
            user_id = user['user_id']
            return redirect(url_for('index', user_id=user_id, user=user, profile_image = user['profile_image']))
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))


        

