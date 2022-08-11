from asyncore import file_dispatcher
from distutils import config
from config import config
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy

from flask_mysqldb import MySQL
import MySQLdb.cursors


# instancia
app = Flask(__name__)

app.secret_key = "30302220jefferson"

userpass = "mysql+pymysql://jefferson:30302220@"
basedir = "127.0.0.1"
dbname = "/companydb"


app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

db = SQLAlchemy(app)


class Noticias(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    resumo = db.Column(db.String(120), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(6), nullable=False)
    image_data = db.Column(db.String(6), nullable=False)

    def __init__(self, titulo, descricao, categoria, resumo, autor, date, image_data):
        self.titulo = titulo
        self.descricao = descricao
        self.categoria = categoria
        self.resumo = resumo
        self.autor = autor
        self.date = date
        self.image_data = image_data


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(102), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, fullname):
        self.username = username
        self.password = password
        self.fullname = fullname


@ app.route('/')
def index():
    data_noticias = db.session.query(Noticias)
    return render_template('/index.html', data=data_noticias)


# REGISTER, LOGIN AND LOGOUT

# TODO: TERMINAR A LOGICA DE LOGAR NO SISTEMA, REGISTRAR NOVOS USUARIOS E CRIAR PAINEL ADMIN

@app.route('/login', methods=['GET', 'POST'])
def login():
    data_users = db.session.query(Users)
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        userdetails = request.form
        username = userdetails['username']
        password = userdetails['password']

        if password == 'jefferson':
            return render_template('index.html', data=data_users)
        else:
            return "SUCCESS!,Successfully entered into the Database"
    else:
        return render_template('auth/login.html')


@ app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        resumo = request.form['resumo']
        autor = request.form['autor']
        date = request.form['date']
        image_data = request.form['file']

        add_data = Noticias(titulo, descricao, categoria,
                            resumo, autor, date, image_data)

        db.session.add(add_data)
        db.session.commit()

        flash("A notícia foi cadastrada corretamente.")

        return redirect(url_for('index'))

    return render_template('input.html')


@ app.route('/edit/<int:id>')
def edit_data(id):
    data_noticias = Noticias.query.get(id)
    return render_template('edit.html', data=data_noticias)


@ app.route('/process_edit', methods=['POST', 'GET'])
def process_edit():
    data_noticias = Noticias.query.get(request.form.get('id'))

    data_noticias.titulo = request.form['titulo']
    data_noticias.descricao = request.form['descricao']
    data_noticias.categoria = request.form['categoria']
    data_noticias.resumo = request.form['resumo']
    data_noticias.autor = request.form['autor']
    data_noticias.date = request.form['date']
    data_noticias.image_data = request.form['file']

    db.session.commit()

    flash('Notícia editada com sucesso!!')

    return redirect(url_for('index'))


@ app.route('/delete/<int:id>')
def delete(id):
    data_noticias = Noticias.query.get(id)
    db.session.delete(data_noticias)
    db.session.commit()

    flash('Notícia deletada com sucesso!')

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.run()
