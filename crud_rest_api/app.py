from flask import Flask, render_template, request, redirect, url_for, Response
from models import db, Estudante

import json

import os
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')

app = Flask(__name__, template_folder='templates', static_folder='public')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudantes.sqlite3'



@app.route('/')
def index():
    estudantes = Estudante.query.all()
    result = [estudante.to_dict()  for estudante in estudantes]
    return Response(response=json.dumps(result), status=200, content_type="application/json")


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        estudante = Estudante(nome, idade)
        db.session.add(estudante)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    estudante = Estudante.query.get(id)
    if request.method == 'POST':
        estudante.nome = request.form['nome']
        estudante.idade = request.form['idade']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', estudante=estudante)


@app.route('/delete/<int:id>')
def delete(id):
    estudante = Estudante.query.get(id)
    db.session.delete(estudante)
    db.session.commit()
    return redirect(url_for('index'))


if __name__=="__main__":
    db.init_app(app=app)
    with app.test_request_context():
        db.create_all()
    app.run(debug=True)