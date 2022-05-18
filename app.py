from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = '!@#$%'
# database config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prak5'

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        cur = db.connection.cursor()
        email = request.form['email']
        password = request.form['password']
        cur.execute("SELECT * FROM users WHERE email = %s and password = %s", (email,password))
        result = cur.fetchone()
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect(url_for('index'))

        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/index')
def index():
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM users')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', users=data)

@app.route('/logout')
def logout():
    session.pop('is_logged_in', None)
    session.pop('username', None)

    return redirect(url_for('login'))


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        cur = db.connection.cursor()
        email= request.form['email']
        password= request.form['password']
        nama= request.form['username']
        cur.execute(f"INSERT INTO `users` (`username`, `password`, `email`) VALUES ( '{nama}', '{password}', '{email}' )")
        db.connection.commit()
        cur.execute("SELECT * FROM users WHERE email = %s and password = %s", (email,password))
        result = cur.fetchone()
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect(url_for('index'))

        else:
            return render_template('login.html')

    else:
        return render_template('register.html')

if __name__=="__main__":
    app.run(debug=True)