# Importing flask module


from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
import sqlite3

# App creation
app = Flask("Flask - Lab")

# SqlLite db file path
DATABASE = 'database.db'

@app.route('/create_database', methods=['GET', 'POST'])
def create_db():
    # Db connection
    conn = sqlite3.connect(DATABASE)
    # Create tables with sqlite3
    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS books (title TEXT, author TEXT, FOREIGN KEY(author) REFERENCES users(username))')
    # Terminate the db connection
    conn.close()
    
    return index()


@app.route('/', methods=['GET', 'POST'])
def index():
    con = sqlite3.connect(DATABASE)
    
    # Fetch data from table
    cur = con.cursor()
    cur.execute("select * from books")
    books = cur.fetchall();  

    return render_template('main.html', books = books)


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
        con = sqlite3.connect(DATABASE)
    
        # Fetch data from table
        cur = con.cursor()
        cur.execute("select * from users")
        users = cur.fetchall();  

        return render_template('users.html', users = users)


@app.route('/add_user', methods=['POST'])
def addUser():
        username = request.form['username']
        password = request.form['password']

        # Add book to DB
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        con.commit()
        cur.execute("select * from users")
        users = cur.fetchall(); 
        con.close()

        return "User succesfully added <br>" + render_template('users.html', users = users)

# Start the app in debug mode
app.run(debug = True)