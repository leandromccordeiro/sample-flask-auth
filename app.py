from flask import Flask, request, jsonify
from models.user import User
from database import db
from login import login_manager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager.init_app(app)

#view login
login_manager.login_view = 'login'

#session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        #login
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({'messege': 'Autenticação realizada com sucesso'})
    
    return jsonify({'message':'Credenciais Inválidas'}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'messege': "Logout realizado com sucesso!"})

@app.route('/user', methods=['POST'])
def create_user ():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'messege': 'Cadastro realizado com sucesso!'})
    
    return jsonify({'messege': 'Dados inválidos!'}), 400

@app.route('/user/<int:id_user>', methods=['GET'])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return {'username': user.username}
    
    return jsonify({'messege': 'Usuário não encontrado'}), 404

@app.route('/hello-world', methods=['GET'])
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)