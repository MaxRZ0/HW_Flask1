from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/jackets')
def jackets():
    return render_template('jackets.html')


@app.route('/pants')
def pants():
    return render_template('pants.html')


@app.route('/shoes')
def shoes():
    return render_template('shoes.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


if __name__ == '__main__':
    app.run()
