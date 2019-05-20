from flask import Flask, session, jsonify, request 
import os
import traceback

app = Flask(__name__)
app.secret_key = os.urandom(24)

count = 0

@app.route('/')
def index():
    session['user'] = 'Anthony'
    return "Index"

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return "Not logged in!"

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return "dropped"

@app.route('/chat', methods=['POST'])
def chat():
    global count
    json_input = request.json
    #print(json_input)
    count += 1

    return(str(count))
    #return "Cheese"




if __name__ == '__main__':
    app.run(debug=True)
