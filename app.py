from flask import *
import pymysql
import os

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.environ['SECRET_KEY']

# Configure MySQL connection
app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']

# Establish a connection to MySQL
mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/home')
def home():
    # Render the index.html template
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    # Serve the favicon.ico file from the static directory
    return app.send_static_file('static/favicon.ico')

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
                # Redirect to the dashboard route
                return redirect('/dashboard')
            else:
                msg = "Incorrect Username or Password"
        else:
            msg = "Incorrect Username or Password"

    # Render the login.html template with the appropriate message
    return render_template('login.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    if 'Username' in session:
        Username = session['Username']
        # Display the welcome message with the logged-in Username
        return f"Welcome, {Username}!"
    else:
        # Redirect to the login route if the user is not logged in
        return redirect('/'login)

if __name__ == '__main__':
    # Run the application on host '0.0.0.0' and port 81
    app.run(host='0.0.0.0', port=81)
