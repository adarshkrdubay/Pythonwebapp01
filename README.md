# Python Web-App 01


This is a Flask application that serves a website. It includes routes for handling various HTTP requests, a connection to a MySQL database, and styling using CSS.

## Overview

This Flask application is designed to serve a website that provides various functionalities such as user login, a dashboard, and project details. It uses the Flask web framework and MySQL database for data storage.
Check it: https://mywebtest.adarshkrdubay.repl.co

## Features

- User login functionality with username and password verification.
- Session management to maintain user authentication.
- Dashboard page to display personalized information.
- Project details page to showcase different projects.
- Styling using CSS for an enhanced user interface.

## Installation

1. Clone the repository or download the code:

```bash
git clone https://github.com/yourusername/your-repo.git
```
2. Install the required dependencies:
```bash
pip3 install -r requirements.txt
```
## Usage
1. Start the Flask application.
```python
python3 app.py
```
2. Access the website locally in your browser.
```curl
http://localhost:81
```
## Configuration
1. Before running the application, make sure to set up the following environment variables:
```sql
SECRET_KEY: Secret key used for session management.
MYSQL_HOST: Hostname of the MySQL database.
MYSQL_USER: MySQL database username.
MYSQL_PASSWORD: MySQL database password.
MYSQL_DB: Name of the MySQL database.
```
## Dependencies
1. Flask
2. pymysql
## License
This project is licensed under the MIT License.


