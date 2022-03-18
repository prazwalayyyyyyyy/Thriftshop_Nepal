from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus_page():
    return render_template('aboutus.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')


app.run(debug=True)

#@app.route('/about/<username>')
#def about_page(username):
#    return f'<h1>This is the about page of {username}</h1>'

