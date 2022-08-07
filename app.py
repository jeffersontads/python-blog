from asyncore import file_dispatcher
import io
from flask import Flask, render_template, redirect, url_for, request, flash
import urllib.request
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.secret_key = "30302220jefferson"

userpass = "mysql+pymysql://jefferson:30302220@"
basedir = "127.0.0.1"
dbname = "/companydb"

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# UPLOAD_FOLDER = 'static/uploads/'


# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@ app.route('/')
def index():
    data_noticias = db.session.query(Noticias)
    return render_template('index.html', data=data_noticias)


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


# @app.route('/', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
#     file = request.files['file']
#     if file.filename == '':
#         flash('No image selected for uploading')
#         return redirect(request.url)
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         #print('upload_image filename: ' + filename)
#         flash('Image successfully uploaded and displayed below')
#         return render_template('index.html', filename=filename)
#     else:
#         flash('Allowed image types are - png, jpg, jpeg, gif')
#         return redirect(request.url)


# @app.route('/display/<filename>')
# def display_image(filename):
#     #print('display_image filename: ' + filename)
#     return redirect(url_for('static', filename='uploads/' + filename), code=301)


# if __name__ == "__main__":
#     app.run()


# REGISTER, LOGIN AND LOGOUT
@app.route('/login', methods=['GET', 'POST'])
def login():
    data_noticias = db.session.query(Noticias)
    return render_template('login.html', data=data_noticias)
