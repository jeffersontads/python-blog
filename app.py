from pydoc import describe
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null 

app = Flask(__name__)
app.secret_key = "30302220jefferson"

userpass = "30302220"
basedir = "127.0.0.1"
dbname = "/companydb"

app.config["SQLALCHEMY_DATABASE_URI"] = userpass + basedir + dbname
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Noticias(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(1000), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    data = db.Column(db.String(6), nullable=False)
    
    def __init__(self, titulo, descricao, categoria, data):
        self.titulo = titulo
        self.descricao = descricao
        self.categoria = categoria
        self.data = data
    
    
@app.route('/')
def index():    
    return render_template('index.html')


@app.route('/input')
def input_data():    
    return render_template('input.html')