# Importing flask module


from flask import Flask, template_rendered
from flask import render_template, request, redirect, url_for, flash, session
from flask_session import Session
import sqlite3

# App creation
app = Flask("Flask - Lab")

# Session creation
sess = Session()

# SqlLite db file path
DATABASE = 'database.db'

@app.route('/create_database', methods=['GET', 'POST'])
def create_db():
    # Db connection
    conn = sqlite3.connect(DATABASE)
    # Create tables with sqlite3
    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, isAdmin TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT, FOREIGN KEY(author) REFERENCES users(username))')
    # Terminate the db connection
    conn.close()
    
    return index()


@app.route('/', methods=['GET', 'POST'])
def index():

    if 'user' in session:
        con = sqlite3.connect(DATABASE)
    
        # Fetch data from table
        cur = con.cursor()
        cur.execute("select * from books")
        books = cur.fetchall();  

        return render_template('main.html', books = books)

    else:
        return render_template('login.html')

    


@app.route('/add_book', methods=['POST'])
def addBook():
        title = request.form['title']
        author = request.form['author']

        # Add book to DB
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("INSERT INTO books (title,author) VALUES (?,?)",(title,author) )
        con.commit()
        con.close()

        return "Book succesfully added <br>" + index()


@app.route('/users', methods=['POST', 'GET'])
def showUsers():

        if request.args.get("username"):
            username = request.args.get("username")
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            currentLoggedUser = session["user"]
            cur.execute("select * from users where username=?", (currentLoggedUser, ))
            currentUser = cur.fetchone()
            if currentUser[2] != 'yes':
                return 'Only admin has access!'
            else:
                cur.execute("select * from users where username=?", (username, ))
                user = cur.fetchone()
                con.close()
                return render_template('user.html', user = user)
            
        else:
            con = sqlite3.connect(DATABASE)
        
            # Fetch data from table
            cur = con.cursor()
            cur.execute("select * from users")
            users = cur.fetchall()
            con.close()  

            return render_template('users.html', users = users)


@app.route('/add_user', methods=['POST'])
def addUser():
        username = request.form['username']
        password = request.form['password']
        isAdmin = 'no' if (request.form.get('isAdmin') is None) else 'yes'        
        # Add book to DB
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("INSERT INTO users (username,password,isAdmin) VALUES (?,?,?)",(username,password,isAdmin))
        con.commit()
        cur.execute("select * from users")
        users = cur.fetchall(); 
        con.close()

        return "User succesfully added <br>" + render_template('users.html', users = users)


@app.route('/login', methods=['GET'])
def showLoginScreen():
    
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logOut():
    # If the user session exists - remove it
    if 'user' in session:
        session.pop('user')
    else:
        # Redirect the client to the homepage
        redirect(url_for('index'))
    
    return "Logged out <br>  <a href='/'> Back </a>"


@app.route('/authenticate', methods=['POST'])
def authenticate():

    username = request.form['username']
    password = request.form['password']
    print(username)
    print(password)
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("select * from users where username=?", (username, ))
    requestedUser = cur.fetchone()
    con.close()
    print(requestedUser)
    if requestedUser is None or requestedUser[1] != password:
        return "Invalid username or password"

    session["user"] = username
    
    return f'Hello, welcome {username}' + index()



# Start the app in debug mode
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)
app.config.from_object(__name__)
app.run(debug = True)