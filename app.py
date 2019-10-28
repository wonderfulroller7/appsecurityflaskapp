from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, world!"

@app.route("/login")
def login():
    return "Login user."

@app.route("/register")
def register():
    return "Register user."

@app.route("/spell_check")
def spell_check():
    return "Spell Check."

if __name__ == "__main__":
    app.run(debug=True)