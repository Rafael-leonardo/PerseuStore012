from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///produto.sqlite3'

db = SQLAlchemy(app)

class Pessoas(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.Integer)
    senha = db.Column(db.String(20))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/carrinho', methods=['GET', 'POST'])
def carrinho():
    return render_template('carrinho.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/banco', methods=['GET', 'POST'])
def banco():
    pessoaTable = Pessoas.query.all()
    return render_template('banco.html', pessoaTable=pessoaTable)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        pessoa = Pessoas(request.form['nome'], request.form['email'], request.form['senha'])
        db.session.add(pessoa)
        db.session.commit()
        return redirect(url_for('banco'))
    return render_template('add.html')

@app.route('/del/<int:id>', methods=['GET', 'POST'])
def delete(id):
    pessoa = Pessoas.query.get(id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('banco'))

@app.route('/<string:nome>')
def erro(nome):
  variavel = f'Pagina ({nome}) não existe!'
  return render_template('erro.html', variavel=variavel)

if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)
