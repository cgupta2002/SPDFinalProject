from flask import Flask, render_template, url_for, request, redirect, flash, session
from tools import Tool
from reviews import Review
from users import User
from messages import Message, Conversation
from werkzeug.utils import secure_filename
import os
from datetime import datetime, date

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
    tools = Tool.getAllTools()
    print(tools)
    return render_template('market.html', user_id=user_id, user=user, tools=tools)

@app.route('/marketplace/add', methods=['GET', 'POST'])
def add_tool():
    user_id = session.get('user_id')
    if request.method == 'GET':
        return render_template('add_tool.html', user_id=user_id, user=User.getUserByID(user_id))
    elif request.method == 'POST':
        tools = Tool.getAllTools()
        last_id = tools[-1]['id']
        tool_id = last_id + 1
        title = request.form['title']
        desc = request.form['desc']
        category = request.form['categories']
        imgPath = request.files['imgPath']
        availability = request.form['availability']
        if imgPath and allowed_file(imgPath.filename):
            filename = secure_filename(imgPath.filename)
            imgPath.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Tool.addTool(tool_id, user_id, title, desc, filename, category, availability, datePosted=date.today())
        else: 
            Tool.addToolNoPic(tool_id, user_id,title, desc, category, availability, datePosted=date.today())
        return redirect(url_for('market'))
    
@app.route('/marketplace/<int:tool_id>')
def tool(tool_id=None):
    user_id = session.get('user_id')
    tool = Tool.getTool(tool_id)
    user = User.getUserByID(user_id)
    seller = tool['user_id']
    seller_info = User.getUserByID(seller)
    return render_template('tool.html', tool=tool, user_id=user_id, user=user, seller=seller_info)


@app.route('/marketplace/<int:tool_id>/edit', methods=['GET', 'POST'])
def edit_tool(tool_id=None):
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.getUserByID(user_id)
        tool = Tool.getTool(tool_id)
        print(tool, tool_id, user_id)
        return render_template('add_tool.html', tool_id=tool_id, tool=tool, user_id=user_id, user=user)
    elif request.method == 'POST': 
        user_id = session.get('user_id')
        title = request.form['title']
        desc = request.form['desc']
        category = request.form['categories']
        imgPath = request.files['imgPath']
        availability = request.form['availability']
        if imgPath and allowed_file(imgPath.filename):
            filename = secure_filename(imgPath.filename)
            imgPath.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Tool.updateTool(tool_id, title, desc, filename, category, availability, datePosted=date.today())
        else: 
            Tool.updateToolNoPic(tool_id,title, desc, category, availability, datePosted=date.today())
        return redirect(url_for('market', user_id=user_id))
    

@app.route('/marketplace/<int:tool_id>/delete', methods = ['GET', 'POST'])
def del_tool(tool_id=None):
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.getUserByID(user_id)
        tool = Tool.getTool(tool_id)
        return render_template('confirmation.html', tool_id = tool_id, tool = tool, user_id=user_id, user=user)
    elif request.method == 'POST':
        tool = Tool.getTool(tool_id)
        user_id = session.get('user_id')
        Tool.delTool(tool_id)
        return redirect(url_for('market', user_id = user_id))

@app.route('/add_review/<int:reviewee_id>', methods=['GET', 'POST'])
def add_review(reviewee_id=None):
    user_id = session.get('user_id')
    reviewee = User.getUserByID(reviewee_id)
    user = User.getUserByID(user_id)
    if request.method == 'GET':
        return render_template('add_review.html', user=user, user_id = user_id, reviewee_id = reviewee_id, reviewee=reviewee)
    elif request.method == 'POST':
        rating = request.form['rating']
        review = request.form['review']
        Review.addReview(reviewee_id, user_id, rating, review, date.today())
        return redirect(url_for('view_profile', viewing_id=reviewee_id))

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if user_id is None:
        flash('You must be logged in to access this page.', 'error')
        return redirect(url_for('login'))
    user = User.getUserByID(user_id)
    ratings = Review.getReviewsForUser(user_id)
    sum = 0
    num_ratings = 0
    avg_rating = 0
    for rating in ratings:
        sum += rating['rating']
        num_ratings += 1
    if ratings:
        avg_rating = sum / num_ratings
        print(ratings, avg_rating)
    user_tools = Tool.getToolsForUser(user_id)
    print(user_tools)
    return render_template('profile.html', user=user, user_id=user_id, ratings=ratings, avg_rating=avg_rating, tools=user_tools)

@app.route('/profile/<int:viewing_id>')
def view_profile(viewing_id=None):
    print(viewing_id)
    user_id = session.get('user_id')
    user = User.getUserByID(user_id)
    viewed = User.getUserByID(viewing_id)
    ratings = Review.getReviewsForUser(viewing_id)
    sum = 0
    num_ratings = 0
    avg_rating = 0
    for rating in ratings:
        sum += rating['rating']
        num_ratings += 1
    if ratings:
        avg_rating = sum / num_ratings
    return render_template('profile.html', user=user, viewed=viewed, user_id=user_id, ratings=ratings, avg_rating=avg_rating)

@app.route('/profile/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id=None):
    if request.method == 'GET':
        user = User.getUserByID(user_id)
        return render_template('registration.html', user_id=user_id, user=user)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        user_id = session['user_id'] 
        
        if not password or not email or not location:
            flash('All required fields must be filled out.', 'error')
            return redirect(url_for('edit_user', user_id=user_id))
        else:
            User.updateUser(user_id, email, password, location)
            user = User.getUserByID(user_id)
            return redirect(url_for('profile', user_id=user_id, user=user))


@app.route('/profile/<int:user_id>/edit_image', methods=['GET','POST'])
def change_image(user_id=None):
    user = User.getUserByID(user_id)
    if request.method == 'GET':
        return render_template('image.html', user_id=user_id, user=user)
    elif request.method == 'POST':
        profile_image = request.files['profile_image']
        if profile_image and allowed_file(profile_image.filename):
            filename = secure_filename(profile_image.filename)
            filepath = "static/images/" + filename
            filepath = filepath.replace("\\", "/")
            profile_image.save(filepath)
            User.updateImage(user_id,filename)
            user = User.getUserByID(user_id)
            return render_template('profile.html', user_id=user_id, user=user)
        else:
            flash("Invalid file format. Please upload a valid image.", "error")
            return redirect(url_for('change_image', user_id=user_id, user=user))


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
    recipient = User.getUserByName(receiver)
    print(receiver, recipient)
    return render_template('conversation.html', user_id = user_id, user=user,conversation_id=conversation_id, convo=convo, receiver=receiver, recipient=recipient)
    
@app.route('/new_message', methods=['GET', 'POST'])
def new_conversation():
    sender_id = session.get('user_id')
    user = User.getUserByID(sender_id)
    users = User.getAllUsers()
    for u in range(len(users)):
        if users[u-1]['user_id'] == sender_id:
            del users[u-1]
    if request.method == 'GET':
        return render_template('new_message.html', user_id = sender_id, sender_id = sender_id, user=user, users=users)
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
        print(profile_image)
        location = request.form['location']
        name = (str(fname) +' '+ str(lname)).title()
        session['user_id'] = user_id
        if profile_image and allowed_file(profile_image.filename):
            filename = secure_filename(profile_image.filename)
            filepath = "static/images/" + filename
            filepath = filepath.replace("\\", "/")
            profile_image.save(filepath)
            if not username or not password or not fname or not lname or not email or not location:
                flash('All required fields must be filled out.', 'error')
                return redirect(url_for('registration'))
            else:
                User.addUser(user_id, username, name, email, password, filename, location)
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
        if user:
            user_id = user['user_id']
            if user['password'] == password:
                session['user_id'] = user['user_id']
                user_id = user['user_id']
                return redirect(url_for('index', user_id=user_id, user=user, profile_image = user['profile_image']))
            else:
                users = User.getAllUsers()
                return render_template('login.html', error="Invalid password.", users=users)
        else:
            users= User.getAllUsers()
            return render_template('login.html', error="User does not exist. Did you mean to register?", users=users)            
    if request.method == 'GET':
        users = User.getAllUsers()
        return render_template('login.html', users=users)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))



