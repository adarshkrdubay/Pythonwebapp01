from flask import *
import pymysql
import os
import re

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']
app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('static/logo.png')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form:
        Username = request.form['Username']
        Password = request.form['Password']
        cursor = mysql.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE BINARY Username = %s', (Username,))
        account = cursor.fetchone()
        if account:
            cursor.execute(
                "SELECT * FROM user WHERE BINARY Username = %s AND BINARY Password = %s", (Username, Password)
            )
            account = cursor.fetchone()
            if account:
                session['Username'] = account['Username']
                Usernamelog = session['Username']
                msg = f'Logged in successfully as {Usernamelog}!'
                print(msg)
                return redirect('/dashboard')
            else:
                msg = "Incorrect Username or Password"
        else:
            msg = "Incorrect Username or Password"

    return render_template('login.html', msg=msg)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  msg = ''
  if request.method == 'POST' and 'Username' in request.form and 'Name' in request.form and 'Email' in request.form and 'Password' in request.form and 'Reenterpassword' in request.form and 'key' in request.form:
        Username = request.form['Username']
        Name = request.form['Name']
        Email = request.form['Email']
        Password = request.form['Password']
        Reenterpassword = request.form['Reenterpassword']
        key = request.form['key']
        cursor = mysql.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE BINARY Username = %s', (Username,))
        accountu = cursor.fetchone()
        cursor = mysql.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE BINARY Email = %s', (Email,))
        accounte = cursor.fetchone()
        if Reenterpassword != Password:
          msg = 'Password dose not match'
        elif accountu:
            msg = 'Username already taken !'
        elif accounte:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', Username):
            msg = 'Username must contain only characters and numbers !'
        elif key !=  os.environ['a_key']:
            msg = 'Access key is wrong'
        else:
          cursor = mysql.cursor(pymysql.cursors.DictCursor)
          cursor.execute('INSERT INTO user VALUES (%s, %s, %s, %s)', (Name, Username, Email, Password))
          mysql.commit()
          msg = 'Account registered'
          return render_template('login.html', msg=msg)
          
  elif request.method == 'POST':
        msg = 'Please fill out the form !'
        
  return render_template('signup.html', msg=msg)
@app.route('/passreset' , methods=['GET', 'POST'])
def passreset():
    msg = ''
    if request.method == 'POST' and 'Username' in request.form and 'Password' in request.form and 'Reenterpassword' in request.form and 'key' in request.form:
      Username = request.form['Username']
      Password = request.form['Password']
      Reepass = request.form['Reenterpassword']
      key = request.form['key']
      cursor = mysql.cursor(pymysql.cursors.DictCursor)
      cursor.execute('SELECT * FROM user WHERE BINARY Username = %s', (Username,))
      accountu = cursor.fetchone()
      if Reepass != Password:
           msg = 'Password dose not match'
      elif key !=  os.environ['a_key']:
              msg = 'Access key is wrong'
      elif not accountu:
          msg = 'User not found'
      else:
          if Username == "test" or Username == "try":
              msg ="You Can't change password for dummy user."
          else:
              cursor = mysql.cursor(pymysql.cursors.DictCursor)
              cursor.execute("UPDATE user SET Password=%s WHERE Username=%s", (Password, Username))
              mysql.commit()
              msg= "Password Changed"
              return render_template('login.html', msg=msg)

    return render_template('passreset.html', msg=msg)


    
    
@app.route('/dashboard')
def dashboard():
    if 'Username' in session:
        Username = session['Username']
        return f"Welcome, {Username}!"
    else:
        return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
