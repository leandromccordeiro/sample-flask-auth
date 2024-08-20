from flask import Flask
from models.user import User
from database import db
from login import login_manager

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)

#view login

#session
@app.route('//login', methods=['POST'])
def login():
    



@app.route("/hello-world", methods=['GET'])
def hello_world():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)