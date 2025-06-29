from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
import auth
import database
import bot
import random
from urllib.parse import urlparse

app = Flask(__name__)

JWT_SECRET="redacted"

database.init_db()

class Greeting:
    def __init__(self, greeting, compliment):
        self.greeting = greeting
        self.compliment = compliment

def greet(template, person):
    return template.format(person=person)


@app.route('/')
def index():
    token = request.cookies.get('token')
    if token:
        try:
            payload = auth.decode_token(token)
            return redirect(url_for('home'))
        except:
            pass
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = database.get_user(username)
        if user and auth.verify_password(password, user['password']):
            token = auth.generate_token(username, user['role'])
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('token', token)
            return resp
        
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        if database.get_user(username):
            return render_template('register.html', error='Username already exists')
        database.create_user(username, auth.hash_password(password), nickname, 'user')
        token = auth.generate_token(username, 'user')
        resp = make_response(redirect(url_for('home')))
        resp.set_cookie('token', token)
        return resp
    
    return render_template('register.html')

@app.route('/home')
def home():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    try:
        payload = auth.decode_token(token)
        username = payload['username']
        role = payload['role']
        user = database.get_user(username)
        greetings = ["Hello", "Hi", "Hey", "Greetings", "Yo"]
        compliments = ["Nice to see you", "Looking sharp!", "Hope you're having a great day", "You're awesome!", "Always a pleasure"]
        selected_greeting = random.choice(greetings)
        selected_compliment = random.choice(compliments)
        person = Greeting(selected_greeting, selected_compliment)
        template = " {person.greeting}, {person.compliment}"
        template = user['nickname']+template
        greeting_text = greet(template, person)
        return render_template(
            'home.html', 
            greeting_text=greeting_text, 
            role=role, 
            notes=database.get_user_notes(username)
        )
    except:
        return redirect(url_for('login'))

@app.route('/create_note', methods=['POST'])
def create_note():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    
    try:
        payload = auth.decode_token(token)
        username = payload['username']
        content = request.form.get('content')
        note_id = database.create_note(username, content)
        
        return redirect(url_for('home'))
    except:
        return redirect(url_for('login'))

@app.route('/note/<note_id>')
def get_note(note_id):
    note = database.get_note_by_id(note_id)
    if note:
        return render_template('note.html', note=note)
    return "Note not found", 404

@app.route('/report', methods=['POST'])
def report():
    token = request.cookies.get('token')
    if not token:
        return jsonify({"error": "Authentication required"}), 401
    try:
        payload = auth.decode_token(token)
        if payload['role'] != 'director':
            return jsonify({"error": "You should be the Youtube director"}), 403
        youtube_url = request.form.get('youtube_url')
        parsed_url = urlparse(youtube_url)
        if not "youtube.com" in parsed_url.netloc and not "youtu.be" in parsed_url.netloc:
            return jsonify({"error": "Only YouTube URLs are allowed"}), 400
        
        bot.visit_url(youtube_url)
        
        return jsonify({"success": "URL reported and will be visited by the Youtube director soon"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('token')
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)