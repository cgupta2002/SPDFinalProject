from flask import Flask, render_template, url_for, request, redirect
from tools import Tool
from reviews import Review
from users import User
from messages import Message

app = Flask(__name__)

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
