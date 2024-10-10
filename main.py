from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'chave_secreta'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/projeto_cadastro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Mapeando as tabelas existentes
class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    senha = db.Column(db.String(200), nullable=False)


#rotas 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "As senhas não coincidem!", 400

        # verificando se o usuário já existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            return "Usuário já cadastrado com este email!", 400

        # criando um novo usuário
        novo_usuario = Usuario(nome_usuario=username, email=email, senha=password)

        # adicionando ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # verifica se o email e a senha correspondem a um usuário cadastrado
        usuario = Usuario.query.filter_by(email=email, senha=password).first()

        if usuario:
            return redirect(url_for('sucesso'))
        else:
            return "Login inválido. Email ou senha incorretos!", 400

    return render_template('login.html')


# rota para a tela de sucesso, ao fazer o login corretamente
@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')


if __name__ == '__main__':
    app.run(debug=True)
