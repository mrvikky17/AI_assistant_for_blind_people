from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
app = Flask(__name__)
from chatbot import get_bot_response

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('Login.html')


@app.route('/logout')
def logout():
    session.pop('name', None)
    return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', name=session.get('name'))
    
# @app.route("/chat", methods=["POST"])
# def chat():
#     user_input = request.json.get("message")
#     bot_response = get_bot_response(user_input)
#     return jsonify({"response": bot_response})

# Forms

if __name__ == '__main__':
    app.run( debug=True,port=8000)