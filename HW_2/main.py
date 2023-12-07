"""Создать страницу, на которой будет форма для ввода имени и электронной почты. При отправке которой будет создан
cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия, где будет
отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными
пользователя и произведено перенаправление на страницу ввода имени и электронной почты."""

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import make_response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        response = make_response(redirect(url_for('hello', name=name)))
        response.set_cookie('username', name)
        response.set_cookie('email', email)
        return response
    return render_template('index.html')


@app.route('/hello/<string:name>', methods=['POST', 'GET'])
def hello(name):
    if request.method == 'POST':
        response = make_response(redirect(url_for('index')))
        response.set_cookie('username', max_age=0)
        response.set_cookie('email', max_age=0)
        return response
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run()
